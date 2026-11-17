"""Qwen services for logged-in trip planning.

For travel and food, Qwen returns JSON to this service. A validator converts
the JSON to the *unchanged* text markers consumed by login_app.py.
"""
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from Service.config import (
    QWEN_MODEL_NAME,
    QWEN_BASE_URL,
    TRAVEL_PROMPT,
    FOOD_PROMPT,
    ACCOMMODATION_PROMPT,
    SUMMARY_PROMPT,
)
from Service.model.structured_output import format_food, format_routes


ROUTES_JSON_INSTRUCTIONS = """
重要：以上关于文本输出排版的示例仅描述旅行内容要求，不是最终输出格式。
现在只输出一个严格合法的 JSON 对象，不要 Markdown、解释或代码块。
必须使用如下结构：{"routes":["第一条完整路线描述","第二条完整路线描述","第三条完整路线描述"]}
routes 必须恰好有三个非空中文字符串，每个字符串是完整的自然语言路线。
字符串内禁止包含“路线1”、“路线2”、“路线3”、“餐厅 1”、“餐厅 2”、“餐厅 3”或“@@@”。
不要在字符串中写路线编号或开头的路线标签；程序会自动添加。
"""

FOOD_JSON_INSTRUCTIONS = """
重要：以上文本排版示例仅描述推荐内容要求，不是最终输出格式。
只输出一个严格合法的 JSON 对象，不要 Markdown、解释或代码块。
结构必须为：
{"meals":[{"meal_type":"早餐","restaurants":[
{"name":"店名","cuisine":"菜系","price":"人均价格（元）","reason":"推荐理由","navigation":"导航建议"},
{"name":"店名","cuisine":"菜系","price":"人均价格（元）","reason":"推荐理由","navigation":"导航建议"},
{"name":"店名","cuisine":"菜系","price":"人均价格（元）","reason":"推荐理由","navigation":"导航建议"}
]}]}
根据用户 meal_preferences 的原始顺序，每一种餐别各返回一个 meals 元素，
meal_type 必须逐字与用户提供的餐别名称一致；每组恰好有三家不同餐厅。
所有字段都必须是非空的中文字符串。内容应遵守预算和距离偏好。
任何自由文本字段都不能出现“路线1”、“路线2”、“路线3”、
“餐厅 1”、“餐厅 2”、“餐厅 3”或“@@@”；这些标签由程序自动添加。
"""


class Login:
    def __init__(self):
        self.start_model()
        self.prompts()
        self.initialize()

    def start_model(self):
        self.model = OllamaLLM(model=QWEN_MODEL_NAME, base_url=QWEN_BASE_URL)
        # Ollama JSON mode constrains syntax; Python schema validation below
        # additionally checks counts, fields and the backend's splitting markers.
        self.json_model = OllamaLLM(
            model=QWEN_MODEL_NAME, base_url=QWEN_BASE_URL,
            format="json", temperature=0,
        )

    def prompts(self):
        self.prompt_travel = ChatPromptTemplate.from_template(TRAVEL_PROMPT)
        self.prompt_food = ChatPromptTemplate.from_template(FOOD_PROMPT)
        self.prompt_accommodation = ChatPromptTemplate.from_template(ACCOMMODATION_PROMPT)
        self.prompt_summary = ChatPromptTemplate.from_template(SUMMARY_PROMPT)

    def initialize(self):
        # Only accommodation and summary still use raw natural-language output.
        self.chain_accommodation = self.prompt_accommodation | self.model
        self.chain_summary = self.prompt_summary | self.model

    def _generate_validated(self, prompt: str, formatter):
        """Never return malformed text as success; try a corrective generation."""
        last_error = None
        for attempt in range(3):
            instructions = prompt
            if attempt:
                instructions += (
                    "\n上一次回答未通过结构验证。必须返回且仅返回符合以上格式的JSON。"
                    f" 错误类型：{type(last_error).__name__}。"
                )
            raw = self.json_model.invoke(instructions)
            try:
                return formatter(raw)
            except ValueError as exc:
                last_error = exc
        raise ValueError(
            "Qwen failed to generate a valid structured response after 3 attempts"
        ) from last_error

    def invoke(self, category: str, data: Dict):
        if category == "travel":
            prompt = self.prompt_travel.format(**data) + "\n\n" + ROUTES_JSON_INSTRUCTIONS
            return self._generate_validated(prompt, format_routes)
        elif category == "food":
            prompt = self.prompt_food.format(**data) + "\n\n" + FOOD_JSON_INSTRUCTIONS
            return self._generate_validated(
                prompt, lambda raw: format_food(raw, data["meal_preferences"])
            )
        elif category == "accommodation":
            return self.chain_accommodation.invoke(data)
        elif category == "summary":
            return self.chain_summary.invoke(data)
        else:
            return "无效类别，请选择 'travel'、'food' 或 'accommodation'。"

"""Qwen generation for logged-in travel planning.

Travel/food are schema constrained through Ollama's native generate API.
The public return type for those categories is list[str], not a text blob.
Accommodation and summary intentionally retain their existing string output.
"""
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from ollama import Client

from Service.config import (
    QWEN_MODEL_NAME,
    QWEN_BASE_URL,
    TRAVEL_PROMPT,
    FOOD_PROMPT,
    ACCOMMODATION_PROMPT,
    SUMMARY_PROMPT,
)
from Service.model.structured_output import (
    FoodResult,
    RouteResult,
    format_food,
    format_routes,
)


class Login:
    def __init__(self):
        self.start_model()
        self.prompts()
        self.initialize()

    def start_model(self):
        self.model = OllamaLLM(model=QWEN_MODEL_NAME, base_url=QWEN_BASE_URL)
        self.structured_client = Client(host=QWEN_BASE_URL)

    def prompts(self):
        self.prompt_travel = ChatPromptTemplate.from_template(TRAVEL_PROMPT)
        self.prompt_food = ChatPromptTemplate.from_template(FOOD_PROMPT)
        self.prompt_accommodation = ChatPromptTemplate.from_template(ACCOMMODATION_PROMPT)
        self.prompt_summary = ChatPromptTemplate.from_template(SUMMARY_PROMPT)

    def initialize(self):
        self.chain_accommodation = self.prompt_accommodation | self.model
        self.chain_summary = self.prompt_summary | self.model

    def _generate_validated(self, prompt: str, schema, formatter):
        """Retry invalid outputs; never report malformed recommendations as success."""
        last_error = None
        for attempt in range(3):
            retry_note = (
                ""
                if attempt == 0
                else "\n上一次结果未通过字段和数量验证。请严格按照JSON Schema重新生成。"
            )
            # 'format' is a JSON Schema dict, not just the string 'json'.
            response = self.structured_client.generate(
                model=QWEN_MODEL_NAME,
                prompt=prompt + retry_note,
                format=schema.model_json_schema(),
                options={"temperature": 0},
                stream=False,
            )
            try:
                return formatter(response.response)
            except ValueError as exc:
                last_error = exc
        raise ValueError("Qwen failed structured-output validation after 3 attempts") from last_error

    def invoke(self, category: str, data: Dict):
        if category == "travel":
            prompt = self.prompt_travel.format(**data)
            return self._generate_validated(prompt, RouteResult, format_routes)
        elif category == "food":
            prompt = self.prompt_food.format(**data)
            return self._generate_validated(
                prompt,
                FoodResult,
                lambda raw: format_food(raw, data["meal_preferences"]),
            )
        elif category == "accommodation":
            return self.chain_accommodation.invoke(data)
        elif category == "summary":
            return self.chain_summary.invoke(data)
        else:
            return "无效类别，请选择 'travel'、'food'、'accommodation' 或 'summary'。"

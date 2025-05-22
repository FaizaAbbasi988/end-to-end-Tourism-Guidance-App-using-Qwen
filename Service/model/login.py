from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from typing import Dict

class Login():
    def __init__(self):
        self.start_model()
        self.prompts()
        self.initialize()

    def start_model(self):
        self.model = OllamaLLM(model="qwen2.5:3b", base_url="http://localhost:11434")

    def prompts(self):
        # These should be your pre-written templates
        self.travel_template = """
您是一位专业的太原旅行规划助手。请根据用户的旅行时间、兴趣偏好、出行天数以及旅行者的年龄，生成三个完整的个性化太原旅行路线选项。

📥 输入参数：

到达日期和时间： {arrival_datetime}

离开日期和时间： {departure_datetime}

旅行者年龄（列表）： {traveler_ages}

历史文化旅游兴趣： {historical_culture_interests}

民俗文化旅游兴趣： {folk_culture_interests}

名人人文旅游兴趣： {famous_humanistic_interests}

红色文化旅游兴趣： {red_culture_interests}

美食旅游兴趣： {food_interests}

网红文化旅游兴趣： {celebrity_culture_interests}

兴趣优先级顺序（例如：1. 美食旅游，2. 历史文化旅游，3. 民俗文化旅游）： {interest_priority_order}

📝 任务说明：

请根据用户选择的兴趣类别、兴趣优先级顺序、旅行的天数以及旅行者的年龄段，规划出 三个不同的太原旅行路线。每条路线需覆盖用户所选择的所有旅游类别，并在行程顺序或主题侧重点上进行变化。

请合理安排每天的行程内容，使其适合不同年龄层的游客：如老年人或儿童安排轻松舒适的活动，年轻人可适当增加探索性和深度体验的内容。同时，需结合太原景点的地理分布和游览习惯，确保行程流畅合理，注重每日活动节奏的平衡。

每条路线请以 自然段落的叙述方式 进行描述，不要使用列表符号、括号或引号。描述需清晰地指出每日的行程，例如：

“第一天可以从参观山西博物院开始，随后漫步于迎泽公园，享受轻松的一天。第二天可前往晋祠，深入了解太原的历史文化，并在附近品尝当地特色午餐……”

🧾 输出格式：

🎉 根据您的出行时间、兴趣偏好和旅伴年龄，我们为您定制了三条太原旅行路线，请查阅并选择最适合的一条：

🔹 路线一：
[自然段文字，描述路线 1]

🔹 路线二：
[自然段文字，描述路线 2]

🔹 路线三：
[自然段文字，描述路线 3]



"""
        
        self.food_template = """

你是一位专业的太原旅行助手。请根据用户提供的信息，为用户推荐符合要求的当地餐厅。请根据与所选路线的距离、预算以及用户选择的用餐偏好，提供三家餐厅名称。

📥 用户输入参数：

- 所选旅行路线：{selected_route}
- 用餐人数：{number_of_people}
- 人均用餐预算：{budget} 元
- 餐厅与景点之间可接受的距离范围：{distance_range}
- 用户用餐偏好（仅提供用户请求的餐食，可能包括早餐、午餐、小吃或晚餐）：{meal_preferences}

📝 任务：

请根据与所选路线的距离、预算以及用户选择的用餐偏好，提供三家餐厅名称。
如果用户选择：
- 早餐：靠近路线上的第一个景点；

- 午餐：靠近路线中途的景点；

- 小吃：可靠近任何景点；

- 晚餐：靠近路线上的最后一个景点。

对于用户选择的每种餐食类型，请提供三项符合以下要求的推荐：

- 价格：人均价格不得超过预算；

- 必须包含以下内容：

- 餐厅名称

- 菜系（例如：山西特色菜、小吃、川菜、清真、素食等）；

- 人均价格（必须符合预算）；

- 简洁的推荐理由（1~2 句话，突出环境或菜品特色）；

- 导航建议（例如：“距离 XXX 步行约 5 分钟”或“乘坐出租车约 10 分钟”）。

📌 输出格式：

请严格遵循以下格式，仅输出用户选择的餐食。例如，如果用户选择了早餐和晚餐，则输出应为：

早餐：

选项 1：
XXXX

选项 2：
XXXX

选项 3：
XXXX

晚餐：

选项 1：
XXXX

选项 2：
XXXX

选项 3：
XXXX

"""
        
        self.accommodation_template = """
你是一位专业的太原市旅行助理。请根据用户选择的旅行路线和住宿需求，推荐两到三个合适的住宿选项。

以下是用户已选择的旅行路线（用于判断住宿的地理位置是否便捷，是否靠近关键景点或交通枢纽）：
{selected_route}

用户的住宿需求如下：
- 入住日期范围：{date_of_stay}
- 住宿类型偏好：{accommodation_type}（如：酒店客房、民宿、公寓等）
- 酒店星级：{stars}星级
- 每晚最高预算（总价）：{room_rate}元人民币
- 总人数：{total_people}
- 成人数量：{adults}
- 老年人数量：{elderly}
- 儿童数量：{children}
- 儿童年龄：{children_age}
- 偏好的出行方式：{transportation_preference}（如出租车、地铁、公交等）

🎯 任务说明：

请推荐 2–3 个住宿选项，要求符合用户提供的预算和住宿需求，尽量靠近所选路线中的主要景点或交通便利区域。推荐时需特别考虑老年人和儿童的舒适性、安全性与无障碍需求。

每个住宿选项请提供以下信息：
- 住宿名称
- 所在位置（例如哪个区域或靠近哪些景点）
- 预估每晚价格（不超出用户预算）
- 服务和设施简介（如电梯、无障碍通道、是否含早餐、是否有家庭房、是否适合儿童等）
- 从住宿前往主要景点或交通枢纽的推荐交通方式（基于用户的出行偏好）

📌 回答要求：

语气应专业、自然，结构清晰。每个住宿选项单独成段，信息完整，便于用户做出决策。

回答：
"""
        self.summary = """你是太原的专业旅行助理。请根据用户选择的旅行路线、餐饮偏好和住宿选择，为用户生成完整的旅行计划概要。

以下是用户的选择信息：

🧭 路线安排：

{selected_route}

🍽️ 餐饮推荐（一日三餐）：

{selected_food}

🏨 住宿安排：

{selected_accommodation}

🎯 任务：

根据以上信息，请生成完整的太原旅行概要，包含以下三个部分：

1. 📅 每日行程安排：

- 根据 selected_route 中的景点顺序进行拆分；

- 合理分配行程到每一天（根据路线距离和节奏合理性）；

- 列出每天推荐的景点参观顺序、推荐的餐厅名称（早餐、午餐、晚餐）以及住宿名称。

2. 🎒 行前准备建议（“行前准备”）：

建议用户携带的物品（例如身份证、雨具、儿童用品、老人用品等）；
- 提醒用户提前预订门票、交通工具或需要预订的物品；
- 根据季节和天气推荐相应的衣物或用品。

3. ⚠️ 注意事项：
- 包括但不限于景点排队、交通高峰、门票预订、餐厅高峰时段等；
- 老年人和儿童的安全提示；
- 特殊说明，例如出租车/地铁使用建议、是否接受移动支付等。

📝 输出要求：

- 内容专业自然，分段清晰，结构严谨；
- 请以“第X天”为标题，每日行程开始，每一天独立成段；
- “行前准备”和“注意事项”作为最后两个标题；
- 请确保语言礼貌友好，方便用户参考直接发送。

请生成完整的旅行摘要：
"""
        self.prompt_travel = ChatPromptTemplate.from_template(self.travel_template)
        self.prompt_food = ChatPromptTemplate.from_template(self.food_template)
        self.prompt_accommodation = ChatPromptTemplate.from_template(self.accommodation_template)
        self.prompt_summary = ChatPromptTemplate.from_template(self.summary)

    def initialize(self):
        self.chain_travel = self.prompt_travel | self.model
        self.chain_food = self.prompt_food | self.model
        self.chain_accommodation = self.prompt_accommodation | self.model
        self.chain_summary = self.prompt_summary | self.model

    def invoke(self, category: str, data: Dict):
        if category == "travel":
            return self.chain_travel.invoke(data)
        elif category == "food":
            return self.chain_food.invoke(data)
        elif category == "accommodation":
            return self.chain_accommodation.invoke(data)
        elif category == "summary":
            return self.chain_summary.invoke(data)
        else:
            return "无效类别，请选择 'travel'、'food' 或 'accommodation'。"

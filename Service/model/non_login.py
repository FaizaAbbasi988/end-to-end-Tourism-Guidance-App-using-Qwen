# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM
# from typing import Dict

# class NonLogin():
#     def __init__(self):
#         self.start_model()
#         self.prompts()
#         self.initialize()
#     def start_model(self):
#         self.model = OllamaLLM(model="qwen2.5:3b", base_url = "http://localhost:11434")
#     def prompts(self):
#         self.best_route = """
#             你是太原市的旅游助手，用户想了解{place}的{info}信息。

#             请按照以下要求生成回答：
#             - 如果用户询问的是“最佳路线”或“游览顺序”，请推荐一个合理的游览线路。
#             - 使用“→”符号连接各个景点，展示清晰的游览顺序。
#             - 路线应尽量连贯，反映出地理位置或文化逻辑上的合理性。
#             - 不要添加多余的解释或段落，只输出路线内容本身。

#             示例输出格式（仅供参考）：
#             晋祠南门牌坊 → 飞龙阁 → 龙亭照壁图壁 → 水镜台 → 航取 → 品道讲堂 → 圣母殿...

#             请根据{place}实际情况生成类似的路线内容。

#             回答：
#             """
#         self.Traffic_information = """
#             你是太原市的旅游助手，负责根据用户的问题提供专业且详细的指导。
#             用户想了解关于{place}的{info}信息。

#             请严格按照以下格式和内容要求进行回答，并使用中文输出：

#             1. 回答必须分为以下三个固定部分，且顺序一致：
#             - 公交线路信息
#             - 自驾信息
#             - 其他信息

#             2. 每个部分需包含以下具体内容（如有）：

#             【公交线路信息】
#             - 公交线路编号（例如：10路、308路等）
#             - 起点与终点名称
#             - 主要经过站点
#             - 首末班车时间（注明夏季和冬季时间）
#             - 全程票价（注明票价金额及是否单一票制）

#             【自驾信息】
#             - 推荐行车路线（起点→目的地，注明主干道名称）
#             - 预计行驶时间（例如：30–45分钟）
#             - 停车场位置（距离景点多少米）
#             - 停车容量（可容纳多少车辆）
#             - 收费标准（按次或按天，并写金额）

#             【其他信息】
#             - 是否免费开放、特别活动或展览说明
#             - 周边推荐景点或设施（如公园、餐厅）
#             - 建议事项或出行提示

#             3. 如果某部分没有相关信息，请明确写出“暂无相关信息”。

#             4. 内容需简明、客观、格式统一，使用项目符号“–”列出每条内容。

#             回答：
#             """
#         self.template_culinary_specialities = """
#             你是太原市的旅游助手，负责根据用户的问题提供专业且详细的指导。
#             用户想了解关于{place}的{info}信息。

#             请根据以下要求作答：
#             - 使用清晰的项目符号格式组织内容
#             - 答案应包含菜系的详细信息，且不应包含其他无关信息。具体说明
#             - 回答应简洁明了，信息完整，格式统一

#             回答：
#             """

#         self.cultural_introduction = """
#             你是太原市的旅游助手，负责根据用户的问题提供指导。
#             用户想了解关于{place}的{info}信息。
#             你的回答应当简明且具有专业性。
#             回答：
#             """
#         self.Sightseeing_tours = """
#             你是太原市的旅游助手，负责根据用户的问题提供指导。
#             用户想了解关于{place}的{info}信息。
#             你的回答应当简明且具有专业性。
#             你的回答应该涵盖所问地点的所有重要细节
#             回答：
#             """
#         self.prompt_best_route = ChatPromptTemplate.from_template(self.best_route)
#         self.prompt_Traffic_information = ChatPromptTemplate.from_template(self.Traffic_information)
#         self.prompt_culinary_specialities = ChatPromptTemplate.from_template(self.template_culinary_specialities)
#         self.prompt_cultural_introduction = ChatPromptTemplate.from_template(self.cultural_introduction)
#         self.prompt_Sightseeing_tours = ChatPromptTemplate.from_template(self.Sightseeing_tours)

#     def initialize(self):
#         self.chain_cultural_introduction = self.prompt_cultural_introduction | self.model
#         self.chain_best_route = self.prompt_best_route | self.model
#         self.chain_prompt_Sightseeing_tours = self.prompt_Sightseeing_tours | self.model
#         self.chain_culinary_specialities = self.prompt_culinary_specialities | self.model
#         self.chain_Traffic_information = self.prompt_Traffic_information | self.model
#     def invoke(self, place, info):
#         if info == "文化介绍":
#             return self.chain_cultural_introduction.invoke({"info": info, "place": place})
#         elif info == "最佳路线":
#             return self.chain_best_route.invoke({"info": info, "place": place})
#         elif info == "景点游览":
#             return self.chain_prompt_Sightseeing_tours.invoke({"info": info, "place": place})
#         elif info == "特色美食":
#             return self.chain_culinary_specialities.invoke({"info": info, "place": place})
#         elif info == "交通信息":
#             return self.chain_Traffic_information.invoke({"info": info, "place": place})
#         else:
#             return self.chain_cultural_introduction.invoke({"info": info, "place": place})
"""Login audio intent extraction; shared ASR and preprocessing utilities."""
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from Service.config import (
    QWEN_SPEECH_MODEL,
    QWEN_SPEECH_BASE_URL,
    TRAVEL_PARSE_PROMPT,
    FOOD_PARSE_PROMPT,
    ACCOMMODATION_PARSE_PROMPT,
    SUMMARY_PARSE_PROMPT,
)
from Service.model.audio_utils import preprocess_audio
from Service.model.speech_model import SpeechRecognitionModel, get_speech_recognition_model


class LoginSpeechAnswer:
    def __init__(self):
        self._start_model()
        self._load_prompts()
        self._initialize_chains()

    def _start_model(self):
        self.model = OllamaLLM(
            model=QWEN_SPEECH_MODEL,
            base_url=QWEN_SPEECH_BASE_URL
        )

    def _load_prompts(self):
        self.prompt_travel = ChatPromptTemplate.from_template(TRAVEL_PARSE_PROMPT)
        self.prompt_food = ChatPromptTemplate.from_template(FOOD_PARSE_PROMPT)
        self.prompt_accommodation = ChatPromptTemplate.from_template(ACCOMMODATION_PARSE_PROMPT)
        self.prompt_summary = ChatPromptTemplate.from_template(SUMMARY_PARSE_PROMPT)

    def _initialize_chains(self):
        self.chain_travel = self.prompt_travel | self.model
        self.chain_food = self.prompt_food | self.model
        self.chain_accommodation = self.prompt_accommodation | self.model
        self.chain_summary = self.prompt_summary | self.model

    def invoke(self, category: str, input_data: Dict):
        """
        Invoke the appropriate LLM chain based on category.
        :param category: One of "travel", "food", "accommodation", "summary"
        :param input_data: Dictionary with key 'question' or relevant prompt input
        :return: JSON-like structured dict
        """
        try:
            if category == "travel":
                return self.chain_travel.invoke(input_data)
            elif category == "food":
                return self.chain_food.invoke(input_data)
            elif category == "accommodation":
                return self.chain_accommodation.invoke(input_data)
            elif category == "summary":
                return self.chain_summary.invoke(input_data)
            else:
                return {"错误": "无效类别，请选择 'travel'、'food'、'accommodation' 或 'summary'。"}
        except Exception as e:
            return {"错误": f"模型调用失败: {str(e)}"}

"""Extract travel information from a transcribed audio question."""
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
# Older code may import these helpers from this module.
from Service.model.audio_utils import preprocess_audio
from Service.model.speech_model import SpeechRecognitionModel, get_speech_recognition_model


class LoginSpeechAnswer:
    def __init__(self):
        model = OllamaLLM(
            model=QWEN_SPEECH_MODEL,
            base_url=QWEN_SPEECH_BASE_URL,
        )
        # Each category needs a different prompt, but they share the same model.
        prompts = {
            "travel": TRAVEL_PARSE_PROMPT,
            "food": FOOD_PARSE_PROMPT,
            "accommodation": ACCOMMODATION_PARSE_PROMPT,
            "summary": SUMMARY_PARSE_PROMPT,
        }
        self.chains = {
            name: ChatPromptTemplate.from_template(prompt) | model
            for name, prompt in prompts.items()
        }

    def invoke(self, category: str, input_data: Dict):
        """Run the requested extraction prompt with the transcribed question."""
        if category not in self.chains:
            return {"错误": "无效类别，请选择 'travel'、'food'、'accommodation' 或 'summary'。"}
        try:
            return self.chains[category].invoke(input_data)
        except Exception as exc:
            return {"错误": f"模型调用失败: {exc}"}

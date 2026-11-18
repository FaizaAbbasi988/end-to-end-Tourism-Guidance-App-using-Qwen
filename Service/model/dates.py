"""Date extraction LLM; audio preprocessing/ASR are shared elsewhere."""
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from Service.config import SPEECH_PROMPT, QWEN_SPEECH_MODEL, QWEN_SPEECH_BASE_URL
# Preserve old imports for callers while keeping one actual implementation.
from Service.model.audio_utils import preprocess_audio
from Service.model.speech_model import SpeechRecognitionModel, get_speech_recognition_model


class NonLoginSpeechAnswer:
    def __init__(self):
        model = OllamaLLM(model=QWEN_SPEECH_MODEL, base_url=QWEN_SPEECH_BASE_URL)
        self.chain = ChatPromptTemplate.from_template(SPEECH_PROMPT) | model

    def invoke(self, text_input: str):
        response = self.chain.invoke({"question": text_input})
        if not isinstance(response, str):
            return {"到达时间": None, "离开时间": None, "original_text": text_input}
        arrival = re.search(r"到达[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)", response)
        departure = re.search(r"离开[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)", response)
        return {
            "到达时间": arrival.group(1) if arrival else None,
            "离开时间": departure.group(1) if departure else None,
            "original_text": text_input,
        }

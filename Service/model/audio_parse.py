from typing import Dict
import re
import os
import io
import re
import numpy as np
import soundfile as sf
import librosa
from funasr import AutoModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from Service.config import (
    QWEN_SPEECH_MODEL, QWEN_SPEECH_BASE_URL,
    TRAVEL_PARSE_PROMPT, FOOD_PARSE_PROMPT, ACCOMMODATION_PARSE_PROMPT, 
     SUMMARY_PARSE_PROMPT, SPEECH_PROMPT, 
    MODELS_DIR, MAIN_MODEL, VAD_MODEL, 
    PUNC_MODEL, GEN_PARAMS, QWEN_SPEECH_MODEL, QWEN_SPEECH_BASE_URL
)

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

class SpeechRecognitionModel:
    def __init__(self):
        self.model = AutoModel(
            model=os.path.join(MODELS_DIR, MAIN_MODEL["name"]),
            model_revision=MAIN_MODEL["revision"],
            vad_model=os.path.join(MODELS_DIR, VAD_MODEL["name"]),
            vad_model_revision=VAD_MODEL["revision"],
            punc_model=os.path.join(MODELS_DIR, PUNC_MODEL["name"]),
            punc_model_revision=PUNC_MODEL["revision"]
        )

    def transcribe(self, audio_data):
        res = self.model.generate(input=audio_data, cache={}, **GEN_PARAMS)
        return res[0]["text"] if res else ""

def preprocess_audio(audio_bytes):
    buffer = io.BytesIO(audio_bytes)
    audio, sr = sf.read(buffer)
    if len(audio.shape) == 2:
        audio = np.mean(audio, axis=1)
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sr = 16000
    out_buffer = io.BytesIO()
    sf.write(out_buffer, audio, sr, format='WAV')
    return out_buffer.getvalue()
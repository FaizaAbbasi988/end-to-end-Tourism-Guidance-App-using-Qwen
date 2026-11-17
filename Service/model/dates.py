import os
import io
import re
import numpy as np
import soundfile as sf
import librosa
from funasr import AutoModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from Service.config import SPEECH_PROMPT, MODELS_DIR, MAIN_MODEL, VAD_MODEL, PUNC_MODEL, GEN_PARAMS, QWEN_SPEECH_MODEL, QWEN_SPEECH_BASE_URL

class NonLoginSpeechAnswer:
    def __init__(self):
        self.model = OllamaLLM(
            model=QWEN_SPEECH_MODEL,
            base_url=QWEN_SPEECH_BASE_URL
        )
        self.prompt = ChatPromptTemplate.from_template(SPEECH_PROMPT)
        self.chain = self.prompt | self.model

    def invoke(self, text_input: str):
        response = self.chain.invoke({"question": text_input})
        if not isinstance(response, str):
            return {"到达时间": None, "离开时间": None, "original_text": text_input}

        arrival = re.search(r"到达[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)", response)
        departure = re.search(r"离开[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)", response)
        return {
            "到达时间": arrival.group(1) if arrival else None,
            "离开时间": departure.group(1) if departure else None,
            "original_text": text_input
        }

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

"""Single FunASR model implementation shared by all speech endpoints.

get_speech_recognition_model() loads a single instance on first use, instead
of loading separate models while importing API router modules.
"""
import os
from functools import lru_cache

from Service.config import (
    MODELS_DIR,
    MAIN_MODEL,
    VAD_MODEL,
    PUNC_MODEL,
    GEN_PARAMS,
)


class SpeechRecognitionModel:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        # Delayed import keeps module imports and test discovery lightweight.
        from funasr import AutoModel

        self.model = AutoModel(
            model=os.path.join(MODELS_DIR, MAIN_MODEL["name"]),
            model_revision=MAIN_MODEL["revision"],
            vad_model=os.path.join(MODELS_DIR, VAD_MODEL["name"]),
            vad_model_revision=VAD_MODEL["revision"],
            punc_model=os.path.join(MODELS_DIR, PUNC_MODEL["name"]),
            punc_model_revision=PUNC_MODEL["revision"],
        )

    def transcribe(self, audio_data):
        result = self.model.generate(input=audio_data, cache={}, **GEN_PARAMS)
        return result[0]["text"] if result else ""


@lru_cache(maxsize=1)
def get_speech_recognition_model() -> SpeechRecognitionModel:
    """Reuse the same loaded FunASR instance across audio endpoints."""
    return SpeechRecognitionModel()

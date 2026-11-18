"""Non-login AI handlers with lazy, shared model dependencies."""
import base64
from functools import lru_cache

from Service.model.non_login import NonLogin
from Service.model.text_to_speech import TTS
from Service.model.speech_model import get_speech_recognition_model
from Service.model.audio_utils import preprocess_audio
from Service.model.non_login_speech_answer import NonLoginSpeechAnswer
from Service.common.non_login_audio_chatbot_response import NonLoginAudioChatbotResponse
from Service.common.non_login_chatbot_response import NonLoginChatBotResponse


@lru_cache(maxsize=1)
def get_non_login_model():
    return NonLogin()


@lru_cache(maxsize=1)
def get_non_login_speech_answer():
    return NonLoginSpeechAnswer()


@lru_cache(maxsize=1)
def get_text_to_speech():
    return TTS()



def non_login_chatbot(place: str, info: str):
    answer = get_non_login_model().invoke(place, info)
    if info not in ("文化介绍", "特色美食"):
        return NonLoginChatBotResponse(response=answer)

    speech_answer, full_path = get_text_to_speech().text_to_speech_and_show_bytes(answer)
    return NonLoginChatBotResponse(
        response=answer, audio=speech_answer, full_path=str(full_path)
    )


def non_audio_chatbot(content: bytes) -> NonLoginAudioChatbotResponse:
    audio_bytes = preprocess_audio(content)
    question = get_speech_recognition_model().transcribe(audio_bytes)
    answer = get_non_login_speech_answer().invoke(question)
    if "文化介绍" in answer or "最佳路线" in answer:
        speech_answer, full_path = get_text_to_speech().text_to_speech_and_show_bytes(answer)
        return NonLoginAudioChatbotResponse(
            question=question, answer=answer, audio=speech_answer,
            audio_path=str(full_path),
        )
    return NonLoginAudioChatbotResponse(question=question, answer=answer)


def mp3_to_base64_and_play(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")
    except Exception as exc:
        print(f"Error processing audio: {exc}")
        return None

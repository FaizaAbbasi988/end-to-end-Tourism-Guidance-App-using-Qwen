
import io
import soundfile as sf
import numpy as np
import librosa 

from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Form, HTTPException
from Service.model.non_login import NonLogin
from Service.common.http.transcription_request import TranscriptionRequest
from Service.common.http.transcription_response import TranscriptionResponse
from Service.model.speech_model import SpeechRecognitionModel
from Service.common.http.chatbot_request import ChatbotRequest
from Service.common.http.chatbot_response import ChatbotResponse
from Service.model.non_login_speech_answer import NonLoginSpeechAnswer
from Service.model_service.non_login_chatbot import non_login_chatbot
from Service.model_service.non_login_chatbot import non_audio_chatbot, mp3_to_base64_and_play

from pydantic import BaseModel


class AudioPath(BaseModel):
    audio_path: str

non_login_model = NonLogin()
speech_model = SpeechRecognitionModel()
non_login_speech_answer = NonLoginSpeechAnswer()

router = APIRouter(
    prefix = "/non-login",
    tags = ["non-login"]
)
@router.post("/chatbot", response_model = ChatbotResponse)
async def non_login(parameters: ChatbotRequest):
    place = parameters.place
    info  = parameters.info
    chatbot_answer = non_login_chatbot(place, info)
    return ChatbotResponse(answer = chatbot_answer.response,audio_path = chatbot_answer.full_path ,audio_response = chatbot_answer.audio ,success = True)     
@router.post("/audio_chatbot", response_model=TranscriptionResponse)
async def audio_chatbot(
    file: UploadFile,
):
    try:
        content = await file.read()
        result = non_audio_chatbot(content)
        return TranscriptionResponse(
                question = result.question,
                audio_path = result.audio_path,
                answer = result.answer,
                audio = result.audio,
                success = True
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing input: {str(e)}"
        )
@router.post("/audio_path")
async def file_request(path: AudioPath):
    try:
        audio_bytes = mp3_to_base64_and_play(path.audio_path)
        return {"audio_base64": audio_bytes}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Audio file not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio: {str(e)}"
        )

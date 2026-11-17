"""Non-login HTTP endpoints; model services are loaded on first use."""
from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import BaseModel

from Service.common.http.transcription_response import TranscriptionResponse
from Service.common.http.chatbot_request import ChatbotRequest
from Service.common.http.chatbot_response import ChatbotResponse
from Service.model_service.non_login_chatbot import (
    non_login_chatbot,
    non_audio_chatbot,
    mp3_to_base64_and_play,
)


class AudioPath(BaseModel):
    audio_path: str


router = APIRouter(prefix="/non-login", tags=["non-login"])


@router.post("/chatbot", response_model=ChatbotResponse)
async def non_login(parameters: ChatbotRequest):
    result = non_login_chatbot(parameters.place, parameters.info)
    return ChatbotResponse(
        answer=result.response, audio_path=result.full_path,
        audio_response=result.audio, success=True,
    )


@router.post("/audio_chatbot", response_model=TranscriptionResponse)
async def audio_chatbot(file: UploadFile):
    try:
        content = await file.read()
        result = non_audio_chatbot(content)
        return TranscriptionResponse(
            question=result.question,
            audio_path=result.audio_path,
            answer=result.answer,
            audio=result.audio,
            success=True,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error processing input: {exc}") from exc


@router.post("/audio_path")
async def file_request(path: AudioPath):
    try:
        audio_bytes = mp3_to_base64_and_play(path.audio_path)
        return {"audio_base64": audio_bytes}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Audio file not found") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {exc}") from exc

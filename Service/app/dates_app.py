"""Extract arrival and departure dates from uploaded speech."""
import logging
from functools import lru_cache

from fastapi import APIRouter, File, HTTPException, UploadFile

from Service.common.http.dates_response import ChineseDateResponse
from Service.model.audio_utils import preprocess_audio
from Service.model.dates import NonLoginSpeechAnswer
from Service.model.speech_model import get_speech_recognition_model

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/dates", tags=["dates"])


@lru_cache(maxsize=1)
def get_date_extractor():
    return NonLoginSpeechAnswer()


@router.post("/extract_dates", response_model=ChineseDateResponse)
async def process_audio(file: UploadFile = File(...)):
    try:
        content = await file.read()
        processed_audio = preprocess_audio(content)
        transcription = get_speech_recognition_model().transcribe(processed_audio)
        answer = get_date_extractor().invoke(transcription)
        # Keep the existing Chinese field names for API compatibility.
        return {
            "到达时间": answer["到达时间"],
            "离开时间": answer["离开时间"],
        }
    except Exception as exc:
        logger.exception("Failed to extract dates")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {exc}",
        ) from exc

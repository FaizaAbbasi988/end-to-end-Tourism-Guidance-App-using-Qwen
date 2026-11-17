from fastapi import UploadFile, File, HTTPException
from functools import lru_cache
from Service.model.dates import NonLoginSpeechAnswer
from Service.model.audio_utils import preprocess_audio
from Service.model.speech_model import get_speech_recognition_model
from fastapi import APIRouter
from Service.common.http.dates_response import ChineseDateResponse  # ✅ import your new response model
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/dates", tags=["dates"])
speech_model = SpeechRecognitionModel()
extractor = NonLoginSpeechAnswer()

@router.post("/extract_dates", response_model=ChineseDateResponse)
async def process_audio(file: UploadFile = File(...)):
    try:
        content = await file.read()
        logger.info(f"Received audio file: {file.filename} size: {len(content)} bytes")

        processed_audio = preprocess_audio(content)
        transcription = get_speech_recognition_model().transcribe(processed_audio)
        logger.info(f"Transcription: {transcription}")

        answer = get_date_extractor().invoke(transcription)
        logger.info(f"Extracted times: {answer}")

        #  Return only the required Chinese fields
        return {
            "到达时间": answer["到达时间"],
            "离开时间": answer["离开时间"]
        }

    except Exception as e:
        logger.error(f"Failed to process audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

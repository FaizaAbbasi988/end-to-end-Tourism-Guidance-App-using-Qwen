"""Audio requests that extract travel, food, hotel, and summary parameters."""
import json
import logging
from functools import lru_cache

from fastapi import APIRouter, File, HTTPException, UploadFile

from Service.common.http.parse_response import ParseResponse
from Service.model.audio_parse import LoginSpeechAnswer
from Service.model.audio_utils import preprocess_audio
from Service.model.speech_model import get_speech_recognition_model

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/audiologin", tags=["audiologin"])


@lru_cache(maxsize=1)
def get_login_audio_extractor():
    """Create the Qwen extractor only when an audio endpoint is called."""
    return LoginSpeechAnswer()


def parse_model_response(response):
    """Accept a JSON object or a list of strings from the extraction model."""
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError("Qwen did not return valid JSON") from exc

    if isinstance(response, dict):
        if "错误" in response:
            raise ValueError(str(response["错误"]))
        return response

    if isinstance(response, list) and all(isinstance(item, str) for item in response):
        return response

    raise ValueError("Qwen must return a JSON object or a list of strings")


def run_pipeline(file: UploadFile) -> str:
    """Read the audio, convert it to WAV, and transcribe it."""
    try:
        content = file.file.read()
        processed_audio = preprocess_audio(content)
        return get_speech_recognition_model().transcribe(processed_audio)
    except Exception as exc:
        logger.exception("Audio transcription failed")
        raise HTTPException(status_code=500, detail="音频处理失败") from exc


def build_endpoint(route_type: str):
    """Register one API for each kind of information to extract."""
    @router.post(f"/{route_type}", response_model=ParseResponse)
    async def handler(file: UploadFile = File(...)):
        try:
            transcription = run_pipeline(file)
            raw_answer = get_login_audio_extractor().invoke(
                route_type, {"question": transcription}
            )
            answer = parse_model_response(raw_answer)
            return ParseResponse(answer=answer, success=True)
        except Exception as exc:
            logger.exception("%s audio parsing failed", route_type)
            return ParseResponse(answer=str(exc), success=False)
    return handler


travel_from_audio = build_endpoint("travel")
food_from_audio = build_endpoint("food")
accommodation_from_audio = build_endpoint("accommodation")
summary_from_audio = build_endpoint("summary")

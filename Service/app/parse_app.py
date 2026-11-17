from fastapi import UploadFile, File, HTTPException, APIRouter
from Service.model.audio_parse import SpeechRecognitionModel, LoginSpeechAnswer, preprocess_audio
from Service.common.http.parse_response import ParseResponse
import logging
import json
from typing import Union

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/audiologin", tags=["audiologin"])

# Initialize models
speech_model = SpeechRecognitionModel()
extractor = LoginSpeechAnswer()

def run_pipeline(file: UploadFile) -> str:
    """Handle audio preprocessing and transcription."""
    try:
        content = file.file.read()
        logger.info(f"Received audio file: {file.filename}, size: {len(content)} bytes")

        processed_audio = preprocess_audio(content)
        transcription = speech_model.transcribe(processed_audio)
        logger.info(f"Transcription: {transcription}")
        return transcription
    except Exception as e:
        logger.error(f"Audio processing/transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail="音频处理失败")

def safe_parse_model_response(response) -> Union[str, list[str]]:
    """Ensure the model's output is either string or list[str] as required by BaseResponse."""
    if isinstance(response, dict):
        return json.dumps(response, ensure_ascii=False)
    elif isinstance(response, str):
        # Try to parse as JSON, if valid and a list of strings, return it as list
        try:
            parsed = json.loads(response)
            if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
                return parsed
            elif isinstance(parsed, dict):
                return json.dumps(parsed, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        return response
    elif isinstance(response, list):
        return [str(item) for item in response]
    return str(response)

# Endpoint Template
def build_endpoint(route_type: str):
    @router.post(f"/{route_type}", response_model=ParseResponse)
    async def handler(file: UploadFile = File(...)):
        try:
            transcription = run_pipeline(file)
            response = extractor.invoke(route_type, {"question": transcription})
            parsed = safe_parse_model_response(response) if isinstance(response, dict) else json.loads(response)
            return ParseResponse(answer=parsed, success=True)
        except Exception as e:
            logger.exception(f"{route_type.capitalize()} audio processing failed")
            return ParseResponse(answer=str(e), success=False)
    return handler

# Register endpoints dynamically
travel_from_audio = build_endpoint("travel")
food_from_audio = build_endpoint("food")
accommodation_from_audio = build_endpoint("accommodation")
summary_from_audio = build_endpoint("summary")

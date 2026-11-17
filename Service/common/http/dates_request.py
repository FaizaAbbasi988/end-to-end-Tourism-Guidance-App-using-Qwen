from pydantic import BaseModel
from typing import Optional, Dict
from Service.common.http.dates_response import TimeExtractionResponse

class NonLoginAudioChatbotRequest(BaseModel):
    audio: bytes

class NonLoginAudioChatbotResponse(BaseModel):
    question: str
    answer: TimeExtractionResponse
    audio: str 

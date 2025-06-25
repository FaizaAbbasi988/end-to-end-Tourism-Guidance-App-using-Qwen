from pydantic import BaseModel
from typing import Optional

class NonLoginAudioChatbotResponse(BaseModel):
    question: str
    answer: str
    audio: Optional[str] = None
    audio_path: Optional[str] = None
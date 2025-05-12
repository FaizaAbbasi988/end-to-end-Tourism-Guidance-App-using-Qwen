from pydantic import BaseModel
from typing import Optional

class ChatbotResponse(BaseModel):
    answer:str
    audio_response: Optional[str] = None
    success: bool
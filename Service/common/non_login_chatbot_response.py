from pydantic import BaseModel
from typing import Optional

class NonLoginChatBotResponse(BaseModel):
    response: str
    audio: Optional[str] = None
    full_path: Optional[str] = None
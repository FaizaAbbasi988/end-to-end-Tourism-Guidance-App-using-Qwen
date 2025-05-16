from pydantic import BaseModel
from typing import Optional

class TranscriptionResponse(BaseModel):
    question: str  # The original transcribed text
    answer: str    # The response from the insurance model
    audio : Optional[str] = None
    success: bool
    message: str = ""
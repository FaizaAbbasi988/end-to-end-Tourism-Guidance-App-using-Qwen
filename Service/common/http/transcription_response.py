from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    question: str  # The original transcribed text
    answer: str    # The response from the insurance model
    success: bool
    message: str = ""
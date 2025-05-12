from pydantic import BaseModel

class ChatbotRequest(BaseModel):
    place: str
    info:str

from pydantic import BaseModel

class BaseResponse(BaseModel):
    answer: str
    success: bool

from pydantic import BaseModel
from typing import Union

class BaseResponse(BaseModel):
    answer: Union[str, list[str]]
    success: bool

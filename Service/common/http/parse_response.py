from typing import Union
from pydantic import BaseModel

class ParseResponse(BaseModel):
    answer: Union[str, list[str], dict]  # Add dict support here
    success: bool

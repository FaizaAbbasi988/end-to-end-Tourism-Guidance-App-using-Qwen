"""Travel/food return string lists; other login APIs return text strings."""
from typing import Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    answer: Union[str, list[str]]
    success: bool

"""Audio parameter extraction may return a JSON object, a list, or an error string."""
from typing import Union

from pydantic import BaseModel


class ParseResponse(BaseModel):
    answer: Union[str, list[str], dict]
    success: bool

"""Response schema for extracted Chinese arrival and departure dates."""
from typing import Optional

from pydantic import BaseModel, Field


class ChineseDateResponse(BaseModel):
    arrival: Optional[str] = Field(default=None, alias="到达时间")
    departure: Optional[str] = Field(default=None, alias="离开时间")

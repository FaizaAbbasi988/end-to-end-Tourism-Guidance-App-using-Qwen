from pydantic import BaseModel


class DescriptionRequest(BaseModel):
    destination: str

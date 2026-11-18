"""Generate a short description of a destination."""
from functools import lru_cache

from fastapi import APIRouter

from Service.common.http.description_request import DescriptionRequest
from Service.common.http.description_response import DescriptionResponse
from Service.model.description import Description

router = APIRouter(prefix="/description", tags=["description"])


@lru_cache(maxsize=1)
def get_description_model():
    """Create the Qwen client only when the description API is first used."""
    return Description()


@router.post("/text", response_model=DescriptionResponse)
async def description_endpoint(data: DescriptionRequest):
    try:
        answer = get_description_model().invoke(data.model_dump())
        return DescriptionResponse(answer=answer, success=True)
    except Exception as exc:
        return DescriptionResponse(answer=str(exc), success=False)

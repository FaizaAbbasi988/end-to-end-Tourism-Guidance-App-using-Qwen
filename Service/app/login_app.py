"""Logged-in AI endpoints. Travel/food already return list[str] from the AI model."""
from fastapi import APIRouter

from Service.common.http.travel_request import TravelRequest
from Service.common.http.base_response import BaseResponse
from Service.common.http.food_request import FoodRequest
from Service.common.http.accomodation_request import AccommodationRequest
from Service.common.http.summary_request import SummaryRequest
from Service.model_service.login_chatbot import (
    handle_travel,
    handle_food,
    handle_accommodation,
    handle_summary,
)

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/travel", response_model=BaseResponse)
async def travel_endpoint(data: TravelRequest):
    try:
        # The AI layer produces [intro, route1, route2, route3] directly.
        answer = handle_travel(data.model_dump())
        return BaseResponse(answer=answer, success=True)
    except Exception as exc:
        return BaseResponse(answer=str(exc), success=False)


@router.post("/food", response_model=BaseResponse)
async def food_endpoint(data: FoodRequest):
    try:
        # The AI layer produces [intro, three restaurants per requested meal].
        answer = handle_food(data.model_dump())
        return BaseResponse(answer=answer, success=True)
    except Exception as exc:
        return BaseResponse(answer=str(exc), success=False)


@router.post("/accommodation", response_model=BaseResponse)
async def accommodation_endpoint(data: AccommodationRequest):
    try:
        result = handle_accommodation(data.dict())
        return BaseResponse(answer=result, success=True)
    except Exception as exc:
        return BaseResponse(answer=str(exc), success=False)


@router.post("/summary", response_model=BaseResponse)
async def summary_endpoint(data: SummaryRequest):
    try:
        result = handle_summary(data.dict())
        return BaseResponse(answer=result, success=True)
    except Exception as exc:
        return BaseResponse(answer=str(exc), success=False)

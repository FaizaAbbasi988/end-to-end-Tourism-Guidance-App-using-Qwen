from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Form, HTTPException


from Service.model.login import Login
from Service.common.http.travel_request import TravelRequest
from Service.common.http.base_response import BaseResponse
from Service.common.http.food_request import FoodRequest
from Service.common.http.accomodation_request import AccommodationRequest
from Service.common.http.summary_request import SummaryRequest
from Service.model_service.login_chatbot import (
    handle_travel,
    handle_food,
    handle_accommodation,
    handle_summary
)

login_model = Login()

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

# ===== Endpoints =====
@router.post("/travel", response_model=BaseResponse)
async def travel_endpoint(data: TravelRequest):
    try:
        raw_result = handle_travel(data.dict())
        
        # Split the string on each 路线 marker
        segments = []
        for part in ["路线1", "路线2", "路线3"]:
            if part in raw_result:
                # ensure there's a delimiter before each marker
                raw_result = raw_result.replace(part, f"@@@{part}")
        
        # Split and remove empty segments
        parts = [seg.strip() for seg in raw_result.split("@@@") if seg.strip()]
        
        return BaseResponse(answer=parts, success=True)
    except Exception as e:
        return BaseResponse(answer=str(e), success=False)


@router.post("/food", response_model=BaseResponse)
async def food_endpoint(data: FoodRequest):
    try:
        raw_result = handle_food(data.dict())
        segments = []
        for part in ["餐厅 1", "餐厅 2", "餐厅 3"]:
            if part in raw_result:
                # ensure there's a delimiter before each marker
                raw_result = raw_result.replace(part, f"@@@{part}")
        
        # Split and remove empty segments
        parts = [seg.strip() for seg in raw_result.split("@@@") if seg.strip()]
        return BaseResponse(answer=parts, success=True)
    except Exception as e:
        return BaseResponse(answer=str(e), success=False)

@router.post("/accommodation", response_model=BaseResponse)
async def accommodation_endpoint(data: AccommodationRequest):
    try:
        result = handle_accommodation(data.dict())
        return BaseResponse(answer=result, success=True)
    except Exception as e:
        return BaseResponse(answer=str(e), success=False)

@router.post("/summary", response_model=BaseResponse)
async def summary_endpoint(data: SummaryRequest):
    try:
        result = handle_summary(data.dict())
        return BaseResponse(answer=result, success=True)
    except Exception as e:
        return BaseResponse(answer=str(e), success=False)
from pydantic import BaseModel
from typing import List

class TravelRequest(BaseModel):
    arrival_datetime: str
    departure_datetime: str
    traveler_ages: List[int]
    historical_culture_interests: List[str]
    folk_culture_interests: List[str]
    famous_humanistic_interests: List[str]
    red_culture_interests: List[str]
    food_interests: List[str]
    celebrity_culture_interests: List[str]
    interest_priority_order: List[str]
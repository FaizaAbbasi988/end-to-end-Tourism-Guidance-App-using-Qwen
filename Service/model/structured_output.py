"""Structured Qwen output contracts for the AI service.

Qwen generates structured content only. Python constructs the public list[str]
contract so the consumer can use answer[0], answer[1], ... directly.
"""
from typing import List

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RouteResult(StrictModel):
    routes: List[str] = Field(min_length=3, max_length=3)


class Restaurant(StrictModel):
    name: str
    cuisine: str
    price: str
    reason: str
    navigation: str


class MealGroup(StrictModel):
    meal_type: str
    restaurants: List[Restaurant] = Field(min_length=3, max_length=3)


class FoodResult(StrictModel):
    meals: List[MealGroup] = Field(min_length=1)


TRAVEL_INTRO = (
    "根据您的出行时间、兴趣偏好和同行人员的年龄，"
    "我们为您定制了三条山西旅行路线，请查阅并选择最适合您的行程："
)
FOOD_INTRO = "根据您选择的旅行路线和用餐偏好，我们为您推荐以下本地餐厅："


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()


def format_routes(raw: str) -> List[str]:
    """Parse Qwen JSON and return [intro, route1, route2, route3]."""
    try:
        result = RouteResult.model_validate_json(raw)
    except (ValidationError, ValueError, TypeError) as exc:
        raise ValueError("Invalid three-route response from Qwen") from exc
    routes = [_text(route, f"route {i}") for i, route in enumerate(result.routes, 1)]
    return [TRAVEL_INTRO] + [
        f"路线{i}：{route}" for i, route in enumerate(routes, 1)
    ]


def format_food(raw: str, meal_preferences: List[str]) -> List[str]:
    """Return [intro, 3 restaurant strings per meal], preserving meal order."""
    try:
        result = FoodResult.model_validate_json(raw)
    except (ValidationError, ValueError, TypeError) as exc:
        raise ValueError("Invalid food response from Qwen") from exc
    requested = [_text(meal, "meal preference") for meal in meal_preferences]
    if not requested or len(result.meals) != len(requested):
        raise ValueError("Expected one food group per requested meal")

    answer = [FOOD_INTRO]
    for meal, expected in zip(result.meals, requested):
        if _text(meal.meal_type, "meal type") != expected:
            raise ValueError("Meal groups must follow requested meal order")
        for index, restaurant in enumerate(meal.restaurants, 1):
            name = _text(restaurant.name, "restaurant name")
            cuisine = _text(restaurant.cuisine, "cuisine")
            price = _text(restaurant.price, "price")
            reason = _text(restaurant.reason, "reason")
            navigation = _text(restaurant.navigation, "navigation")
            answer.append(
                f"【{expected}】餐厅 {index}：\n"
                f"名称：{name}\n"
                f"菜系：{cuisine}\n"
                f"人均：{price}\n"
                f"推荐理由：{reason}\n"
                f"导航建议：{navigation}"
            )
    return answer

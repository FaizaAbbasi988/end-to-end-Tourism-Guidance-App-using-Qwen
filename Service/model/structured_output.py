"""Validate Qwen JSON and render the existing /login endpoint text protocol.

The FastAPI layer intentionally remains unchanged. Its splitting markers are
created here, never trusted to appear in the generated model content.
"""
import json
import re
from typing import List

from pydantic import BaseModel, ValidationError


class RouteResult(BaseModel):
    routes: List[str]


class Restaurant(BaseModel):
    name: str
    cuisine: str
    price: str
    reason: str
    navigation: str


class MealGroup(BaseModel):
    meal_type: str
    restaurants: List[Restaurant]


class FoodResult(BaseModel):
    meals: List[MealGroup]


# The backend uses literal .replace() on these labels. Never allow them inside
# free-form model fields, otherwise it will split a recommendation in two.
ROUTE_MARKERS = ("路线1", "路线2", "路线3")
FOOD_MARKERS = ("餐厅 1", "餐厅 2", "餐厅 3")
RESERVED = ROUTE_MARKERS + FOOD_MARKERS + ("@@@",)


def _clean(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    text = " ".join(value.split())
    if any(marker in text for marker in RESERVED):
        raise ValueError(f"{field} contains a reserved splitting marker")
    return text


def _load(raw: str):
    if not isinstance(raw, str):
        raise ValueError("Qwen response must be a JSON string")
    try:
        return json.loads(raw)
    except (ValueError, TypeError) as exc:
        raise ValueError("Qwen response is not valid JSON") from exc


def format_routes(raw: str) -> str:
    """Return a legacy string with exactly three canonical route markers."""
    try:
        result = RouteResult.parse_obj(_load(raw))
    except ValidationError as exc:
        raise ValueError("Invalid routes JSON schema") from exc
    if len(result.routes) != 3:
        raise ValueError("Qwen must return exactly three routes")
    routes = [_clean(route, f"route {i}") for i, route in enumerate(result.routes, 1)]
    intro = "根据您的出行时间、兴趣偏好和同行人员的年龄，我们为您定制了三条山西旅行路线，请查阅并选择最适合您的行程："
    return intro + "\n\n" + "\n\n".join(
        f"路线{i}：{route}" for i, route in enumerate(routes, 1)
    )


def format_food(raw: str, meal_preferences: List[str]) -> str:
    """Return legacy restaurant labels for each requested meal, in user order."""
    try:
        result = FoodResult.parse_obj(_load(raw))
    except ValidationError as exc:
        raise ValueError("Invalid restaurant JSON schema") from exc
    requested = [_clean(str(meal), "meal preference") for meal in meal_preferences]
    if not requested or len(result.meals) != len(requested):
        raise ValueError("Qwen must return one meal group per requested meal")
    blocks = ["根据您选择的旅行路线和用餐偏好，我们为您推荐以下本地餐厅："]
    for index, (group, expected) in enumerate(zip(result.meals, requested), 1):
        if _clean(group.meal_type, f"meal type {index}") != expected:
            raise ValueError("Meal groups must match requested meal preferences and order")
        if len(group.restaurants) != 3:
            raise ValueError("Qwen must return exactly three restaurants per meal")
        blocks.append(f"【{expected}】推荐：")
        for number, restaurant in enumerate(group.restaurants, 1):
            fields = [
                _clean(restaurant.name, "name"),
                _clean(restaurant.cuisine, "cuisine"),
                _clean(restaurant.price, "price"),
                _clean(restaurant.reason, "reason"),
                _clean(restaurant.navigation, "navigation"),
            ]
            blocks.append(
                f"餐厅 {number}：\n名称：{fields[0]}\n菜系：{fields[1]}\n"
                f"人均：{fields[2]}\n推荐理由：{fields[3]}\n导航建议：{fields[4]}"
            )
    return "\n\n".join(blocks)

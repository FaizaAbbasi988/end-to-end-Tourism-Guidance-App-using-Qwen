"""Qwen generation for the four logged-in tourism APIs.

Qwen returns schema-constrained JSON. Pydantic validates it, then Python
formats each result as an answer list so the backend never splits text.
"""
import logging
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from ollama import Client

from Service.config import (
    QWEN_MODEL_NAME,
    QWEN_BASE_URL,
    TRAVEL_PROMPT,
    FOOD_PROMPT,
    ACCOMMODATION_PROMPT,
    SUMMARY_PROMPT,
)
from Service.model.structured_output import (
    AccommodationResult,
    FoodResult,
    RouteResult,
    SummaryResult,
    format_accommodation,
    format_food,
    format_routes,
    format_summary,
)


logger = logging.getLogger(__name__)


class Login:
    def __init__(self):
        self.structured_client = Client(host=QWEN_BASE_URL)
        self.prompt_travel = ChatPromptTemplate.from_template(TRAVEL_PROMPT)
        self.prompt_food = ChatPromptTemplate.from_template(FOOD_PROMPT)
        self.prompt_accommodation = ChatPromptTemplate.from_template(ACCOMMODATION_PROMPT)
        self.prompt_summary = ChatPromptTemplate.from_template(SUMMARY_PROMPT)

    def _generate_validated(self, prompt: str, schema, formatter):
        """Retry up to three times if generated data does not match the schema."""
        last_error = None
        for attempt in range(3):
            retry_note = (
                ""
                if attempt == 0
                else "\n上一次结果未通过字段和数量验证。请严格按照JSON Schema重新生成。"
            )
            response = self.structured_client.generate(
                model=QWEN_MODEL_NAME,
                prompt=prompt + retry_note,
                format=schema.model_json_schema(),
                options={"temperature": 0},
                stream=False,
            )
            try:
                return formatter(response.response)
            except ValueError as exc:
                last_error = exc
                # Log the actual validation issue without changing the HTTP contract.
                # Exception chaining includes the original Pydantic field errors.
                logger.warning(
                    "Qwen structured-output validation failed (schema=%s, attempt=%d/3): %s",
                    schema.__name__, attempt + 1, exc, exc_info=True,
                )
        raise ValueError(
            f"Qwen failed structured-output validation after 3 attempts ({schema.__name__})"
        ) from last_error

    def invoke(self, category: str, data: Dict):
        if category == "travel":
            return self._generate_validated(
                self.prompt_travel.format(**data), RouteResult, format_routes
            )
        if category == "food":
            return self._generate_validated(
                self.prompt_food.format(**data),
                FoodResult,
                lambda raw: format_food(raw, data["meal_preferences"]),
            )
        if category == "accommodation":
            return self._generate_validated(
                self.prompt_accommodation.format(**data),
                AccommodationResult,
                format_accommodation,
            )
        if category == "summary":
            return self._generate_validated(
                self.prompt_summary.format(**data),
                SummaryResult,
                format_summary,
            )
        return "无效类别，请选择 'travel'、'food'、'accommodation' 或 'summary'。"

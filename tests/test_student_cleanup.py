"""Simple checks for the cleaned-up request models and audio extraction.

Run: python -m unittest discover -s tests -p "test_student_cleanup.py" -v
No Ollama or speech model is started.
"""
import unittest
from unittest.mock import Mock

from Service.common.http.food_request import FoodRequest
from Service.common.http.accomodation_request import AccommodationRequest
from Service.common.http.description_request import DescriptionRequest
from Service.common.http.base_response import BaseResponse
from Service.common.http.parse_response import ParseResponse
from Service.model.audio_parse import LoginSpeechAnswer


class StudentCleanupTests(unittest.TestCase):
    def test_food_request_fields_are_unchanged(self):
        request = FoodRequest(
            selected_route="晋祠",
            date="2026-12-01",
            distance_range="1-3公里",
            number_of_people=2,
            budget=150,
            meal_preferences=["午餐", "晚餐"],
        )
        self.assertEqual(request.model_dump()["meal_preferences"], ["午餐", "晚餐"])

    def test_accommodation_request_fields_are_unchanged(self):
        request = AccommodationRequest(
            selected_route="晋祠",
            date_of_stay="2026-12-01",
            accommodation_type="酒店",
            housing_type="双人间",
            stars=3,
            room_rate=500,
            total_people=2,
            adults=2,
            elderly=0,
            children=0,
            children_age=[],
            transportation_preference="出租车",
        )
        self.assertEqual(request.total_people, 2)

    def test_description_request_is_unchanged(self):
        self.assertEqual(DescriptionRequest(destination="平遥古城").destination, "平遥古城")

    def test_existing_response_types_still_work(self):
        self.assertEqual(BaseResponse(answer=["介绍", "路线1"], success=True).answer[1], "路线1")
        self.assertEqual(BaseResponse(answer="错误", success=False).answer, "错误")
        self.assertEqual(ParseResponse(answer={"目的地": "晋祠"}, success=True).answer["目的地"], "晋祠")

    def test_audio_extraction_selects_matching_prompt(self):
        # Bypass __init__ to avoid an actual Ollama connection.
        extractor = object.__new__(LoginSpeechAnswer)
        travel = Mock()
        food = Mock()
        travel.invoke.return_value = '{"目的地":"晋祠"}'
        food.invoke.return_value = '{"餐别":"午餐"}'
        extractor.chains = {"travel": travel, "food": food}
        result = extractor.invoke("food", {"question": "我要午餐"})
        self.assertEqual(result, '{"餐别":"午餐"}')
        food.invoke.assert_called_once_with({"question": "我要午餐"})
        travel.invoke.assert_not_called()

    def test_audio_extraction_handles_unsupported_category(self):
        extractor = object.__new__(LoginSpeechAnswer)
        extractor.chains = {}
        self.assertIn("错误", extractor.invoke("unknown", {"question": "test"}))

    def test_audio_extraction_handles_model_failure(self):
        extractor = object.__new__(LoginSpeechAnswer)
        chain = Mock()
        chain.invoke.side_effect = RuntimeError("model unavailable")
        extractor.chains = {"travel": chain}
        result = extractor.invoke("travel", {"question": "test"})
        self.assertIn("错误", result)
        self.assertIn("model unavailable", result["错误"])


if __name__ == "__main__":
    unittest.main()

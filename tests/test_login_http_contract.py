"""API contract tests: FastAPI layer returns list elements, not split text.

Run: python -m unittest discover -s tests -p "test_login_http_contract.py" -v
No live Qwen server is needed; the AI service handlers are mocked.
"""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

# Load the endpoint file without importing Service.app.__init__, which starts
# unrelated speech/audio services and expects the service startup PYTHONPATH.
# We only need the travel/food endpoint functions for contract testing.
endpoint_path = Path(__file__).resolve().parents[1] / "Service" / "app" / "login_app.py"
spec = importlib.util.spec_from_file_location("_login_endpoints_contract", endpoint_path)
login_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(login_app)
travel_endpoint = login_app.travel_endpoint
food_endpoint = login_app.food_endpoint
from Service.common.http.food_request import FoodRequest
from Service.common.http.travel_request import TravelRequest


TRAVEL_DATA = {
    "arrival_datetime": "2026-12-01",
    "departure_datetime": "2026-12-05",
    "traveler_ages": [25],
    "historical_culture_interests": ["晋祠"],
    "folk_culture_interests": [],
    "famous_humanistic_interests": [],
    "red_culture_interests": [],
    "food_interests": [],
    "celebrity_culture_interests": [],
    "interest_priority_order": [],
}
FOOD_DATA = {
    "selected_route": "晋祠",
    "date": "2026-12-02",
    "distance_range": "3公里",
    "number_of_people": 2,
    "budget": 100,
    "meal_preferences": ["午餐", "晚餐"],
}


class LoginApiContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_travel_preserves_exact_answer_list(self):
        elements = ["介绍", "路线1：甲，乙", "路线2：丙，丁", "路线3：戊，己"]
        with patch.object(login_app, "handle_travel", return_value=elements):
            response = await travel_endpoint(TravelRequest(**TRAVEL_DATA))
        self.assertTrue(response.success)
        self.assertEqual(response.answer, elements)

    async def test_food_preserves_seven_independent_elements(self):
        elements = ["介绍"] + [
            f"【{meal}】餐厅 {number}：\n名称：{meal}餐厅{number}"
            for meal in ("午餐", "晚餐") for number in range(1, 4)
        ]
        with patch.object(login_app, "handle_food", return_value=elements):
            response = await food_endpoint(FoodRequest(**FOOD_DATA))
        self.assertTrue(response.success)
        self.assertEqual(response.answer, elements)
        self.assertEqual(len(response.answer), 7)

    async def test_errors_are_not_reported_as_success(self):
        with patch.object(login_app, "handle_food", side_effect=ValueError("invalid meal")):
            response = await food_endpoint(FoodRequest(**FOOD_DATA))
        self.assertFalse(response.success)
        self.assertEqual(response.answer, "invalid meal")


if __name__ == "__main__":
    unittest.main()

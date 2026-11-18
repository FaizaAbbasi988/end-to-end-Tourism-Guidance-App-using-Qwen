"""Tests for the actual AI-service answer list contract (no live Ollama needed).

Run from repository root:
    python -m unittest discover -s tests -p "test_structured_output.py" -v
"""
import json
import unittest

from Service.model.structured_output import format_food, format_routes


def restaurant(name):
    return {
        "name": name,
        "cuisine": "山西菜",
        "price": "50 元",
        "reason": "有当地特色，环境舒适。",
        "navigation": "步行约五分钟。",
    }


class StructuredOutputTests(unittest.TestCase):
    def test_travel_returns_exactly_four_array_elements(self):
        raw = json.dumps({"routes": [
            "游览晋祠并参观博物馆。",
            "体验平遥的古城文化。",
            "参观五台山景点。",
        ]}, ensure_ascii=False)
        answer = format_routes(raw)
        self.assertIsInstance(answer, list)
        self.assertEqual(len(answer), 4)
        self.assertTrue(answer[0].startswith("根据您的出行时间"))
        for i in range(1, 4):
            self.assertTrue(answer[i].startswith(f"路线{i}："))

    def test_travel_rejects_wrong_count_malformed_json_and_blank_routes(self):
        for raw in (
            '{"routes":["one","two"]}',
            '{"routes":["one","two","three","four"]}',
            '{"routes":["one","","three"]}',
            'not JSON',
            '{"routes":["one","two","three"],"extra":"not allowed"}',
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                format_routes(raw)

    def test_travel_content_commas_do_not_split_recommendations(self):
        raw = json.dumps({"routes": ["晋祠，平遥古城", "云冈石窟，五台山", "乔家大院，王家大院"]}, ensure_ascii=False)
        answer = format_routes(raw)
        self.assertEqual(len(answer), 4)
        self.assertIn("晋祠，平遥古城", answer[1])

    def test_one_meal_returns_four_elements(self):
        raw = json.dumps({"meals": [
            {"meal_type": "午餐", "restaurants": [restaurant("甲"), restaurant("乙"), restaurant("丙")]}
        ]}, ensure_ascii=False)
        answer = format_food(raw, ["午餐"])
        self.assertEqual(len(answer), 4)
        self.assertTrue(answer[0].startswith("根据您选择的旅行路线"))
        self.assertTrue(answer[1].startswith("【午餐】餐厅 1："))
        self.assertTrue(answer[3].startswith("【午餐】餐厅 3："))
        self.assertIn("名称：甲", answer[1])

    def test_two_meals_return_seven_independent_elements(self):
        raw = json.dumps({"meals": [
            {"meal_type": "午餐", "restaurants": [restaurant("甲"), restaurant("乙"), restaurant("丙")]},
            {"meal_type": "晚餐", "restaurants": [restaurant("丁"), restaurant("戊"), restaurant("己")]},
        ]}, ensure_ascii=False)
        answer = format_food(raw, ["午餐", "晚餐"])
        self.assertEqual(len(answer), 7)
        self.assertTrue(answer[3].startswith("【午餐】餐厅 3："))
        self.assertNotIn("【晚餐】", answer[3])
        self.assertTrue(answer[4].startswith("【晚餐】餐厅 1："))
        self.assertTrue(answer[6].startswith("【晚餐】餐厅 3："))

    def test_rejects_missing_or_reordered_meals(self):
        raw = json.dumps({"meals": [
            {"meal_type": "晚餐", "restaurants": [restaurant("甲"), restaurant("乙"), restaurant("丙")]},
            {"meal_type": "午餐", "restaurants": [restaurant("丁"), restaurant("戊"), restaurant("己")]},
        ]}, ensure_ascii=False)
        with self.assertRaises(ValueError):
            format_food(raw, ["午餐", "晚餐"])
        with self.assertRaises(ValueError):
            format_food('{"meals":[]}', ["午餐"])

    def test_rejects_wrong_restaurant_count_and_missing_fields(self):
        raw = json.dumps({"meals": [{
            "meal_type": "午餐",
            "restaurants": [restaurant("甲"), restaurant("乙")],
        }]}, ensure_ascii=False)
        with self.assertRaises(ValueError):
            format_food(raw, ["午餐"])
        raw = json.dumps({"meals": [{
            "meal_type": "午餐",
            "restaurants": [{"name": "甲"}] * 3,
        }]}, ensure_ascii=False)
        with self.assertRaises(ValueError):
            format_food(raw, ["午餐"])

    def test_rejects_blank_restaurant_fields(self):
        r = restaurant("甲")
        r["navigation"] = "   "
        raw = json.dumps({"meals": [{
            "meal_type": "午餐",
            "restaurants": [r, restaurant("乙"), restaurant("丙")],
        }]}, ensure_ascii=False)
        with self.assertRaises(ValueError):
            format_food(raw, ["午餐"])


if __name__ == "__main__":
    unittest.main()

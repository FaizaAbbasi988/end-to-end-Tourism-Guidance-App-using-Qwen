"""Contract tests: the backend's existing literal split logic must keep working.

Run: python -m unittest discover -s tests -p "test_structured_output.py"
"""
import json
import unittest

from Service.model.structured_output import format_food, format_routes


def backend_split(text, markers):
    # Matches Service/app/login_app.py without changing its implementation.
    for marker in markers:
        if marker in text:
            text = text.replace(marker, "@@@" + marker)
    return [part.strip() for part in text.split("@@@") if part.strip()]


class StructuredOutputTests(unittest.TestCase):
    def test_travel_is_split_into_intro_and_three_routes(self):
        raw = json.dumps({"routes": [
            "游览晋祠并参观博物馆。",
            "体验平遥的古城文化。",
            "参观五台山景点。",
        ]}, ensure_ascii=False)
        result = backend_split(format_routes(raw), ["路线1", "路线2", "路线3"])
        self.assertEqual(len(result), 4)
        self.assertTrue(result[1].startswith("路线1："))
        self.assertTrue(result[2].startswith("路线2："))
        self.assertTrue(result[3].startswith("路线3："))

    def test_rejects_bad_counts_and_malformed_json(self):
        for raw in ['{"routes":["one","two"]}', "not JSON",
                    '{"routes":["one","","three"]}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                format_routes(raw)

    def test_rejects_embedded_backend_markers(self):
        with self.assertRaises(ValueError):
            format_routes(json.dumps({
                "routes": ["请看路线2", "a", "b"]
            }, ensure_ascii=False))

    def test_food_is_split_into_three_restaurants(self):
        restaurants = [
            {"name": "餐馆甲", "cuisine": "山西菜", "price": "30元",
             "reason": "传统风味", "navigation": "步行五分钟"},
            {"name": "餐馆乙", "cuisine": "面食", "price": "40元",
             "reason": "适合家庭", "navigation": "步行八分钟"},
            {"name": "餐馆丙", "cuisine": "小吃", "price": "20元",
             "reason": "本地特色", "navigation": "步行十分钟"},
        ]
        raw = json.dumps({"meals": [
            {"meal_type": "午餐", "restaurants": restaurants}
        ]}, ensure_ascii=False)
        parts = backend_split(format_food(raw, ["午餐"]),
                              ["餐厅 1", "餐厅 2", "餐厅 3"])
        self.assertEqual(len(parts), 4)
        self.assertTrue(parts[1].startswith("餐厅 1："))
        self.assertTrue(parts[3].startswith("餐厅 3："))

    def test_food_requires_all_requested_meals(self):
        raw = '{"meals":[]}'
        with self.assertRaises(ValueError):
            format_food(raw, ["早餐", "午餐"])

    def test_food_rejects_missing_fields(self):
        raw = json.dumps({"meals": [{
            "meal_type": "午餐",
            "restaurants": [{"name": "餐馆"}] * 3,
        }]}, ensure_ascii=False)
        with self.assertRaises(ValueError):
            format_food(raw, ["午餐"])


if __name__ == "__main__":
    unittest.main()

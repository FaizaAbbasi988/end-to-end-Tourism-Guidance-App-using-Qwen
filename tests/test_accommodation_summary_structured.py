"""Accommodation and summary structured response tests (no live Ollama needed)."""
import json
import unittest
from unittest.mock import Mock

from Service.model.login import Login
from Service.model.structured_output import format_accommodation, format_summary


def accommodation(name):
    return {
        "name": name,
        "location": "晋祠附近",
        "price": "350元",
        "facilities": "无线网络、早餐",
        "transport": "建议乘坐出租车",
        "reason": "符合用户预算",
    }


def accommodation_json():
    return json.dumps({
        "accommodations": [
            accommodation("甲酒店"),
            accommodation("乙酒店"),
            accommodation("丙酒店"),
        ]
    }, ensure_ascii=False)


def summary_json():
    return json.dumps({
        "itinerary": "第1天：晋祠。\n第2天：平遥古城。",
        "preparation": "身份证、舒适的鞋。",
        "safety": "注意出行安全，紧急电话120。",
    }, ensure_ascii=False)


class AccommodationAndSummaryTests(unittest.TestCase):
    def test_accommodation_returns_intro_and_three_options(self):
        answer = format_accommodation(accommodation_json())
        self.assertEqual(len(answer), 4)
        self.assertTrue(answer[1].startswith("住宿选项1："))
        self.assertIn("名称：甲酒店", answer[1])
        self.assertIn("交通建议：", answer[2])
        self.assertTrue(answer[3].startswith("住宿选项3："))

    def test_accommodation_rejects_invalid_data(self):
        for bad in (
            "not JSON",
            json.dumps({"accommodations": [accommodation("甲"), accommodation("乙")]}),
            json.dumps({"accommodations": [accommodation("甲")] * 4}),
            json.dumps({"accommodations": [{"name": "甲"}] * 3}),
            json.dumps({"accommodations": [
                {**accommodation("甲"), "price": "   "},
                accommodation("乙"), accommodation("丙"),
            ]}),
            json.dumps({"accommodations": [accommodation("甲")] * 3, "extra": "invalid"}),
        ):
            with self.subTest(raw=bad), self.assertRaises(ValueError):
                format_accommodation(bad)

    def test_summary_returns_four_independent_sections(self):
        answer = format_summary(summary_json())
        self.assertEqual(len(answer), 4)
        self.assertTrue(answer[1].startswith("每日行程："))
        self.assertIn("第2天：平遥古城", answer[1])
        self.assertTrue(answer[2].startswith("行前准备："))
        self.assertTrue(answer[3].startswith("重要事项及安全："))

    def test_summary_rejects_missing_blank_or_extra_fields(self):
        for bad in (
            "not JSON",
            '{"itinerary":"day 1","preparation":"bring shoes"}',
            '{"itinerary":"day 1","preparation":" ","safety":"careful"}',
            '{"itinerary":"day 1","preparation":"shoes","safety":"careful","extra":"bad"}',
        ):
            with self.subTest(raw=bad), self.assertRaises(ValueError):
                format_summary(bad)

    def test_accommodation_invokes_schema_constrained_ollama(self):
        model = object.__new__(Login)
        model.structured_client = Mock()
        model.structured_client.generate.return_value.response = accommodation_json()
        model.prompt_accommodation = Mock()
        model.prompt_accommodation.format.return_value = "accommodation prompt"
        answer = model.invoke("accommodation", {})
        self.assertEqual(len(answer), 4)
        call = model.structured_client.generate.call_args.kwargs
        self.assertIn("accommodations", call["format"]["properties"])
        self.assertEqual(call["options"], {"temperature": 0})

    def test_summary_invokes_schema_constrained_ollama(self):
        model = object.__new__(Login)
        model.structured_client = Mock()
        model.structured_client.generate.return_value.response = summary_json()
        model.prompt_summary = Mock()
        model.prompt_summary.format.return_value = "summary prompt"
        answer = model.invoke("summary", {})
        self.assertEqual(len(answer), 4)
        call = model.structured_client.generate.call_args.kwargs
        self.assertIn("itinerary", call["format"]["properties"])

    def test_invalid_model_response_retries_then_fails(self):
        model = object.__new__(Login)
        model.structured_client = Mock()
        model.structured_client.generate.return_value.response = '{"accommodations":[]}'
        model.prompt_accommodation = Mock()
        model.prompt_accommodation.format.return_value = "accommodation prompt"
        with self.assertRaises(ValueError):
            model.invoke("accommodation", {})
        self.assertEqual(model.structured_client.generate.call_count, 3)


if __name__ == "__main__":
    unittest.main()

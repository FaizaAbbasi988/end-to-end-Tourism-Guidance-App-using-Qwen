"""Tests for simple audio parser JSON handling.

Run from the repository root:
    python -m unittest discover -s tests -p "test_audio_parser.py" -v

These tests don't call Ollama or load FunASR.
"""
import unittest

from Service.app.parse_app import parse_model_response


class AudioParserTests(unittest.TestCase):
    def test_json_object(self):
        self.assertEqual(parse_model_response('{"目的地":"晋祠"}'), {"目的地": "晋祠"})

    def test_json_list(self):
        self.assertEqual(parse_model_response('["午餐","晚餐"]'), ["午餐", "晚餐"])

    def test_already_parsed_object(self):
        self.assertEqual(parse_model_response({"人数": 2}), {"人数": 2})

    def test_malformed_json(self):
        with self.assertRaises(ValueError):
            parse_model_response("This is not JSON")

    def test_reported_model_error(self):
        with self.assertRaises(ValueError):
            parse_model_response('{"错误":"模型调用失败"}')

    def test_invalid_array_items(self):
        with self.assertRaises(ValueError):
            parse_model_response('[1, 2, 3]')


if __name__ == "__main__":
    unittest.main()

"""Regression tests for the first speech-service cleanup.

Run: python -m unittest discover -s tests -p "test_speech_refactor.py" -v
No FunASR/Ollama model is loaded in these tests.
"""
import io
import unittest
from unittest.mock import patch

import numpy as np
import soundfile as sf

from Service.model import speech_model
from Service.model.audio_utils import preprocess_audio
from Service.common.http.dates_response import ChineseDateResponse


class SpeechRefactorTests(unittest.TestCase):
    def tearDown(self):
        speech_model.get_speech_recognition_model.cache_clear()

    def test_speech_recognizer_is_lazy_and_shared(self):
        speech_model.get_speech_recognition_model.cache_clear()
        with patch.object(speech_model, "SpeechRecognitionModel") as factory:
            first = speech_model.get_speech_recognition_model()
            second = speech_model.get_speech_recognition_model()
            self.assertIs(first, second)
            factory.assert_called_once_with()

    def test_audio_preprocess_produces_mono_16khz_wav(self):
        original = np.zeros((320, 2), dtype=np.float32)
        original[:, 0] = 0.2
        original[:, 1] = -0.2
        stream = io.BytesIO()
        sf.write(stream, original, 16000, format="WAV")
        converted = preprocess_audio(stream.getvalue())
        samples, sample_rate = sf.read(io.BytesIO(converted))
        self.assertEqual(sample_rate, 16000)
        self.assertEqual(samples.ndim, 1)
        self.assertEqual(len(samples), 320)

    def test_date_response_matches_actual_chinese_fields(self):
        response = ChineseDateResponse.model_validate({
            "到达时间": "2026年12月1日",
            "离开时间": "2026年12月5日",
        })
        self.assertEqual(response.model_dump(by_alias=True), {
            "到达时间": "2026年12月1日",
            "离开时间": "2026年12月5日",
        })


if __name__ == "__main__":
    unittest.main()

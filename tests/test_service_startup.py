"""Startup regression checks for registered routes and lazy speech imports.

Run: python -m unittest discover -s tests -p "test_service_startup.py" -v
This imports the app but does not invoke Qwen or speech recognition.
"""
import unittest

from Service.app import create_app, register_router
from Service.app.dates_app import get_date_extractor
from Service.app.parse_app import get_login_audio_extractor


class ServiceStartupTests(unittest.TestCase):
    def test_lazy_audio_factories_exist_and_start_uncalled(self):
        self.assertTrue(callable(get_date_extractor))
        self.assertTrue(callable(get_login_audio_extractor))
        self.assertEqual(get_date_extractor.cache_info().currsize, 0)
        self.assertEqual(get_login_audio_extractor.cache_info().currsize, 0)

    def test_app_registers_all_active_audio_and_login_routes(self):
        app = create_app()
        register_router(app)
        paths = {route.path for route in app.routes}
        required = {
            "/algorithm/api/login/travel",
            "/algorithm/api/login/food",
            "/algorithm/api/dates/extract_dates",
            "/algorithm/api/audiologin/travel",
            "/algorithm/api/audiologin/food",
            "/algorithm/api/audiologin/accommodation",
            "/algorithm/api/audiologin/summary",
        }
        self.assertTrue(required.issubset(paths), required - paths)


if __name__ == "__main__":
    unittest.main()

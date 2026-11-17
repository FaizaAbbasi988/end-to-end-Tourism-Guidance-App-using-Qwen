"""Check that archived teaching materials are still in the repository.

Run: python -m unittest discover -s tests -p "test_repository_cleanup.py" -v
"""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryCleanupTests(unittest.TestCase):
    def test_all_archived_experiments_are_present(self):
        expected_files = (
            "image_enhancement.py",
            "image_enhancement.ipynb",
            "text_correction.ipynb",
            "tt.ipynb",
            "non_login/test2.ipynb",
            "non_login/test_1.ipynb",
        )
        for filename in expected_files:
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / "experiments" / filename).is_file())

    def test_active_service_files_are_still_present(self):
        paths = (
            "Service/main.py",
            "Service/app/login_app.py",
            "Service/app/beautification_app.py",
            "Service/app/dates_app.py",
            "Service/app/parse_app.py",
            "Service/model/speech_model.py",
        )
        for filename in paths:
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / filename).is_file())


if __name__ == "__main__":
    unittest.main()

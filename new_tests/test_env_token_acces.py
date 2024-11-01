# new_tests/account_test.py
import os
import unittest
from unittest.mock import patch
from dotenv import load_dotenv

class TestEnvironmentVariables(unittest.TestCase):

    def setUp(self):
        # Load environment variables for the test
        load_dotenv()

    @patch.dict(os.environ, {"FIREBASE_WEB_API_KEY": "test_api_key"})
    def test_firebase_web_api_key_success(self):
        """Test when FIREBASE_WEB_API_KEY is correctly set."""
        firebase_key = os.getenv("FIREBASE_WEB_API_KEY")
        self.assertIsNotNone(firebase_key, "FIREBASE_WEB_API_KEY should not be None.")
        self.assertNotEqual(firebase_key, "", "FIREBASE_WEB_API_KEY should not be empty.")

    @patch.dict(os.environ, {"FIREBASE_WEB_API_KEY": ""})
    def test_firebase_web_api_key_failure(self):
        """Test when FIREBASE_WEB_API_KEY is empty or missing."""
        firebase_key = os.getenv("FIREBASE_WEB_API_KEY")
        self.assertIsNotNone(firebase_key, "FIREBASE_WEB_API_KEY should not be None.")
        self.assertEqual(firebase_key, "", "FIREBASE_WEB_API_KEY should be empty.")

if __name__ == "__main__":
    unittest.main()

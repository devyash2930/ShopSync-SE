import unittest
from unittest.mock import patch
import os

class TestEnvironmentVariables(unittest.TestCase):

    @patch.dict(os.environ, {"FIREBASE_WEB_API_KEY": "test_api_key"})
    def test_firebase_web_api_key_success(self):
        """Test when FIREBASE_WEB_API_KEY is correctly set."""
        # Simulate the presence of a valid API key
        firebase_key = os.getenv("FIREBASE_WEB_API_KEY")
        self.assertIsNotNone(firebase_key, "FIREBASE_WEB_API_KEY should not be None.")
        self.assertNotEqual(firebase_key, "", "FIREBASE_WEB_API_KEY should not be empty.")
        self.assertEqual(firebase_key, "test_api_key", "FIREBASE_WEB_API_KEY should match the test value.")

    @patch.dict(os.environ, {"FIREBASE_WEB_API_KEY": ""})
    def test_firebase_web_api_key_failure(self):
        """Test when FIREBASE_WEB_API_KEY is empty or missing."""
        # Simulate an empty API key
        firebase_key = os.getenv("FIREBASE_WEB_API_KEY")
        self.assertIsNotNone(firebase_key, "FIREBASE_WEB_API_KEY should not be None.")
        self.assertEqual(firebase_key, "", "FIREBASE_WEB_API_KEY should be empty.")

    @patch.dict(os.environ, {}, clear=True)
    def test_firebase_web_api_key_missing(self):
        """Test when FIREBASE_WEB_API_KEY is completely missing."""
        # Simulate the absence of the API key
        firebase_key = os.getenv("FIREBASE_WEB_API_KEY")
        self.assertIsNone(firebase_key, "FIREBASE_WEB_API_KEY should be None when missing.")

if __name__ == "__main__":
    unittest.main()

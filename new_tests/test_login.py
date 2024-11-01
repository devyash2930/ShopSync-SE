import unittest
from unittest.mock import patch, MagicMock
import sys 
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')


# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import functions to test
from frontend.account import is_valid_email, verify_password

class TestAccountFunctions(unittest.TestCase):

    @patch('frontend.account.firebase_admin.initialize_app')
    @patch('frontend.account.requests.post')
    def test_login_success(self, mock_post, mock_initialize_app):
        # Arrange
        email = "sr@gmail.com"
        password = "123456"
        mock_response = {
            "idToken": "some_valid_token"
        }
        mock_post.return_value.json.return_value = mock_response
        
        # Act
        result = verify_password(email, password)

        # Assert
        self.assertTrue(result)

    def test_invalid_email_format(self):
        # Act
        result = is_valid_email("invalid-email")
        # Assert
        self.assertFalse(result)

    @patch('frontend.account.firebase_admin.auth')
    @patch('frontend.account.requests.post')
    def test_account_does_not_exist(self, mock_post, mock_auth):
        # Arrange
        email = "rs@gmail.com"
        password = "123456"
        mock_response = {
            "error": {
                "message": "EMAIL_NOT_FOUND"
            }
        }
        mock_post.return_value.json.return_value = mock_response
        
        # Act
        result = verify_password(email, password)

        # Assert
        self.assertFalse(result)

    @patch('frontend.account.firebase_admin.auth')
    @patch('frontend.account.requests.post')
    def test_invalid_credentials(self, mock_post, mock_auth):
        # Arrange
        email = "sr@gmail.com"
        password = "123890"
        mock_response = {
            "error": {
                "message": "INVALID_PASSWORD"
            }
        }
        mock_post.return_value.json.return_value = mock_response
        
        # Act
        result = verify_password(email, password)

        # Assert
        self.assertFalse(result)

    @patch('frontend.account.firebase_admin.auth')
    @patch('frontend.account.requests.post')
    def test_missing_both_fields(self, mock_post, mock_auth):
        # Arrange & Act & Assert
        with self.assertRaises(ValueError) as context:
            verify_password("", "")
        self.assertEqual(str(context.exception), "Both email and password must be provided.")

    def test_missing_email(self):
        with self.assertRaises(ValueError) as context:
            verify_password("", "123456")
        self.assertEqual(str(context.exception), "Email must be provided.")

    def test_missing_password(self):
        with self.assertRaises(ValueError) as context:
            verify_password("test@example.com", "")
        self.assertEqual(str(context.exception), "Password must be provided.")

# Run the tests
if __name__ == '__main__':
    unittest.main()
    print(f"Tests run: {unittest.TestResult().testsRun}, "
          f"Failures: {len(unittest.TestResult().failures)}, "
          f"Errors: {len(unittest.TestResult().errors)}")


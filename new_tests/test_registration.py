# test_registration.py

import unittest
from unittest.mock import patch
import sys
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the signup function
from frontend.account import signup, is_valid_email

class TestAccountRegistration(unittest.TestCase):

    @patch('frontend.account.auth.create_user')
    def test_username_already_exists(self, mock_create_user):
        mock_create_user.side_effect = Exception("USERNAME_EXISTS")
        with self.assertRaises(ValueError) as context:
            signup("sr", "new_email@gmail.com", "1233456")
        self.assertEqual(str(context.exception), "The username is already taken.")

    @patch('frontend.account.auth.create_user')
    def test_email_already_exists(self, mock_create_user):
        mock_create_user.side_effect = Exception("EMAIL_EXISTS")
        with self.assertRaises(ValueError) as context:
            signup("new_user", "sr@gmail.com", "123456")
        self.assertEqual(str(context.exception), "The email is already registered.")

    def test_password_length(self):
        with self.assertRaises(ValueError) as context:
            signup("new_user", "test@gmail.com", "123")
        self.assertEqual(str(context.exception), "Password must be at least 6 characters long.")

    @patch('frontend.account.auth.create_user')
    def test_registration_success(self, mock_create_user):
        mock_create_user.return_value = True
        result = signup("lajksdf", "lajksdf@gmail.com", "123456")
        self.assertEqual(result, "Account created successfully.")

    def test_creds_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("", "", "")
        self.assertEqual(str(context.exception), "Please enter the credentials.")

    def test_username_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("", "test@example.com", "password123")
        self.assertEqual(str(context.exception), "Username is required.")

    def test_email_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("unique_user", "", "password123")
        self.assertEqual(str(context.exception), "Email Address is required.")

    def test_password_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("unique_user", "test@example.com", "")
        self.assertEqual(str(context.exception), "Password is required.")

    def test_invalid_email_format(self):
        with self.assertRaises(ValueError) as context:
            signup("unique_user", "invalid-email", "password123")
        self.assertEqual(str(context.exception), "Invalid email format. Please enter a valid email address.")

    def test_email_and_password_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("new_user", "", "")
        self.assertEqual(str(context.exception), "Email Address is required.")

    def test_password_and_username_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("", "test@example.com", "")
        self.assertEqual(str(context.exception), "Username is required.")

    def test_username_and_email_missing(self):
        with self.assertRaises(ValueError) as context:
            signup("", "", "password123")
        self.assertEqual(str(context.exception), "Username is required.")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountRegistration)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    print(f"\nTests run: {result.testsRun}, "
          f"Failures: {len(result.failures)}, "
          f"Errors: {len(result.errors)}")

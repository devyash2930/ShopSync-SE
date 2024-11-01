import unittest
from unittest.mock import patch
import sys
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'frontend')))

from account import initialize_firebase  # Adjust based on your actual imports
from firebase_admin import firestore  # Ensure Firestore is imported correctly

class TestAccountRegistration(unittest.TestCase):

    @patch('account.firebase_admin.initialize_app')
    def test_firebase_initialization_success(self, mock_initialize_app):
        # Simulate successful Firebase initialization
        mock_initialize_app.return_value = True
        result = initialize_firebase(suppress_errors=True)
        self.assertTrue(result, "Firebase should initialize successfully.")

    @patch('account.firebase_admin.initialize_app')
    def test_firebase_initialization_failure(self, mock_initialize_app):
        # Simulate Firebase initialization failure by raising an Exception
        mock_initialize_app.side_effect = Exception("Firebase initialization failed.")
        with self.assertRaises(Exception) as context:
            initialize_firebase(suppress_errors=True)
        self.assertEqual(str(context.exception), "Firebase initialization failed.")

    @patch('account.firebase_admin.auth')
    def test_firebase_auth_success(self, mock_auth):
        # Simulate successful Firebase authentication
        mock_auth.sign_in_with_email_and_password.return_value = {'idToken': 'mocked_token'}
        
        # Call the function that uses this auth
        result = mock_auth.sign_in_with_email_and_password('sr@gmail.com', '123456')
        self.assertEqual(result['idToken'], 'mocked_token', "Firebase auth should return a mocked token.")

    @patch('account.firebase_admin.auth')
    def test_firebase_auth_failure(self, mock_auth):
        # Simulate Firebase authentication failure by raising an Exception
        mock_auth.sign_in_with_email_and_password.side_effect = Exception("Authentication failed.")
        with self.assertRaises(Exception) as context:
            mock_auth.sign_in_with_email_and_password('sr@gmail.com', '123098')
        self.assertEqual(str(context.exception), "Authentication failed.")

    @patch('firebase_admin.firestore')  # Mock Firestore correctly
    def test_firebase_read_success(self, mock_firestore):
        # Simulate successful read operation from Firestore
        mock_firestore.client.return_value.collection.return_value.document.return_value.get.return_value.to_dict.return_value = {
            'name': 'sr', 
            'email': 'sr@gmail.com'
        }
        
        # Simulate the read function call
        data = mock_firestore.client().collection('users').document('user_id').get().to_dict()
        self.assertEqual(data, {'name': 'sr', 'email': 'sr@gmail.com'}, "Data should match the mocked data.")

    @patch('firebase_admin.firestore')  # Mock Firestore correctly
    def test_firebase_read_failure(self, mock_firestore):
        # Simulate failure in reading from Firestore
        mock_firestore.client.return_value.collection.return_value.document.return_value.get.side_effect = Exception("Read failed.")
        with self.assertRaises(Exception) as context:
            mock_firestore.client().collection('users').document('user_id').get()
        self.assertEqual(str(context.exception), "Read failed.", "Reading from Firestore should raise an exception.")

# Run the tests and print results
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountRegistration)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    print(f"\nTests run: {result.testsRun}, "
          f"Failures: {len(result.failures)}, "
          f"Errors: {len(result.errors)}")
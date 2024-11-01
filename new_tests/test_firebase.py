import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'frontend')))

from account import initialize_firebase  # Import your actual initialize function

class TestAccountRegistration(unittest.TestCase):

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.credentials.Certificate')
    def test_firebase_initialization_success(self, mock_certificate, mock_initialize_app):
        # Simulate successful Firebase initialization
        mock_certificate.return_value = MagicMock()  # Mock Certificate to avoid file loading
        mock_initialize_app.return_value = MagicMock()  # Mock initialize_app
        
        result = initialize_firebase()
        self.assertTrue(result, "Firebase shoul# Run the tests and print results
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountRegistration)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    print(f"\nTests run: {result.testsRun}, "
          f"Failures: {len(result.failures)}, "
          f"Errors: {len(result.errors)}")d initialize successfully.")

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.credentials.Certificate')
    def test_firebase_initialization_failure(self, mock_certificate, mock_initialize_app):
        # Mock Certificate to raise an exception when called
        mock_certificate.side_effect = FileNotFoundError("Firebase initialization failed.")
        
        with self.assertRaises(FileNotFoundError) as context:
            initialize_firebase()
        self.assertEqual(str(context.exception)# Run the tests and print results
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountRegistration)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    print(f"\nTests run: {result.testsRun}, "
          f"Failures: {len(result.failures)}, "
          f"Errors: {len(result.errors)}"), "Firebase initialization failed.")


    @patch('firebase_admin.auth')
    def test_firebase_auth_success(self, mock_auth):
        # Simulate successful Firebase authentication
        mock_auth.sign_in_with_email_and_password.return_value = {'idToken': 'mocked_token'}
        result = mock_auth.sign_in_with_email_and_password('sr@gmail.com', '123456')
        self.assertEqual(result['idToken'], 'mocked_token', "Firebase auth should return a mocked token.")

    @patch('firebase_admin.auth')
    def test_firebase_auth_failure(self, mock_auth):
        # Simulate Firebase authentication failure by raising an Exception
        mock_auth.sign_in_with_email_and_password.side_effect = Exception("Authentication failed.")
        with self.assertRaises(Exception) as context:
            mock_auth.sign_in_with_email_and_password('sr@gmail.com', '123098')
        self.assertEqual(str(context.exception), "Authentication failed.")

    @patch('firebase_admin.firestore.client')
    def test_firebase_read_success(self, mock_firestore_client):
        # Simulate successful read operation from Firestore
        mock_doc = MagicMock()
        mock_doc.get.return_value.to_dict.return_value = {'name': 'sr', 'email': 'sr@gmail.com'}
        mock_firestore_client.return_value.collection.return_value.document.return_value = mock_doc
        
        data = mock_firestore_client().collection('users').document('user_id').get().to_dict()
        self.assertEqual(data, {'name': 'sr', 'email': 'sr@gmail.com'}, "Data should match the mocked data.")

    @patch('firebase_admin.firestore.client')
    def test_firebase_read_failure(self, mock_firestore_client):
        # Simulate failure in reading from Firestore
        mock_doc = MagicMock()
        mock_doc.get.side_effect = Exception("Read failed.")
        mock_firestore_client.return_value.collection.return_value.document.return_value = mock_doc

        with self.assertRaises(Exception) as context:
            mock_firestore_client().collection('users').document('user_id').get()
        self.assertEqual(str(context.exception), "Read failed.", "Reading from Firestore should raise an exception.")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountRegistration)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    print(f"\nTests run: {result.testsRun}, "
          f"Failures: {len(result.failures)}, "
          f"Errors: {len(result.errors)}")

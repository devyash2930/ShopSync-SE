import unittest
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'frontend')))
# Initialize Firebase Admin SDK (make sure to replace with your actual credentials)
# cred = credentials.Certificate("path/to/your/credentials.json")
# firebase_admin.initialize_app(cred)

# Import the app function to test
from favourites import app

class TestFavouritesFunctions(unittest.TestCase):

    def setUp(self):
        # Set up session state for the user
        st.session_state.user_email = "vd@gmail.com"  # Use a real user email
        self.db = firestore.client()
        self.user_uid = "vd"  # Replace with the actual UID for the user with favorites

    def test_favourites_page_with_data(self):
        # Act
        app()  # Call the app function

        # Assert: Check if the user's document exists in Firestore
        user_fav_doc = self.db.collection("favourites").document(self.user_uid).get()
        self.assertTrue(user_fav_doc.exists, "User favorites document should exist.")

    def test_favourites_page_no_data(self):
        # Arrange: Set user_email to a user without favorites
        st.session_state.user_email = "srv@gmail.com"  # Use a real user email without favorites
        self.user_uid = "srv"  # Replace with a non-existent UID

        # Act
        app()  # Call the app function

        # Assert: Check that the user's document does not exist
        user_fav_doc = self.db.collection("favourites").document(self.user_uid).get()
        self.assertFalse(user_fav_doc.exists, "User favorites document should not exist.")

# Run the tests
if __name__ == '__main__':
    unittest.main()
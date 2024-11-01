import streamlit as st
import unittest
import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the app function from the correct module
from frontend.account import app

class TestPasswordVisibility(unittest.TestCase):

    def setUp(self):
        """Reset the Streamlit session state before each test."""
        st.session_state.clear()  # Clear session state before each test
        st.session_state.show_password = False  # Reset state

    def test_password_visibility_on(self):
        """Test that the password is shown when the toggle is enabled."""
        self.assertFalse(st.session_state.show_password)
        st.session_state.show_password = True  # Simulate user action
        app()  # Call the app function
        self.assertTrue(st.session_state.show_password)

    def test_password_visibility_off(self):
        """Test that the password is hidden when the toggle is disabled."""
        st.session_state.show_password = True  # Simulate password being visible
        app()  # Call the app function
        self.assertTrue(st.session_state.show_password)
        st.session_state.show_password = False  # Simulate user action
        app()  # Call the app function again
        self.assertFalse(st.session_state.show_password)

if __name__ == "__main__":
    unittest.main(verbosity=2)
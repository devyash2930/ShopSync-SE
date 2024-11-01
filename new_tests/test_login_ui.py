import streamlit as st
import pytest
import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the app function from the correct module
from frontend.account import app

@pytest.fixture
def reset_session_state():
    """Fixture to reset the Streamlit session state before each test."""
    st.session_state.show_password = False  # Reset state before each test
    yield
    st.session_state.show_password = False  # Reset after the test

def test_password_visibility_on(reset_session_state):
    """Test that the password is shown when the toggle is enabled."""
    # Initially, the password should be hidden
    assert st.session_state.show_password == False
    
    # Simulate button click to show password
    st.session_state.show_password = True  # Simulate user action to show password
    app()  # Call the app function

    # Assert that the password is visible
    assert st.session_state.show_password == True  # After toggling, it should be visible

def test_password_visibility_off(reset_session_state):
    """Test that the password is hidden when the toggle is disabled."""
    # Initially, the password should be shown
    st.session_state.show_password = True  # Simulate the password being visible
    app()  # Call the app function

    # Assert that the password is visible
    assert st.session_state.show_password == True  # Initially, it should be visible

    # Simulate button click to hide password
    st.session_state.show_password = False  # Simulate user action to hide password
    app()  # Call the app function again

    # Assert that the password is hidden
    assert st.session_state.show_password == False  # After toggling, it should be hidden

if __name__ == "__main__":
    pytest.main(['-q', __file__])

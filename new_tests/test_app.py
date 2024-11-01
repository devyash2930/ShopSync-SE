import os
import subprocess
import time
import pytest
import httpx

# Path to the app.py file
path_to_app = os.path.join("..", "src", "frontend", "app.py")

@pytest.fixture(scope="module")
def start_streamlit_app():
    # Start the Streamlit app as a subprocess
    process = subprocess.Popen(
        ["streamlit", "run", path_to_app],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # Wait for the Streamlit server to start
    yield process  # Provide the process to the test function
    process.terminate()  # Terminate the server after tests


def test_streamlit_app_running(start_streamlit_app):
    # Test if the Streamlit app is running and responding successfully
    try:
        response = httpx.get("http://localhost:8501/")  # Default Streamlit port
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}."
        print("Streamlit app is running successfully.")
    except httpx.RequestError:
        pytest.fail("Failed to connect to the Streamlit server. Make sure it's running.")


def test_streamlit_app_not_running():
    # Test when the Streamlit app is not running
    try:
        response = httpx.get("http://localhost:8502/")  # A port where no server is running
        assert response.status_code != 200, "Expected a non-200 status code since the server is not running."
    except httpx.RequestError:
        print("Confirmed that the server is not running on port 8502 as expected.")



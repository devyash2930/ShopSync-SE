import os
import subprocess
import time
import pytest
import httpx

# Path to the main.py file
path_to_main = os.path.join("..", "src", "main.py")

@pytest.fixture(scope="module")
def start_fastapi_app():
    # Start the FastAPI app as a subprocess
    process = subprocess.Popen(
        ["python", path_to_main],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # Wait for the FastAPI server to start
    yield process  # Provide the process to the test function
    process.terminate()  # Terminate the server after tests


def test_fastapi_app_running(start_fastapi_app):
    # Test if the FastAPI app is running and responding successfully
    try:
        response = httpx.get("http://127.0.0.1:5051/")  # Default FastAPI port
        assert response.status_code == 307, f"Expected status code 307 but got {response.status_code}."
        print("FastAPI app is running successfully.")
    except httpx.RequestError:
        pytest.fail("Failed to connect to the FastAPI server. Make sure it's running.")


def test_fastapi_app_not_running():
    # Test when the FastAPI app is not running
    try:
        response = httpx.get("http://127.0.0.1:5052/")  # A port where no server is running
        assert response.status_code != 200, "Expected a non-200 status code since the server is not running."
    except httpx.RequestError:
        print("Confirmed that the server is not running on port 5052 as expected.")
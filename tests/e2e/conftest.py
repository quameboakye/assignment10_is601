# tests/e2e/conftest.py
import subprocess
import time
import sys
import pytest
import requests

@pytest.fixture(scope='session', autouse=True)
def fastapi_server():
    """Start FastAPI server as a subprocess before E2E tests and terminate after session."""
    cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
    
    try:
        fastapi_process = subprocess.Popen([sys.executable, 'main.py'])
    except Exception:
        fastapi_process = subprocess.Popen(cmd)
        
    server_url = 'http://127.0.0.1:8000/'
    
    timeout = 15
    start_time = time.time()
    server_up = False
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code < 500:
                server_up = True
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    
    if not server_up:
        fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    fastapi_process.terminate()
    fastapi_process.wait()
import os
os.environ["DEMO_MODE"]="true"
import pytest
from fastapi.testclient import TestClient
from app.config import get_settings
get_settings.cache_clear()
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client: yield test_client

@pytest.fixture
def valid_request():
    return {"story_prompt":"A young inventor discovers a friendly robot in an old workshop.","character_name":"Maya","setting":"A futuristic city","story_tone":"Adventurous","art_style":"Colorful anime","panel_count":5}

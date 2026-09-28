import pytest
from pydantic import ValidationError
from app.models import ComicRequest

def test_valid_request(valid_request):
    model=ComicRequest(**valid_request)
    assert model.character_name=="Maya" and model.panel_count==5

def test_rejects_short_prompt(valid_request):
    valid_request["story_prompt"]="short"
    with pytest.raises(ValidationError): ComicRequest(**valid_request)

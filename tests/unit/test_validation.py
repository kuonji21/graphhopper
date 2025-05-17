import requests_mock
from requests_mock import ANY  # Correct import for the ANY matcher
from src.main import geocoding

def test_empty_location_input(monkeypatch, requests_mock):
    # Mock the user input
    inputs = iter(["", "Paris"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Mock the API response using the ANY matcher
    mock_response = {
        "hits": [{
            "point": {"lat": 48.85, "lng": 2.35},
            "name": "Paris",
            "osm_value": "city"
        }]
    }
    requests_mock.get(ANY,  # Use the imported ANY constant
                     json=mock_response,
                     status_code=200)

    # Test the geocoding flow
    status, lat, lng, name = geocoding("", "valid_key")
    
    assert status == 200
    assert lat == 48.85
    assert name == "Paris"
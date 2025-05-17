# Graphhopper API tests (Niño)
import requests_mock
from src.main import geocoding

def test_geocoding_api_success():
    with requests_mock.Mocker() as m:
        mock_response = {
            "hits": [{
                "point": {"lat": 40.71, "lng": -74.01},
                "name": "New York",
                "osm_value": "city"  # Add this line
            }]
        }
        m.get(requests_mock.ANY, json=mock_response, status_code=200)
        status, lat, lng, name = geocoding("New York", "dummy_key")
        assert status == 200
        assert lat == 40.71

def test_api_rate_limit():
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, status_code=429, json={"message": "API limit exceeded"})
        status, lat, lng, name = geocoding("Paris", "dummy_key")
        assert status == 429

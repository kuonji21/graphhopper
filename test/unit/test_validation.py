# Input validation tests 
from src.main import geocoding

def test_empty_location_input():
    # Simulate empty input followed by valid input
    status, lat, lng, name = geocoding("", "dummy_key")
    assert status != 200  # Expect failure for empty input

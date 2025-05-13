# Export feature tests (Lance) 
from src.main import export_directions
import os

def test_export_directions():
    orig = (200, "40.71", "-74.01", "New York")
    dest = (200, "34.05", "-118.24", "Los Angeles")
    fake_path_data = {
        "paths": [{
            "distance": 100000,
            "time": 7200000,
            "instructions": [{"text": "Turn left", "distance": 500}]
        }]
    }
    export_directions(orig, dest, "car", fake_path_data)
    filename = "directions_New_York_to_Los_Angeles.txt"
    assert os.path.exists(filename)
    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
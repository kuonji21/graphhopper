# Tests for favorites (Jomari)  
from src.main import save_favorite, load_favorites
import os

def test_save_and_load_favorite():
    # Test valid favorite
    save_favorite("test_loc", (200, "12.34", "56.78", "Test Location"))
    favorites = load_favorites()
    assert "test_loc" in favorites
    # Cleanup
    if os.path.exists("favorites.txt"):
        os.remove("favorites.txt")

def test_invalid_favorite_name():
    # Test invalid characters in name
    try:
        save_favorite("invalid/name", (200, "12.34", "56.78", "Test"))
    except ValueError as e:
        assert "Invalid name" in str(e)

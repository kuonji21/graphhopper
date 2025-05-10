from src.main import display_header, clear_screen
from unittest.mock import patch
import os

def test_display_header(capsys):
    display_header("Test Header")
    captured = capsys.readouterr()
    assert "Test Header" in captured.out
    assert "=" * 50 in captured.out

def test_clear_screen():
    # Test for Windows
    with patch('os.name', 'nt'):
        clear_screen()
    # Test for Linux/Mac
    with patch('os.name', 'posix'):
        clear_screen()

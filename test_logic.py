import unittest
import os
import json
from session import log_session # Upewnij się, że plik session.py jest w tym samym folderze

class TestSessionLogic(unittest.TestCase):

    def setUp(self):
        """Przygotowanie przed każdym testem."""
        self.log_path = os.path.join("data", "session_log.json")
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def tearDown(self):
        """Sprzątanie po każdym teście."""
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def test_log_session_creates_file_and_adds_entry(self):
        """Testuje, czy funkcja log_session tworzy plik i dodaje pojedynczy wpis."""
        log_session("start_time_1", "end_time_1", True, True)

        self.assertTrue(os.path.exists(self.log_path)) # Sprawdza, czy plik istnieje

        with open(self.log_path, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1) # Sprawdza, czy jest jeden wpis
        self.assertEqual(data[0]["session_completed"], True)

if __name__ == '__main__':
    unittest.main()
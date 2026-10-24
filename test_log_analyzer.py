
import unittest
from collections import Counter

class LogAnalyzerTests(unittest.TestCase):

    def test_error_count(self):
        messages = [
            "Database connection failed",
            "Request timed out",
            "Database connection failed",
        ]

        counts = Counter(messages)

        self.assertEqual(
            counts["Database connection failed"], 2
        )
        self.assertEqual(counts["Request timed out"], 1)

    def test_log_level_count(self):
        levels = ["INFO", "ERROR", "WARNING", "ERROR"]

        counts = Counter(levels)

        self.assertEqual(counts["ERROR"], 2)
        self.assertEqual(counts["INFO"], 1)
        self.assertEqual(counts["WARNING"], 1)

    def test_empty_logs(self):
        counts = Counter([])

        self.assertEqual(len(counts), 0)

if __name__ == "__main__":
    unittest.main()
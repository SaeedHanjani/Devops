# tests/test_sample.py

import unittest
from src.sample import add  # Adjust the import based on your project structure

class TestSample(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()

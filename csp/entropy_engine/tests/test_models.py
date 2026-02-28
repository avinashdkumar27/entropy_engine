import unittest
from core.attack_models import get_crack_time, format_time, ATTACK_MODELS

class TestAttackModels(unittest.TestCase):
    def test_get_crack_time(self):
        combinations = 1e8 # 100 million
        # CPU is 1e8 guesses / sec
        time = get_crack_time(combinations, "CPU (basic)")
        self.assertEqual(time, 1.0)
        
    def test_invalid_model_fallback(self):
        combinations = 1e8
        # Should fallback to CPU (basic)
        time = get_crack_time(combinations, "NonExistentModel")
        self.assertEqual(time, 1.0)
        
    def test_format_time(self):
        self.assertEqual(format_time(0.5), "Less than a second")
        self.assertEqual(format_time(1), "1 second")
        self.assertEqual(format_time(65), "1 minute")
        self.assertEqual(format_time(3660), "1 hour")

if __name__ == "__main__":
    unittest.main()

import unittest
from core.strength_logic import analyze_password

class TestStrengthLogic(unittest.TestCase):
    def test_empty_password(self):
        res = analyze_password("")
        self.assertEqual(res["entropy"], 0)
        self.assertEqual(res["zxcvbn_score"], 0)
        self.assertEqual(res["meter_label"], "None")
        
    def test_weak_password(self):
        res = analyze_password("password123")
        self.assertLess(res["entropy"], 60)
        self.assertEqual(res["zxcvbn_score"], 0)
        # Should be weak
        
    def test_strong_password(self):
        # High entropy and no dictionary
        res = analyze_password("T^b@rQ8!mPxL2vNz")
        self.assertGreater(res["entropy"], 80)
        self.assertGreaterEqual(res["zxcvbn_score"], 3)
        self.assertTrue(res["meter_label"] in ["Strong", "Very Strong", "Unbreakable"])

if __name__ == "__main__":
    unittest.main()

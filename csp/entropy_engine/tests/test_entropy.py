import unittest
from core.entropy import calculate_entropy

class TestEntropy(unittest.TestCase):
    def test_empty_password(self):
        c, comb, e = calculate_entropy("")
        self.assertEqual(c, 0)
        self.assertEqual(comb, 0)
        self.assertEqual(e, 0)
        
    def test_lowercase(self):
        c, comb, e = calculate_entropy("abc")
        self.assertEqual(c, 26)
        self.assertEqual(comb, 26**3)
        self.assertAlmostEqual(e, 3 * 4.700439718141092, places=5)
        
    def test_mixed(self):
        c, comb, e = calculate_entropy("Abc1!")
        # 1 lower (26) + 1 upper (26) + 1 digit (10) + 1 symbol (32) = 94
        self.assertEqual(c, 94)
        self.assertEqual(comb, 94**5)

if __name__ == "__main__":
    unittest.main()

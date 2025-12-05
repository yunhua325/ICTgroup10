import unittest
from calcErrorRate import calculate_bit_errors, write_result_to_csv
import os

class TestCalcErrorRate(unittest.TestCase):
    def test_calculate_bit_errors(self):
        # 全部相同
        b1 = bytes([0b10101010, 0b11110000])
        b2 = bytes([0b10101010, 0b11110000])
        total, error = calculate_bit_errors(b1, b2)
        self.assertEqual(total, 16)
        self.assertEqual(error, 0)
        # 全部不同
        b3 = bytes([0b00000000, 0b00000000])
        total, error = calculate_bit_errors(b1, b3)
        self.assertEqual(total, 16)
        self.assertEqual(error, 8)
    def test_write_result_to_csv(self):
        path = "test_result.csv"
        write_result_to_csv("a.bin", "b.bin", 0.125, path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('"a.bin"', content)
        self.assertIn('"b.bin"', content)
        self.assertIn('0.125', content)
        os.remove(path)

if __name__ == "__main__":
    unittest.main()
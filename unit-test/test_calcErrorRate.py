import unittest
import os
from calcErrorRate import calculate_bit_errors, write_result_to_csv

class TestCalcErrorRate(unittest.TestCase):
    def test_identical_files(self):
        bytes1 = b'\xAA\x55'  # 10101010, 01010101
        bytes2 = b'\xAA\x55'
        total, errors = calculate_bit_errors(bytes1, bytes2)
        print('total:', total, 'errors:', errors)
        self.assertEqual(errors, 0)
        self.assertEqual(total, 16)

    def test_completely_different_files(self):
        a = b'\xFF\xFF\xFF'
        b = b'\x00\x00\x00'
        errors, total = calculate_bit_errors(a, b)
        self.assertEqual(errors, 24)
        self.assertEqual(total, 24)

    def test_partial_errors(self):
        a = b'\xAA\xBB\xCC'
        b = b'\xAA\x00\xCC'
        total, errors = calculate_bit_errors(a, b)
        print('total:', total, 'errors:', errors)
        self.assertEqual(errors, 6)
        self.assertEqual(total, 24)

    def test_different_lengths(self):
        a = b'\xAA\xBB\xCC'
        b = b'\xAA\xBB'
        total, errors = calculate_bit_errors(a, b)
        print('total:', total, 'errors:', errors)
        self.assertEqual(total, 24)

    def test_csv_output(self):
        result_path = 'unit-test/test_result.csv'
        write_result_to_csv(result_path, 'a.bin', 'b.bin', 0.123)
        with open(result_path, 'r') as f:
            line = f.readline().strip()
        self.assertEqual(line, '"a.bin","b.bin","0.123"')
        #os.remove(result_path)

if __name__ == '__main__':
    unittest.main()
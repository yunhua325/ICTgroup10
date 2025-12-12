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
        total, errors = calculate_bit_errors(a, b)
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
        a = b'\xAA\xBB\xCC'  # 3字节
        b = b'\xAA\xBB'      # 2字节，补0后变成 \xAA\xBB\x00
        total, errors = calculate_bit_errors(a, b)
        print('total:', total, 'errors:', errors)
        self.assertEqual(total, 24)  # 3字节 * 8位 = 24位
        # 最后一字节\xCC (11001100) vs \x00 (00000000) 应该有4个错误位
        self.assertEqual(errors, 4)

    def test_empty_files(self):
        a = b''
        b = b''
        total, errors = calculate_bit_errors(a, b)
        self.assertEqual(total, 0)
        self.assertEqual(errors, 0)

    def test_csv_output(self):
        import os
        result_path = 'test-date/test_result.csv'
        # 确保目录存在
        os.makedirs('test-date', exist_ok=True)
        write_result_to_csv('a.bin', 'b.bin', 0.123, result_path)
        with open(result_path, 'r') as f:
            lines = f.readlines()
        
        # 检查表头和数据行
        self.assertEqual(lines[0].strip(), '"INPUT1","INPUT2","error_rate"')
        self.assertEqual(lines[1].strip(), '"a.bin","b.bin","0.123"')
        
        # 测试追加模式
        write_result_to_csv('c.bin', 'd.bin', 0.456, result_path)
        with open(result_path, 'r') as f:
            lines = f.readlines()
        
        # 应该有3行（表头+2行数据）
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[2].strip(), '"c.bin","d.bin","0.456"')
        # 清理测试文件
        # os.remove(result_path)
        # os.rmdir('test-date')

if __name__ == '__main__':
    unittest.main()
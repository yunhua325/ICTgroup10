import unittest
from repetitionCoder import encode_repetition, decode_repetition

class TestRepetitionCoder(unittest.TestCase):
    def test_encode_decode(self):
        src = b'\xAA\x55'  # 10101010 01010101
        for n in [3, 5, 7]:
            encoded = encode_repetition(src, n)
            self.assertEqual(len(encoded), len(src) * 8 * n)
            decoded = decode_repetition(encoded, n)
            self.assertEqual(decoded, src)

    def test_majority_vote(self):
        # 构造一个有错误的重复码序列
        src = b'\xFF'  # 11111111
        n = 5
        encoded = encode_repetition(src, n)
        # 手动修改部分比特
        tampered = bytearray(encoded)
        tampered[0] = 0x00
        tampered[1] = 0x00
        decoded = decode_repetition(bytes(tampered), n)
        self.assertEqual(decoded, src)  # 多数表决仍为1

if __name__ == '__main__':
    unittest.main()
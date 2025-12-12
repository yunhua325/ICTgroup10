import unittest
import os
import random
import string

class TestRepetitionCoder(unittest.TestCase):

    def setUp(self):
        """生成大于10KB的测试文件"""
        file_size = 10240  # 10KB
        with open("test.txt", "w") as f:
            f.write(self.generate_random_text(file_size))  # 生成随机文本

    def tearDown(self):
        """删除测试生成的文件"""
        for filename in ["test.enc", "test_decoded.txt"]:
            if os.path.exists(filename):
                os.remove(filename)

    def generate_random_text(self, size):
        """生成指定大小的随机文本"""
        chars = string.ascii_letters + string.digits + string.punctuation + " \n"
        return ''.join(random.choice(chars) for _ in range(size))

    def test_file_generation(self):
        """确保生成的文件大小大于10KB"""
        file_size = os.path.getsize("test.txt")
        self.assertGreater(file_size, 10240, "File size is not greater than 10KB")

if __name__ == '__main__':
    unittest.main()


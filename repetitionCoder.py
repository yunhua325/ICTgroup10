#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重复码编码/解码程序
API:
    repetitionCoder.py encode LEN INPUT OUTPUT
    repetitionCoder.py decode INPUT OUTPUT
"""
import sys
import struct
import os

def encode_repetition(src_bytes, n):
    """对每个比特重复n次编码"""
    encoded = bytearray()
    for byte in src_bytes:
        for bit_pos in range(8):
            bit = (byte >> (7 - bit_pos)) & 1
            for _ in range(n):
                encoded.append(bit)
    return encoded

def decode_repetition(encoded_bytes, n):
    """对每n个比特做多数表决解码"""
    decoded = bytearray()
    total_bits = len(encoded_bytes)
    if total_bits % (8 * n) != 0:
        raise ValueError("编码数据长度不正确")
    num_bytes = total_bits // (8 * n)
    for i in range(num_bytes):
        byte_val = 0
        for bit_pos in range(8):
            bits = encoded_bytes[(i * 8 + bit_pos) * n : (i * 8 + bit_pos + 1) * n]
            ones = sum(bits)
            bit = 1 if ones > n // 2 else 0
            byte_val = (byte_val << 1) | bit
        decoded.append(byte_val)
    return decoded

def write_encoded_file(output_path, n, src_bytes):
    with open(output_path, 'wb') as f:
        # 文件头：LEN(1字节) + 源长度(4字节)
        f.write(struct.pack('B', n))
        f.write(struct.pack('>I', len(src_bytes)))
        encoded = encode_repetition(src_bytes, n)
        f.write(encoded)

def read_encoded_file(input_path):
    with open(input_path, 'rb') as f:
        n = struct.unpack('B', f.read(1))[0]
        src_len = struct.unpack('>I', f.read(4))[0]
        encoded = f.read()
    return n, src_len, encoded

def encode_command(n, input_path, output_path):
    if n % 2 == 0 or n <= 2 or n >= 10:
        print("LEN必须为大于2小于10的奇数", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(input_path):
        print(f"输入文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)
    with open(input_path, 'rb') as f:
        src_bytes = f.read()
    write_encoded_file(output_path, n, src_bytes)
    print(f"编码完成: {output_path}")

def decode_command(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"输入文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)
    n, src_len, encoded = read_encoded_file(input_path)
    expected_len = 8 * n * src_len
    if len(encoded) < expected_len:
        print(f"编码数据长度不足，文件可能损坏或被截断 (实际: {len(encoded)}, 理论: {expected_len})", file=sys.stderr)
        sys.exit(1)
    decoded = decode_repetition(encoded, n)
    if len(decoded) != src_len:
        print(f"解码长度不匹配 (实际: {len(decoded)}, 理论: {src_len})", file=sys.stderr)
        sys.exit(1)
    with open(output_path, 'wb') as f:
        f.write(decoded)
    print(f"解码完成: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("用法: repetitionCoder.py encode LEN INPUT OUTPUT 或 repetitionCoder.py decode INPUT OUTPUT", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'encode' and len(sys.argv) == 5:
        n = int(sys.argv[2])
        input_path = sys.argv[3]
        output_path = sys.argv[4]
        encode_command(n, input_path, output_path)
    elif cmd == 'decode' and len(sys.argv) == 4:
        input_path = sys.argv[2]
        output_path = sys.argv[3]
        decode_command(input_path, output_path)
    else:
        print("参数错误！", file=sys.stderr)
        print("用法: repetitionCoder.py encode LEN INPUT OUTPUT 或 repetitionCoder.py decode INPUT OUTPUT", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
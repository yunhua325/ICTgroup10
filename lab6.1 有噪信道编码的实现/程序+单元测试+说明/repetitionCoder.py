"""重复码编码器和解码器。

程序实现了用于纠错的重复码编码和解码功能。
重复码将每个比特重复n次（n为奇数），通过多数表决实现纠错。

用法:
    repetitionCoder.py encode LEN INPUT OUTPUT
    repetitionCoder.py decode INPUT OUTPUT

编码文件格式:
    | LEN (1字节) | source length (4字节) | codeword sequence (多个字节) |
"""

import sys
import argparse
from bitstring import BitStream, Bits

__author__ = "Student"
__version__ = "1.0.0"


# 文件格式常量
HEADER_BYTES_LEN = 1        # 存储码长的字节数
HEADER_BYTES_SOURCE_LEN = 4  # 存储源文件比特数的字节数
HEADER_BYTE_ORDER = 'little' # 文件头的字节序（小端序） 


def encode(input_file, output_file, code_len):
    """使用重复码对输入文件进行编码。
    
    参数:
        input_file: 输入文件路径（任意格式）
        output_file: 编码后的输出文件路径
        code_len: 重复码长度（必须是奇数，2 < n < 10）
    
    异常:
        ValueError: 如果码长无效
        IOError: 如果文件操作失败
    """
    # 验证码长
    if code_len <= 2 or code_len >= 10:
        raise ValueError(f"Code length must be 2 < n < 10, got {code_len}")
    if code_len % 2 == 0:
        raise ValueError(f"Code length must be odd, got {code_len}")
    
    # 将输入文件读取为比特流
    try:
        input_bits = BitStream(filename=input_file)
    except Exception as e:
        raise IOError(f"Failed to read input file: {e}")
    
    source_length = input_bits.length
    
    # 编码：将每个比特重复 code_len 次
    encoded_bits = BitStream()
    for bit in input_bits:
        # 将比特重复 code_len 次
        if bit:
            encoded_bits.append(Bits(bin='1' * code_len))
        else:
            encoded_bits.append(Bits(bin='0' * code_len))
    
    # 写入输出文件（包含文件头）
    try:
        with open(output_file, 'wb') as out_file:
            # 写入文件头：LEN (1字节) + source length (4字节)
            out_file.write(code_len.to_bytes(HEADER_BYTES_LEN, byteorder=HEADER_BYTE_ORDER))
            out_file.write(source_length.to_bytes(HEADER_BYTES_SOURCE_LEN, byteorder=HEADER_BYTE_ORDER))
            
            # 写入编码后的码字序列
            encoded_bits.tofile(out_file)
    except Exception as e:
        raise IOError(f"Failed to write output file: {e}")
    
    print(f"Encoded: {source_length} bits -> {encoded_bits.length} bits (code length: {code_len})")
    print(f"Output saved to: {output_file}")


def decode(input_file, output_file):
    """解码重复码编码的文件。
    
    参数:
        input_file: 编码后的输入文件路径
        output_file: 解码后的输出文件路径
    
    异常:
        IOError: 如果文件操作失败
        ValueError: 如果文件格式无效
    """
    try:
        with open(input_file, 'rb') as in_file:
            # 读取文件头
            len_bytes = in_file.read(HEADER_BYTES_LEN)
            if len(len_bytes) != HEADER_BYTES_LEN:
                raise ValueError("Invalid file format: cannot read code length")
            
            source_len_bytes = in_file.read(HEADER_BYTES_SOURCE_LEN)
            if len(source_len_bytes) != HEADER_BYTES_SOURCE_LEN:
                raise ValueError("Invalid file format: cannot read source length")
            
            # 解析文件头
            code_len = int.from_bytes(len_bytes, byteorder=HEADER_BYTE_ORDER)
            source_length = int.from_bytes(source_len_bytes, byteorder=HEADER_BYTE_ORDER)
            
            # 读取码字序列
            encoded_bytes = in_file.read()
            encoded_bits = BitStream(encoded_bytes)
            
    except Exception as e:
        raise IOError(f"Failed to read input file: {e}")
    
    # 验证码长
    if code_len <= 2 or code_len >= 10 or code_len % 2 == 0:
        raise ValueError(f"Invalid code length in file: {code_len}")
    
    # 使用多数表决进行解码
    decoded_bits = BitStream()
    expected_bits = source_length * code_len
    
    if encoded_bits.length < expected_bits:
        raise ValueError(f"Invalid file format: expected at least {expected_bits} bits, got {encoded_bits.length}")
    
    # 对每组 code_len 个比特使用多数表决进行解码
    for i in range(source_length):
        start_pos = i * code_len
        end_pos = start_pos + code_len
        codeword = encoded_bits[start_pos:end_pos]
        
        # 多数表决：统计1的个数
        ones_count = codeword.count(1)
        # 由于 code_len 是奇数，多数是 > code_len/2
        decoded_bit = 1 if ones_count > code_len / 2 else 0
        decoded_bits.append(Bits(uint=decoded_bit, length=1))
    
    # 写入解码后的输出
    try:
        with open(output_file, 'wb') as out_file:
            decoded_bits.tofile(out_file)
    except Exception as e:
        raise IOError(f"Failed to write output file: {e}")
    
    print(f"Decoded: {encoded_bits.length} bits -> {decoded_bits.length} bits (code length: {code_len})")
    print(f"Output saved to: {output_file}")


def main():
    """主函数，处理命令行参数。"""
    parser = argparse.ArgumentParser(
        description='重复码编码器和解码器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                示例:
                %(prog)s encode 3 input.txt output.enc
                %(prog)s decode output.enc output_decoded.txt
                """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='要执行的命令')
    
    # 编码命令
    encode_parser = subparsers.add_parser('encode', help='使用重复码对文件进行编码')
    encode_parser.add_argument('LEN', type=int, help='码长（必须是奇数，2 < n < 10）')
    encode_parser.add_argument('INPUT', help='输入文件路径')
    encode_parser.add_argument('OUTPUT', help='编码后的输出文件路径')
    
    # 解码命令
    decode_parser = subparsers.add_parser('decode', help='解码重复码编码的文件')
    decode_parser.add_argument('INPUT', help='编码后的输入文件路径')
    decode_parser.add_argument('OUTPUT', help='解码后的输出文件路径')
    
    args = parser.parse_args()
    
    if args.command == 'encode':
        try:
            encode(args.INPUT, args.OUTPUT, args.LEN)
        except (ValueError, IOError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == 'decode':
        try:
            decode(args.INPUT, args.OUTPUT)
        except (ValueError, IOError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()


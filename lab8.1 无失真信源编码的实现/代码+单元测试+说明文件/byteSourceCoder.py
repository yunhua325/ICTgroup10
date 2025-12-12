#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import io
import argparse

# Non-standard library
import numpy as np
from dahuffman_no_EOF import HuffmanCodec


def encode(pmf_file_name, in_file_name, out_file_name):
    """
    编码函数：将源文件编码为压缩文件
    
    参数:
        pmf_file_name: 概率质量函数CSV文件路径
        in_file_name: 输入源文件路径
        out_file_name: 输出编码文件路径
    
    返回:
        (源文件长度, 编码后长度) 元组
    """
    # 从CSV文件读取概率质量函数
    with open(pmf_file_name, newline='') as csv_file:
        pmf = dict([(np.uint8(row[0]), float(row[1])) for row in csv.reader(csv_file)])
    
    # 根据概率质量函数构建Huffman编码器
    codec = HuffmanCodec.from_frequencies(pmf)

    # 读取源文件（作为uint8数组）
    source = np.fromfile(in_file_name, dtype='uint8')
    
    # 使用Huffman编码器编码源数据
    encoded = codec.encode(source)

    # 获取码本（编码表）
    codebook = codec.get_code_table()
    byteorder = 'little'
    
    # 构建header
    # 先预留2字节用于存储header_size
    header = bytearray(2)
    
    # 添加符号数量（码本大小-1，因为uint8最大255，但可能有256个符号）
    header.append(len(codebook)-1)
    
    # 添加源文件长度（4字节，uint32）
    header.extend(len(source).to_bytes(4, byteorder))
    
    # 遍历码本，添加每个符号的编码信息
    for symbol, (word_len, word) in codebook.items():
        # 计算码字需要的字节数（向上取整）
        word_bytes = int(np.ceil(word_len / 8))
        
        header.append(symbol)
        
        header.append(word_len)
        
        header.extend(word.to_bytes(word_bytes, byteorder))
    
    # 将header的实际长度写入前2字节
    header[0:2] = len(header).to_bytes(2, byteorder)

    # 写入输出文件：先写header，再写编码后的数据
    with open(out_file_name, 'wb') as out_file:
        out_file.write(header)
        out_file.write(encoded)
    
    return (len(source), len(encoded))


def decode(in_file_name, out_file_name):
    """
    解码函数：将编码文件解码为源文件
    
    参数:
        in_file_name: 输入编码文件路径
        out_file_name: 输出解码文件路径
    
    返回:
        (编码文件长度, 解码后长度) 元组
    """
    
    byteorder = 'little'
    
    # 读取编码文件
    with open(in_file_name, 'rb') as in_file:
        # 读取header大小（前2字节）
        header_size = int.from_bytes(in_file.read(2), byteorder)
        
        # 读取header的剩余部分（header_size-2字节，因为前2字节是header_size本身）
        header = io.BytesIO(in_file.read(header_size-2))
        
        # 读取编码后的数据（剩余所有字节）
        encoded = in_file.read()
    
    # 从header中重建码本
    codebook = {}
    
    # 读取符号数量（1字节，实际符号数=该值+1）
    symbol_count = header.read(1)[0]
    
    # 读取源文件长度（4字节，uint32）
    source_len = int.from_bytes(header.read(4), byteorder)
    
    # 读取每个符号的编码信息
    for k in range(symbol_count+1):
        symbol = np.uint8(header.read(1)[0])
        
        word_len = header.read(1)[0]
        
        word_bytes = int(np.ceil(word_len / 8))
        
        word = int.from_bytes(header.read(word_bytes), byteorder)
        
        codebook[symbol] = (word_len, word)
    
    # 使用码本创建Huffman解码器
    codec = HuffmanCodec(codebook)
    
    # 解码数据，并截取到源文件长度（因为无EOF版本可能会多解码一些）
    decoded = np.asarray(codec.decode(encoded))[:source_len]
    
    # 将解码后的数据写入输出文件
    decoded.tofile(out_file_name)

    return (len(encoded), len(decoded))


def main():
    """主函数：解析命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(
        description='无失真信源编码程序',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s encode pmf.csv input.dat output.encoded
  %(prog)s decode output.encoded output.decoded
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # encode 命令
    encode_parser = subparsers.add_parser('encode', help='编码命令')
    encode_parser.add_argument('pmf', help='概率质量函数CSV文件路径')
    encode_parser.add_argument('input', help='编码器输入文件路径')
    encode_parser.add_argument('output', help='编码器输出文件路径')
    
    # decode 命令
    decode_parser = subparsers.add_parser('decode', help='解码命令')
    decode_parser.add_argument('input', help='解码器输入文件路径（编码后的文件）')
    decode_parser.add_argument('output', help='解码器输出文件路径')
    
    # 解析参数
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'encode':
            # 执行编码
            print(f"正在编码...")
            print(f"  PMF文件: {args.pmf}")
            print(f"  输入文件: {args.input}")
            print(f"  输出文件: {args.output}")
            
            source_len, encoded_len = encode(args.pmf, args.input, args.output)
            
            print(f"编码完成！")
            print(f"  源文件长度: {source_len} 字节")
            print(f"  编码后长度: {encoded_len} 字节")
            print(f"  压缩比: {source_len/encoded_len:.4f}")
            
        elif args.command == 'decode':
            # 执行解码
            print(f"正在解码...")
            print(f"  输入文件: {args.input}")
            print(f"  输出文件: {args.output}")
            
            encoded_len, decoded_len = decode(args.input, args.output)
            
            print(f"解码完成！")
            print(f"  编码文件长度: {encoded_len} 字节")
            print(f"  解码后长度: {decoded_len} 字节")
            
    except FileNotFoundError as e:
        print(f"错误：找不到文件 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


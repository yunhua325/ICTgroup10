""" A basic source coder.

This program is a basic demo showing a real-world example of source coding. The key point here is how to handle meta-data, such as codebook, so that decoder can get all necessary information to properly decode.

The format specification of the encoded file used here is:

Header  |header_size  : uint16, number of bytes for header
        |symbol_count : uint8, (number of symbols in codebook)-1
  ______|source_len   : uint32, number of symbols in source
  Code-1|symbol       : uint8, symbol
        |word_len     : uint8, number of bits for codeword
  ______|word         : ceil(word_len/8)*uint8, codeword
    ....|...
  ______|
  Code-n|symbol
        |word_len
________|word
Payload |encoded-data : many unit8

Note: This program is intended for use in course, Principle of Information and Coding Theory.

"""

import csv  # 导入CSV模块，用于读取概率质量函数文件
import io   # 导入输入输出模块，用于字节流操作

# Non-standard library
import numpy as np  # 导入NumPy库，用于数值计算和数组操作
from dahuffman_no_EOF import HuffmanCodec  # 导入自定义的Huffman编码器（老师已给dahuffman_no_EOF模块）

# 作者信息
__author__ = "Guo, Jiangling"
__email__ = "tguojiangling@jnu.edu.cn"
__version__ = "20201111.1702"

def encode(pmf_file_name, in_file_name, out_file_name):
    """编码函数：将输入文件编码为压缩文件"""
    # 读取概率质量函数文件并构建概率字典
    with open(pmf_file_name, newline='') as csv_file:
        pmf = dict([(np.uint8(row[0]), float(row[1])) for row in csv.reader(csv_file)])

    # 根据概率质量函数创建Huffman编码器
    codec = HuffmanCodec.from_frequencies(pmf)

    # 读取源文件数据
    source = np.fromfile(in_file_name, dtype='uint8')
    # 对源数据进行编码
    encoded = codec.encode(source)

    # 获取编码表（码本）
    codebook = codec.get_code_table()
    byteorder = 'little'  # 设置字节序为小端

    # 构建头部信息
    header = bytearray(2)  # 创建2字节的头部空间（用于存储头部大小）
    header.append(len(codebook)-1)  # 添加符号数量（码本大小-1）
    header.extend(len(source).to_bytes(4, byteorder))  # 添加源数据长度（4字节）

    # 遍历码本，将每个符号的编码信息添加到头部
    for symbol, (word_len, word) in codebook.items():
        (word_len, word) = codebook[symbol]  # 获取码字长度和码字
        word_bytes = int(np.ceil(word_len / 8))  # 计算码字需要的字节数
        header.append(symbol)  # 添加符号
        header.append(word_len)  # 添加码字长度
        header.extend(word.to_bytes(word_bytes, byteorder))  # 添加码字

    # 将头部大小写入头部的前2个字节
    header[0:2] = len(header).to_bytes(2, byteorder)

    # 将头部和编码数据写入输出文件
    with open(out_file_name, 'wb') as out_file:
        out_file.write(header)
        out_file.write(encoded)

    # 返回源数据长度和编码后数据长度
    return (len(source), len(encoded))

def decode(in_file_name, out_file_name):
    """解码函数：将压缩文件解码为原始文件"""

    byteorder = 'little'  # 设置字节序为小端
    with open(in_file_name, 'rb') as in_file:
        header_size = int.from_bytes(in_file.read(2), byteorder)  # 读取头部大小
        header = io.BytesIO(in_file.read(header_size-2))  # 读取头部内容（减去已读的2字节）
        encoded = in_file.read()  # 读取编码数据

    # 从头部重建码本
    codebook = {}
    symbol_count = header.read(1)[0]  # 读取符号数量
    source_len = int.from_bytes(header.read(4), byteorder)  # 读取源数据长度

    # 遍历头部，重建每个符号的编码信息
    for k in range(symbol_count+1):
        symbol = np.uint8(header.read(1)[0])  # 读取符号
        word_len = header.read(1)[0]  # 读取码字长度
        word_bytes = int(np.ceil(word_len / 8))  # 计算码字字节数
        word = int.from_bytes(header.read(word_bytes), byteorder)  # 读取码字
        codebook[symbol] = (word_len, word)  # 将符号和码字存入码本

    # 使用码本创建Huffman解码器
    codec = HuffmanCodec(codebook)
    # 解码数据并截取到源数据长度
    decoded = np.asarray(codec.decode(encoded))[:source_len]
    # 将解码数据写入输出文件
    decoded.tofile(out_file_name)

    # 返回编码数据长度和解码数据长度
    return (len(encoded), len(decoded))

def compare_file(file_name_1, file_name_2):
    """比较两个文件并统计不同字节的数量"""
    # 读取两个文件的数据
    data1 = np.fromfile(file_name_1, dtype='uint8')
    data2 = np.fromfile(file_name_2, dtype='uint8')

    # 确定比较的大小（取较小的大小）
    compare_size = min(data1.size, data2.size)
    # 如果文件大小不同，输出警告
    if data1.size != data2.size:
        print('[WARNING] These two files have different sizes (in bytes): %d vs %d' % (data1.size, data2.size))
        print('          Comparing the first %d bytes only.' % (compare_size))

    # 统计不同的字节数
    diff_total = np.sum(data1[:compare_size] != data2[:compare_size])
    print('Total %d bytes are different.' % (diff_total))

    return diff_total

def test():
    """测试函数：演示编码和解码过程"""
    test_data_dir = 'test-data/'  # 测试数据目录
    pmf_file_name = test_data_dir + 'pmf.byte.p0=0.8.csv'  # 概率质量函数文件
    source_file_name = test_data_dir + 'source.p0=0.8.len=64KB.dat'  # 源文件
    encoded_file_name = test_data_dir + '_encoded.tmp'  # 编码后文件
    decoded_file_name = test_data_dir + '_decoded.tmp'  # 解码后文件

    print('Encoding...')
    (source_len, encoded_len) = encode(pmf_file_name, source_file_name, encoded_file_name)
    print(' source len:', source_len)
    print('encoded len:', encoded_len)
    print('     ratio :', source_len/encoded_len)  # 计算压缩比
    print('')

    print('Decoding...')
    (encoded_len, decoded_len) = decode(encoded_file_name, decoded_file_name)
    print('encoded len:', encoded_len)
    print('decoded len:', decoded_len)
    print('')

    print('Comparing source and decoded...')
    compare_file(source_file_name, decoded_file_name)  # 比较源文件和解码文件
    print('')

if __name__ == '__main__':
    test()  # 如果直接运行此脚本，则执行测试函数

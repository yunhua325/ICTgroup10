#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二元对称信道（BSC）仿真程序
功能：将噪声文件作用在输入文件上，生成输出文件

程序API：
    byteChannel INPUT NOISE OUTPUT

参数说明：
    INPUT  - 输入文件路径（通过byteSource生成的二进制文件）
    NOISE  - 噪声文件路径（通过byteSource生成的二进制文件）
    OUTPUT - 输出文件路径（将NOISE作用在INPUT上的结果）

原理：
    在BSC中，将NOISE"作用"在INPUT上，实质上是逐字节进行XOR（异或）运算。
    对于每个字节，如果噪声位为1，则输出位翻转；如果噪声位为0，则输出位保持不变。
"""

import sys
import os


def byte_channel(input_path, noise_path, output_path):
    """
    将噪声文件作用在输入文件上，生成输出文件
    
    参数:
        input_path: 输入文件路径
        noise_path: 噪声文件路径
        output_path: 输出文件路径
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"错误: 输入文件 '{input_path}' 不存在", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(noise_path):
        print(f"错误: 噪声文件 '{noise_path}' 不存在", file=sys.stderr)
        sys.exit(1)
    
    try:
        # 以二进制模式打开文件
        with open(input_path, 'rb') as input_file, \
             open(noise_path, 'rb') as noise_file, \
             open(output_path, 'wb') as output_file:
            
            while True:
                # 逐字节读取
                input_byte = input_file.read(1)
                noise_byte = noise_file.read(1)
                
                # 如果输入文件已读完，结束
                if not input_byte:
                    break

                if not noise_byte:
                    noise_byte = b'\x00'
                
                # 执行XOR运算
                output_byte = bytes([input_byte[0] ^ noise_byte[0]])
                output_file.write(output_byte)
    
    except IOError as e:
        print(f"错误: 文件操作失败 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: 发生未知错误 - {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) != 4:
        print("用法: byteChannel INPUT NOISE OUTPUT", file=sys.stderr)
        print("", file=sys.stderr)
        print("参数说明:", file=sys.stderr)
        print("  INPUT  - 输入文件路径（通过byteSource生成的二进制文件）", file=sys.stderr)
        print("  NOISE  - 噪声文件路径（通过byteSource生成的二进制文件）", file=sys.stderr)
        print("  OUTPUT - 输出文件路径（将NOISE作用在INPUT上的结果）", file=sys.stderr)
        sys.exit(1)
    
    input_path = sys.argv[1]
    noise_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # 执行信道仿真
    byte_channel(input_path, noise_path, output_path)
    
    print(f"成功: 已将噪声文件 '{noise_path}' 作用在输入文件 '{input_path}' 上")
    print(f"      输出文件已保存到: '{output_path}'")


if __name__ == '__main__':
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实验2.4 - 256元DMS仿真

使用方法：
    python byteSource.py INPUT OUTPUT MSG_LEN

参数：
    INPUT      输入的概率分布CSV文件路径
    OUTPUT     输出的消息文件路径
    MSG_LEN    输出消息长度（符号数）

CSV文件格式：
    每行包含两个值：<symbol>,<probability>
    共256行，对应符号0-255
"""

import sys
import csv
import numpy as np
import argparse


def read_probability_distribution(input_file):
    """
    从CSV文件中读取概率分布
    
    参数:
        input_file (str): CSV文件路径
        
    返回:
        numpy.ndarray: 长度为256的概率分布数组
    """
    probabilities = np.zeros(256)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    symbol = int(row[0])
                    prob = float(row[1])
                    if 0 <= symbol <= 255:
                        probabilities[symbol] = prob
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
        sys.exit(1)
    except ValueError as e:
        print(f"错误：CSV文件格式错误 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：读取文件时发生错误 - {e}")
        sys.exit(1)
    
    # 验证概率分布
    total_prob = np.sum(probabilities)
    if abs(total_prob - 1.0) > 1e-6:
        print(f"概率分布总和为 {total_prob:.6f}，不等于1.0")
        # 归一化
        probabilities = probabilities / total_prob
        print("已归一化概率分布")
    
    return probabilities


def generate_message(probabilities, msg_len):
    """
    使用蒙特卡罗方法生成符合指定概率分布的消息序列
    
    参数:
        probabilities (numpy.ndarray): 概率分布数组
        msg_len (int): 消息长度
        
    返回:
        numpy.ndarray: 生成的消息序列
    """
    # 计算累积概率分布
    cumsum_probs = np.cumsum(probabilities)
    
    # 生成均匀分布的随机数
    random_values = np.random.uniform(0, 1, msg_len)
    
    # 找到对应的符号
    message = np.searchsorted(cumsum_probs, random_values)
    
    return message


def write_message(message, output_file):
    """
    将消息序列写入文件
    
    参数:
        message (numpy.ndarray): 消息序列
        output_file (str): 输出文件路径
    """
    try:
        # 将numpy数组转换为字节并写入文件
        message_bytes = message.astype(np.uint8).tobytes()
        with open(output_file, 'wb') as f:
            f.write(message_bytes)
        print(f"成功生成消息文件：{output_file}")
        print(f"消息长度：{len(message)} 个符号")
    except Exception as e:
        print(f"错误：写入文件时发生错误 - {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='离散无记忆信源（DMS）仿真程序',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', help='输入的概率分布CSV文件路径')
    parser.add_argument('output', help='输出的消息文件路径')
    parser.add_argument('msg_len', type=int, help='输出消息长度（符号数）')
    
    # 解析命令行参数
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # 验证消息长度
    if args.msg_len <= 0:
        print("错误：消息长度必须大于0")
        sys.exit(1)
    
    print("=" * 50)
    print("离散无记忆信源（DMS）仿真程序")
    print("=" * 50)
    print(f"输入文件：{args.input}")
    print(f"输出文件：{args.output}")
    print(f"消息长度：{args.msg_len}")
    print()
    
    # 读取概率分布
    print("正在读取概率分布...")
    probabilities = read_probability_distribution(args.input)
    print(f"概率分布读取完成，非零概率符号数：{np.count_nonzero(probabilities)}")
    
    # 生成消息
    print("正在生成消息序列...")
    message = generate_message(probabilities, args.msg_len)
    print("消息序列生成完成")
    
    # 写入文件
    print("正在写入文件...")
    write_message(message, args.output)
    
    print("\n程序执行完成！")


if __name__ == "__main__":
    main()

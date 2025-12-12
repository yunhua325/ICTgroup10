#!/usr/bin/env python3
import argparse
import csv
import math
import os
import sys
from typing import List, Tuple


def compute_entropy_bits(file_path: str, chunk_size: int = 1024 * 1024) -> Tuple[float, int]:
    """
    计算文件的信息熵和总字节数
    
    使用流式处理方式读取文件，避免大文件占用过多内存。
    基于香农熵公式计算：H(X) = -Σ p(x) * log2(p(x))
    
    参数:
        file_path: 输入文件路径
        chunk_size: 每次读取的块大小，默认1MB
        
    返回:
        Tuple[float, int]: (信息熵值(比特/字节), 文件总字节数)
        
    异常:
        FileNotFoundError: 文件不存在
        PermissionError: 权限不足
        OSError: 其他文件读取错误
    """
    # 初始化256个字节的直方图，对应0-255的所有可能字节值
    hist: List[int] = [0] * 256
    total = 0  # 总字节计数器
    
    with open(file_path, 'rb') as f:
        while True:
            # 分块读取文件，避免内存溢出
            chunk = f.read(chunk_size)
            if not chunk:  # 读到文件末尾
                break
                
            total += len(chunk)
            # 统计每个字节出现的次数
            for byte in chunk:
                hist[byte] += 1

    # 处理空文件情况
    if total == 0:
        return 0.0, 0

    # 计算信息熵
    entropy = 0.0
    inv_total = 1.0 / float(total)  
    
    # 遍历直方图，计算每个字节的熵贡献
    for count in hist:
        if count == 0:  # 跳过未出现的字节
            continue
            
        # 计算该字节的出现概率
        probability = count * inv_total
        # 累加熵值：-p * log2(p)
        entropy += -probability * math.log2(probability)
        
    return float(entropy), total


def append_csv_line(output_csv: str, input_path: str, entropy_bits: float, length_bytes: int) -> None:
    """
    将计算结果追加到CSV输出文件中
    
    按照实验要求的格式输出：
    "文件名","平均每个字节的信息量（比特）","文件长度（字节）"
    
    参数:
        output_csv: 输出CSV文件路径
        input_path: 输入文件路径
        entropy_bits: 计算得到的信息熵值
        length_bytes: 文件字节长度
        
    异常:
        PermissionError: 写入权限不足
        OSError: 文件写入错误
    """
    # 确保输出目录存在
    dirname = os.path.dirname(output_csv)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

    # 以追加模式打开CSV文件，保持UTF-8编码
    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        # 使用quoting=csv.QUOTE_ALL确保所有字段都被引号包围
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        # 写入一行数据，格式符合实验要求
        writer.writerow([
            input_path,                    # 原始文件名路径
            f"{entropy_bits:.6f}",        # 熵值，保留6位小数
            str(length_bytes)             # 文件大小，字符串格式
        ])


def main(argv: List[str]) -> int:
    """
    程序主函数
    
    处理命令行参数，协调文件读取、熵计算和结果输出。
    
    参数:
        argv: 命令行参数列表（不包含程序名）
        
    返回:
        int: 退出代码
            0 - 成功
            2 - 输入文件相关错误
            3 - 输出文件相关错误
    """
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(
        prog='calcInfo',
        description='计算文件的信息量',
        add_help=True,
        epilog='示例: calcInfo input.txt output.csv'
    )
    parser.add_argument(
        'INPUT', 
        help='待计算信息量的输入文件路径'
    )
    parser.add_argument(
        'OUTPUT', 
        help='存放计算结果的输出文件路径'
    )
    
    # 解析命令行参数
    args = parser.parse_args(argv)
    input_path = args.INPUT
    output_path = args.OUTPUT

    # 计算文件信息熵
    try:
        entropy_bits, total_bytes = compute_entropy_bits(input_path)
    except FileNotFoundError:
        print(f"错误: 找不到输入文件: {input_path}", file=sys.stderr)
        return 2
    except PermissionError:
        print(f"错误: 没有读取权限: {input_path}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"错误: 读取输入文件失败: {input_path}: {e}", file=sys.stderr)
        return 2

    # 将结果写入输出文件
    try:
        append_csv_line(output_path, input_path, entropy_bits, total_bytes)
        print(f"文件: {input_path}")
        print(f"信息量: {entropy_bits:.6f} 比特/字节")
        print(f"文件大小: {total_bytes} 字节")
        print(f"结果已保存到: {output_path}")
    except PermissionError:
        print(f"错误: 没有写入权限: {output_path}", file=sys.stderr)
        return 3
    except OSError as e:
        print(f"错误: 写入输出文件失败: {output_path}: {e}", file=sys.stderr)
        return 3

    return 0  


if __name__ == '__main__':
    # 程序入口点：从命令行参数启动主函数
    sys.exit(main(sys.argv[1:]))
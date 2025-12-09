import sys
import csv
from typing import Tuple

def read_file_bytes(file_path: str) -> bytes:
    """
    以二进制模式读取文件全部内容，处理文件不存在、权限不足等异常。
    :param file_path: 输入文件路径
    :return: 文件的二进制字节流
    :raises: 捕获常见IO异常并友好提示
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在，请检查路径是否正确。")
        sys.exit(1)
    except PermissionError:
        print(f"错误：没有读取文件 '{file_path}' 的权限。")
        sys.exit(1)
    except Exception as e:
        print(f"错误：读取文件 '{file_path}' 失败，原因：{str(e)}")
        sys.exit(1)

def calculate_bit_errors(bytes1: bytes, bytes2: bytes) -> Tuple[int, int]:
    """
    逐位对比两个字节流，统计总位数和错误位数。
    :param bytes1: 第一个文件的二进制字节流
    :param bytes2: 第二个文件的二进制字节流
    :return: (总位数, 错误位数)
    """
    total_bits = 0
    error_bits = 0

    # 取两个文件的最大长度，不足部分补0字节（避免长度不一致导致对比中断）
    max_length = max(len(bytes1), len(bytes2))
    bytes1_padded = bytes1.ljust(max_length, b'\x00')  # 不足部分补0
    bytes2_padded = bytes2.ljust(max_length, b'\x00')

    # 逐字节对比，每个字节拆分为8位
    for b1, b2 in zip(bytes1_padded, bytes2_padded):
        # 逐位比较（从高位到低位，即第7位到第0位）
        for bit_pos in range(7, -1, -1):
            # 提取当前位（用位掩码 & 128 >> bit_pos 实现）
            bit1 = (b1 >> bit_pos) & 1
            bit2 = (b2 >> bit_pos) & 1
            total_bits += 1
            if bit1 != bit2:
                error_bits += 1

    return total_bits, error_bits

def write_result_to_csv(input1: str, input2: str, error_rate: float, result_path: str) -> None:
    """
    将计算结果写入CSV文件，格式："INPUT1","INPUT2","error_rate"
    支持追加模式，如果文件存在则追加新行，否则创建新文件并写入表头。
    :param input1: 第一个输入文件路径
    :param input2: 第二个输入文件路径
    :param error_rate: 计算得到的误码率（保留6位小数）
    :param result_path: 结果CSV文件路径
    """
    try:
        import os
        
        # 检查文件是否存在，决定是否写入表头
        file_exists = os.path.exists(result_path)
        
        # 使用csv模块确保格式规范（处理路径中的逗号、引号等特殊字符）
        with open(result_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # 自动给字段加双引号
            
            # 如果文件不存在，先写入表头
            if not file_exists:
                writer.writerow(['INPUT1', 'INPUT2', 'error_rate'])
            
            # 写入数据行
            writer.writerow([input1, input2, round(error_rate, 6)])
        
        action = "保存到" if file_exists else "创建并写入"
        print(f"成功：结果已{action} '{result_path}'")
    except PermissionError:
        print(f"错误：没有写入文件 '{result_path}' 的权限。")
        sys.exit(1)
    except Exception as e:
        print(f"错误：写入结果文件失败，原因：{str(e)}")
        sys.exit(1)

def main():
    """
    主函数：解析命令行参数，调用上述函数完成误码率计算。
    命令行格式：calcErrorRate.py INPUT1 INPUT2 RESULT
    """
    # 检查命令行参数数量
    if len(sys.argv) != 4:
        print("用法错误：参数数量不正确！")
        print("正确格式：calcErrorRate.py INPUT1 INPUT2 RESULT")
        print("  INPUT1: 第一个对比文件的路径")
        print("  INPUT2: 第二个对比文件的路径")
        print("  RESULT: 结果CSV文件的保存路径")
        sys.exit(1)

    # 解析参数
    input1_path = sys.argv[1]
    input2_path = sys.argv[2]
    result_path = sys.argv[3]

    # 步骤1：读取两个文件的二进制数据
    print(f"正在读取文件：{input1_path} 和 {input2_path}...")
    bytes1 = read_file_bytes(input1_path)
    bytes2 = read_file_bytes(input2_path)

    # 步骤2：逐位对比，统计错误位数和总位数
    print("正在进行位级对比计算误码率...")
    total_bits, error_bits = calculate_bit_errors(bytes1, bytes2)

    # 步骤3：计算误码率（避免除零错误）
    if total_bits == 0:
        error_rate = 0.0
        print("警告：两个文件均为空，总位数为0，误码率设为0.0")
    else:
        error_rate = error_bits / total_bits

    # 步骤4：输出结果并写入CSV
    print(f"计算完成：")
    print(f"  总位数：{total_bits}")
    print(f"  错误位数：{error_bits}")
    print(f"  误码率：{error_rate:.6f}")
    write_result_to_csv(input1_path, input2_path, error_rate, result_path)

if __name__ == "__main__":
    main()

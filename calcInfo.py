import os
import csv
import argparse
import numpy as np

def read_input(file_path):
    """读取输入文件为字节数组"""
    try:
        x = np.fromfile(file_path, dtype='uint8')
        return x
    except Exception as e:
        print(f"错误: 无法读取文件 {file_path}: {e}")
        return None

def probability(x):
    """计算字节符号的近似概率分布"""
    hist = np.zeros(256)
    for k in x:
        hist[k] = hist[k] + 1
    P = hist/x.size
    return P

def self_info(P):
    """计算自信息量"""
    P = np.where(P == 0, np.spacing(1), P)
    return -np.log2(P)

def compute_info(x):
    """计算文件的平均信息量"""
    P = probability(x)
    info = np.sum(P * self_info(P))
    return info

def write_output(output_file, input_file, info, file_size):
    """将结果写入输出文件"""
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 写入CSV文件
    # 验证是否存在同名文件
    file_exists = os.path.isfile(output_file)

    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(['文件名', '平均每个字节的信息量（比特）', '文件长度（字节）'])
        
        # 写入数据
        writer.writerow([f'{input_file}', f"{info:.6f}", file_size])


def workflow(input_file, output_file):

    # 检查输入文件是否存在
    if not os.path.isfile(input_file):
        print(f"错误: 输入文件 {input_file} 不存在")
        return False

    x = read_input(input_file)
    if x is None:
        print(f"错误: 读取文件错误")
        return False

    info = compute_info(x=x)
    file_size = x.size

    write_output(output_file, input_file, info, file_size)

    return True

def test_workflow():
    """单元测试函数"""
    print("运行单元测试...")
    
    # 测试案例1：单一字节文件
    print("\n测试案例1: 单一字节文件")
    test_data = np.full(100, 65, dtype=np.uint8)  # 全部是'A'
    info = compute_info(test_data)
    print(f"理论值: 0.0, 实际值: {info:.6f}")
    
    # 测试案例2：均匀分布文件
    print("\n测试案例2: 均匀分布文件")
    test_data = np.repeat(np.arange(256, dtype=np.uint8), 4)  # 1024字节
    info = compute_info(test_data)
    print(f"理论值: 8.0, 实际值: {info:.6f}")
    
    # 测试案例3：二元等概率文件
    print("\n测试案例3: 二元等概率文件")
    test_data = np.array([0, 1] * 512, dtype=np.uint8)  # 1024字节
    info = compute_info(test_data)
    print(f"理论值: 1.0, 实际值: {info:.6f}")
    
    print("\n单元测试完成!")
    return True

def get_parser():
    parser = argparse.ArgumentParser(
        description='计算文件的信息量',
    )
    
    # 正常模式参数（作为可选的位置参数）
    parser.add_argument(
        "in_file_path", 
        nargs='?',  # 使位置参数变为可选的
        help="输入文件的路径（正常模式）"
    )
    parser.add_argument(
        "out_file_path", 
        nargs='?',  # 使位置参数变为可选的
        help="输出文件的路径（正常模式）"
    )
    
    # 测试模式参数
    parser.add_argument(
        "-t", "--test",
        dest="do_test",
        action="store_true", 
        help="运行单元测试（测试模式）"
    )
    
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.do_test:
        test_workflow()
    else:
        res = workflow(input_file=args.in_file_path, output_file=args.out_file_path)

        if res:
            print("处理完成!")
            return 0
        else:
            print("处理失败!")
            return 1

    return 0

if __name__ == '__main__':
    exit(main())
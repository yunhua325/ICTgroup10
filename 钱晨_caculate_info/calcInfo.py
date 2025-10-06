#!/usr/bin/env python3
import numpy as np
import os
import csv
import sys

# ------------------------------
# 检查命令行参数
# ------------------------------
if len(sys.argv) != 3:
    print("用法: calcInfo INPUT OUTPUT")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

# ------------------------------
# 检查输入文件是否存在
# ------------------------------
if not os.path.isfile(input_path):
    print(f"错误: 文件 '{input_path}' 不存在。")
    sys.exit(1)

# ------------------------------
# 从文件读取数据
# ------------------------------
x = np.fromfile(input_path, dtype='uint8')

# ------------------------------
# 定义计算函数
# ------------------------------
def probability(x):
    hist = np.zeros(256)
    for k in x:
        hist[k] += 1
    return hist / x.size

def entropy(P):
    P = np.where(P == 0, np.spacing(1), P)
    return -np.sum(P * np.log2(P))

# ------------------------------
# 执行计算
# ------------------------------
P = probability(x)
info = entropy(P)
file_size = os.path.getsize(input_path)
file_name = os.path.basename(input_path)

# ------------------------------
# 输出结果到CSV
# ------------------------------
header = ["文件名", "平均每个字节的信息量（比特）", "文件长度（字节）"]
data = [file_name, round(info, 4), file_size]

# 创建输出文件夹（如果没有）
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 检查是否需要写表头
write_header = not os.path.exists(output_path)

with open(output_path, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(header)
    writer.writerow(data)

print(f"✅ 计算完成！结果已保存到 {output_path}")
print(f"文件名: {file_name}")
print(f"平均每字节信息量: {info:.4f} 比特")
print(f"文件长度: {file_size} 字节")

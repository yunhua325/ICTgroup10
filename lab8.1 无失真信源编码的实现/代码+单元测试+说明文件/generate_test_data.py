# -*- coding: utf-8 -*-
"""
生成实验8.1单元测试所需的所有测试数据：
1. 3个PMF文件（概率分布CSV）
2. 3个源文件（短文本、单字节、64KB二进制）
仅显示当前脚本生成的文件清单
"""
import os
import csv
import numpy as np
from pathlib import Path

# --------------------------
# 配置：生成文件的输出目录（当前脚本所在目录）
# --------------------------
OUTPUT_DIR = Path(__file__).parent  # 所有测试数据放在脚本所在目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 记录当前脚本生成的文件（核心：仅跟踪自身生成的文件）
generated_files = []


def generate_pmf_file(file_path: Path, pmf_config: dict):
    """生成PMF（概率质量函数）CSV文件"""
    total_prob = sum(pmf_config.values())
    remaining_prob = 1.0 - total_prob
    remaining_symbols = [s for s in range(256) if s not in pmf_config.keys()]
    prob_per_remaining = remaining_prob / len(remaining_symbols)

    pmf_data = []
    for symbol in range(256):
        if symbol in pmf_config:
            prob = pmf_config[symbol]
        else:
            prob = prob_per_remaining
        pmf_data.append((symbol, round(prob, 8)))

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(pmf_data)

    generated_files.append(file_path)  # 记录生成的文件
    print(f"✅ PMF文件生成完成：{file_path.name}")
    print(f"  关键符号概率：{pmf_config}\n")


def generate_source_file(file_path: Path, content_type: str, **kwargs):
    """生成源文件（支持短文本、单字节、64KB二进制）"""
    if content_type == "text_short":
        text = kwargs.get("text", "abcabcabc")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        generated_files.append(file_path)
        print(f"✅ 短文本源文件生成完成：{file_path.name}")
        print(f"  内容：{text}")
        print(f"  大小：{os.path.getsize(file_path)}字节\n")

    elif content_type == "byte_single":
        byte_value = kwargs.get("byte_value", 120)
        assert 0 <= byte_value <= 255, "字节值必须在0-255之间"
        np.array([np.uint8(byte_value)]).tofile(file_path)
        generated_files.append(file_path)
        print(f"✅ 单字节源文件生成完成：{file_path.name}")
        print(f"  字节值：0x{byte_value:02x}（ASCII：{chr(byte_value) if 32<=byte_value<=126 else '非可打印字符'}）")
        print(f"  大小：{os.path.getsize(file_path)}字节\n")

    elif content_type == "binary_64kb":
        size_bytes = 64 * 1024
        prob_zero = 0.8
        num_zero = int(size_bytes * prob_zero)
        num_other = size_bytes - num_zero
        data = np.concatenate([
            np.zeros(num_zero, dtype=np.uint8),
            np.random.randint(1, 256, num_other, dtype=np.uint8)
        ])
        np.random.shuffle(data)
        data.tofile(file_path)
        generated_files.append(file_path)
        print(f"✅ 64KB二进制源文件生成完成：{file_path.name}")
        print(f"  大小：{os.path.getsize(file_path)}字节")
        print(f"  符号0占比：{np.sum(data == 0)/size_bytes:.4f}（预期0.8）\n")

    else:
        raise ValueError(f"不支持的内容类型：{content_type}")


if __name__ == "__main__":
    # --------------------------
    # 1. 生成3个PMF文件
    # --------------------------
    generate_pmf_file(
        file_path=OUTPUT_DIR / "pmf_test1.csv",
        pmf_config={97: 0.4, 98: 0.3, 99: 0.3}  # a:0.4, b:0.3, c:0.3
    )

    generate_pmf_file(
        file_path=OUTPUT_DIR / "pmf_test3.csv",
        pmf_config={120: 1.0}  # x:1.0
    )

    generate_pmf_file(
        file_path=OUTPUT_DIR / "pmf.byte.p0=0.8.csv",
        pmf_config={0: 0.8}  # 符号0:0.8
    )

    # --------------------------
    # 2. 生成3个源文件
    # --------------------------
    generate_source_file(
        file_path=OUTPUT_DIR / "source_test1.txt",
        content_type="text_short",
        text="abcabcabc"
    )

    generate_source_file(
        file_path=OUTPUT_DIR / "source_test3.dat",
        content_type="byte_single",
        byte_value=120  # x的ASCII码
    )

    generate_source_file(
        file_path=OUTPUT_DIR / "source.p0=0.8.len=64KB.dat",
        content_type="binary_64kb"
    )

    # --------------------------
    # 仅显示当前脚本生成的文件清单
    # --------------------------
    print("="*50)
    print(f"所有测试数据已生成至目录：{OUTPUT_DIR.absolute()}")
    print("当前脚本生成的文件清单：")
    for i, file in enumerate(generated_files, 1):
        print(f"  {i}. {file.name}（{os.path.getsize(file)}字节）")
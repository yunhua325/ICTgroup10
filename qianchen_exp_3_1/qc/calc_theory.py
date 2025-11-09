import numpy as np
import csv
import math


def entropy(p):
    """计算二元熵"""
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


# 计算所有组合的理论值
combinations = [
    (0.2, 0.2), (0.2, 0.5), (0.2, 0.9),
    (0.5, 0.2), (0.5, 0.5), (0.5, 0.9),
    (0.9, 0.2), (0.9, 0.5), (0.9, 0.9)
]

with open('results.expect.csv', 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(['X', 'Y', 'H(X)', 'H(Y)', 'H(XY)', 'H(X|Y)', 'H(Y|X)', 'I(X;Y)', 'p'])

    for p0, p in combinations:
        # 计算各个理论值
        H_x = entropy(p0)
        H_y_given_x = entropy(p)

        # 计算输出概率 P(Y=0) = p*p0 + (1-p)*(1-p0)
        py0 = p * p0 + (1 - p) * (1 - p0)
        H_y = entropy(py0)

        # 计算互信息
        I_xy = H_x + H_y - H_x - H_y_given_x  # 简化为 I(X;Y) = H(Y) - H(Y|X)

        # 计算后验熵
        H_x_given_y = H_x - I_xy

        # 联合熵
        H_xy = H_x + H_y_given_x

        # 写入结果
        x_file = f"DMS.p0={p0}.len=1000.bin"
        y_file = f"BSC.p={p}.DMS.p0={p0}.len=1000.bin"
        writer.writerow([x_file, y_file, H_x, H_y, H_xy, H_x_given_y, H_y_given_x, I_xy, p])

print("理论值计算完成！")
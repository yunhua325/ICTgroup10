import subprocess
import os
import numpy as np
import csv
import math

def entropy(p):
    """计算二进制熵函数"""
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1-p) * math.log2(1-p)

def main():
    # 设置工作目录
    os.chdir('c:\\Users\\钱晨\\Desktop\\ICTgroup10\\qianchen_exp_3_1\\qc')
    
    # 定义所有实验组合 (p0, p)
    combinations = [
        (0.2, 0.2), (0.2, 0.5), (0.2, 0.9),
        (0.5, 0.2), (0.5, 0.5), (0.5, 0.9),
        (0.9, 0.2), (0.9, 0.5), (0.9, 0.9)
    ]
    
    # 删除旧的results.csv
    if os.path.exists('results.csv'):
        os.remove('results.csv')
    
    print("=== 开始实验3.1任务5 ===")
    print("正在计算实际值...")
    
    # 计算所有9组实际值
    for p0, p in combinations:
        x_file = f"experiment/experiment/DMS.p0={p0}.len=1000.bin"
        y_file = f"experiment/experiment/BSC.p={p}.DMS.p0={p0}.len=1000.bin"
        
        cmd = f"python calcBSCInfo.py {x_file} {y_file} results.csv"
        print(f"计算: p0={p0}, p={p}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
        else:
            print(f"✓ 完成")
    
    print("实际值计算完成！")
    
    # 计算理论值
    print("正在计算理论值...")
    
    with open('results.expect.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['X', 'Y', 'H(X)', 'H(Y)', 'H(XY)', 'H(X|Y)', 'H(Y|X)', 'I(X;Y)', 'p'])
        
        for p0, p in combinations:
            # 理论计算
            H_x = entropy(p0)  # H(X)
            H_y_given_x = entropy(p)  # H(Y|X)
            
            # 计算输出概率 py0 = p(Y=0)
            py0 = p * p0 + (1-p) * (1-p0)
            H_y = entropy(py0)  # H(Y)
            
            # 互信息 I(X;Y) = H(Y) - H(Y|X)
            I_xy = H_y - H_y_given_x
            
            # 条件熵 H(X|Y) = H(X) - I(X;Y)
            H_x_given_y = H_x - I_xy
            
            # 联合熵 H(X,Y) = H(X) + H(Y|X)
            H_xy = H_x + H_y_given_x
            
            x_file = f"DMS.p0={p0}.len=1000.bin"
            y_file = f"BSC.p={p}.DMS.p0={p0}.len=1000.bin"
            
            writer.writerow([x_file, y_file, H_x, H_y, H_xy, H_x_given_y, H_y_given_x, I_xy, p])
    
    print("理论值计算完成！")
    
    # 显示结果
    print("\n=== 实验完成 ===")
    print("生成的文件：")
    print("- results.csv (实际计算结果)")
    print("- results.expect.csv (理论预期结果)")
    
    # 显示前3行结果
    print("\n实际结果预览：")
    with open('results.csv', 'r') as f:
        for i, line in enumerate(f):
            if i < 4:
                print(line.strip())
    
    print("\n理论结果预览：")
    with open('results.expect.csv', 'r') as f:
        for i, line in enumerate(f):
            if i < 4:
                print(line.strip())

if __name__ == '__main__':
    main()
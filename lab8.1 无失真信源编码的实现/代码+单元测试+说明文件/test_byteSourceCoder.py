import os
import sys
from pathlib import Path
from byteSourceCoder import encode, decode 

def file_exists(file_path):
    """检查文件是否存在"""
    if not os.path.exists(file_path):
        print(f"❌ 错误：文件不存在 - {file_path}")
        return False
    if not os.path.isfile(file_path):
        print(f"❌ 错误：不是有效文件 - {file_path}")
        return False
    return True

def test_single_file(pmf_file, source_file):
    """测试单个文件的编码和解码流程"""
    # 检查输入文件
    if not (file_exists(pmf_file) and file_exists(source_file)):
        return False

    # 临时文件命名（避免覆盖）
    encoded_file = f"temp_encoded_{os.getpid()}.dat"
    decoded_file = f"temp_decoded_{os.getpid()}.dat"

    try:
        # 1. 执行编码
        print("\n[1/3] 执行编码...")
        source_size = os.path.getsize(source_file)
        print(f"  源文件长度：{source_size}字节")
        
        encode(pmf_file, source_file, encoded_file)
        encoded_size = os.path.getsize(encoded_file)
        print(f"  编码后长度：{encoded_size}字节")
        print(f"  压缩比：{source_size / encoded_size:.4f}")

        # 2. 执行解码
        print("[2/3] 执行解码...")
        decode(encoded_file, decoded_file)  # 注意这里修正了解码函数的参数顺序
        decoded_size = os.path.getsize(decoded_file)
        print(f"  解码后长度：{decoded_size}字节")

        # 3. 对比文件
        print("[3/3] 对比文件...")
        with open(source_file, 'rb') as f1, open(decoded_file, 'rb') as f2:
            if f1.read() == f2.read():
                print("✅ 文件完全一致")
                result = True
            else:
                print("❌ 文件不一致")
                result = False

    except Exception as e:
        print(f"❌ 处理失败：{str(e)}")
        result = False

    finally:
        # 清理临时文件
        for f in [encoded_file, decoded_file]:
            if os.path.exists(f):
                os.remove(f)
                print(f"  清理临时文件：{f}")

    return result

def main():
    # 添加当前目录到Python路径（解决导入问题）
    current_dir = str(Path(__file__).parent)
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    # 终端交互逻辑
    print("=== 字节流编码解码器测试工具 ===")
    pmf_file = input("请输入PMF概率文件路径：").strip()
    
    # 验证PMF文件有效性
    if not file_exists(pmf_file):
        print("PMF文件无效，程序退出")
        sys.exit(1)
    
    print("\n请输入待测试源文件路径（空行结束）：")
    file_list = []
    while True:
        source_file = input().strip()
        if not source_file:  # 空行退出输入
            break
        file_list.append(source_file)
    
    if not file_list:
        print("没有输入任何待测试文件，程序退出")
        sys.exit(0)
    
    # 批量测试文件
    all_success = True
    for i, source_file in enumerate(file_list, 1):
        print(f"\n=== 开始测试文件 {i}/{len(file_list)}: {source_file} ===")
        success = test_single_file(pmf_file, source_file)
        if not success:
            all_success = False
    
    print("\n=== 测试结束 ===")
    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()
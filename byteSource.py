import sys
import csv

def main():
    if len(sys.argv) != 4:
        print("用法: python byteSource.py 输入文件 输出文件 消息长度")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        msg_len = int(sys.argv[3])
    except ValueError:
        print("消息长度必须为整数！")
        sys.exit(1)
    # 这里可以根据你的实验需求，读取 input_file，生成 msg_len 长度的输出，并写入 output_file
    # 示例：直接复制 input_file 的前 msg_len 字节到 output_file
    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        data = fin.read(msg_len)
        fout.write(data)
    print(f"已生成 {output_file}，长度 {msg_len} 字节")

if __name__ == "__main__":
    main()
# repetitionCoder.py 说明

## 运行环境

- **Python版本**: Python 3.x
- **依赖库**: `bitstring`
- **操作系统**: Windows / Linux / macOS

## 安装依赖

在使用本程序前，需要安装 `bitstring` 库：

```bash
pip install bitstring
```

## 使用方法

### 编码命令

```bash
python repetitionCoder.py encode LEN INPUT OUTPUT
```

**参数说明：**
- `LEN`: 重复码的码字长度，必须是**奇数**，且满足 **2 < n < 10**（即只能是 3, 5, 7, 9）
- `INPUT`: 输入文件路径（支持任意格式的文件）
- `OUTPUT`: 编码后的输出文件路径

**示例：**
```bash
python repetitionCoder.py encode 3 input.txt output.enc
python repetitionCoder.py encode 5 data.bin encoded_data.enc
```

### 解码命令

```bash
python repetitionCoder.py decode INPUT OUTPUT
```

**参数说明：**
- `INPUT`: 编码后的输入文件路径（必须是使用本程序编码生成的文件）
- `OUTPUT`: 解码后的输出文件路径

**示例：**
```bash
python repetitionCoder.py decode output.enc decoded.txt
python repetitionCoder.py decode encoded_data.enc decoded_data.bin
```

## 文件格式

### 编码输出文件格式

`encode` 命令生成的输出文件具有以下格式：

| 字段 | 大小 | 说明 |
|------|------|------|
| LEN | 1 字节 | 重复码的码字长度（3, 5, 7, 或 9） |
| source length | 4 字节 | 源文件的比特数（小端序） |
| codeword sequence | 多个字节 | 编码后的码字序列 |



### 编码原理

- 对于源文件中的每个比特：
  - 如果比特为 `0`，则编码为 `000...0`（n个0）
  - 如果比特为 `1`，则编码为 `111...1`（n个1）

### 解码原理

- 读取文件头获取码长 `n` 和源文件比特数
- 将码字序列按 `n` 个比特分组
- 对每组使用多数表决：
  - 统计该组中 `1` 的个数
  - 如果 `1` 的个数 > `n/2`，则解码为 `1`
  - 否则解码为 `0`

## 使用示例

### 示例1：基本编码解码

```bash
# 1. 创建测试文件
echo "Hello, World!" > test.txt

# 2. 编码（使用码长3）
python repetitionCoder.py encode 3 test.txt test.enc

# 3. 解码
python repetitionCoder.py decode test.enc test_decoded.txt

# 4. 验证结果（Windows）
fc test.txt test_decoded.txt

# 4. 验证结果（Linux/Mac）
diff test.txt test_decoded.txt
```

### 示例2：使用不同码长

```bash
# 使用码长5进行编码
python repetitionCoder.py encode 5 input.txt output_5.enc

# 使用码长7进行编码
python repetitionCoder.py encode 7 input.txt output_7.enc

# 使用码长9进行编码
python repetitionCoder.py encode 9 input.txt output_9.enc
```

### 示例3：处理二进制文件

```bash
# 编码二进制文件
python repetitionCoder.py encode 3 image.jpg image_encoded.enc

# 解码
python repetitionCoder.py decode image_encoded.enc image_decoded.jpg
```

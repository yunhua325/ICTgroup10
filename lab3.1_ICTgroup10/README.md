# 二元对称信道（BSC）仿真程序：byteChannel.py

## 代码功能
`byteChannel.py` 是一个用于模拟二元对称信道（BSC）的 Python 脚本，主要功能包括：
- 将噪声文件（NOISE）作用在输入文件（INPUT）上，生成输出文件（OUTPUT）。
- 通过逐字节的 XOR（异或）运算模拟 BSC 信道的行为：
  - 若噪声位为 `1`，则输出位翻转。
  - 若噪声位为 `0`，则输出位保持不变。

## byteChannel.py使用说明
1. **运行脚本**：
   - 使用以下命令运行程序：
     ```bash
     python byteChannel.py INPUT NOISE OUTPUT 
     ```
   - 示例1：
     ```bash
     python byteChannel.py input.dat noise.dat output.dat
     ```
   - 示例2：
     ```bash
     python byteChannel.py experiment\DMS.p0=0.9.len=1048576.bin experiment\NOISE.p=0.9.len=1048576.bin experiment\BSC.p=0.9.DMS.p0=0.9.len=1048576.bin
     ```
    
2. **参数说明**：
| 参数 | 说明 | 示例 |
|------|------|------|
| `INPUT` | 输入文件路径，通过 `byteSource` 生成的二进制文件 |
| `NOISE` | 噪声文件路径，通过 `byteSource` 生成（按错误传递概率 p 生成）的二进制文件，表示信道噪声 | 
| `OUTPUT` | 输出文件路径，将 `NOISE` 作用在 `INPUT` 上的结果 ，与输入文件长度相同（如果噪声文件较短，超出部分用 0 填充）| 
（注意：其中错误传递概率 p = P（1））

## 其他所需程使用说明
1. **calcBSCInfo.py（计算信道各指标）**：
   - 使用以下命令运行程序：
     ```bash
     python calcBSCInfo.py X Y OUTPUT 
     ```
   - 示例1：
     ```bash
     python calcBSCInfo.py input.dat output.dat results.csv
     ```
   - 示例2：
     ```bash
     python calcBSCInfo.py experiment\DMS.p0=0.9.len=1048576.bin experiment\BSC.p=0.9.DMS.p0=0.9.len=1048576.bin experiment\results.csv

2. **unit-test.cmd（批量计算信道各指标，运行在unit-test目录下）**：
     ```bash
     unit-test.cmd
     ```

3. **experiment.cmd（批量计算信道各指标，运行在experiment目录下）**：
     ```bash
     experiment.cmd
     ```

## 单元测试简述
1. **测试方法**：
   - 准备三个较为特殊的测试用例（即三个简单的仿真信道，含输入文件、噪声文件、输出文件在内）。
   - 验证输出文件内容是否符合预期（通过手动计算 XOR 结果）。

2. **测试脚本**：
   - 结合 `unit-test.cmd` 进行批量测试。

## 文件目录结构
```
实验3.1/
└── 已弃用.len=1000（文件夹）               # 弃用的实验数据目录（消息序列长度太短，实验误差太大）
├── experiment/                          # 实验数据目录
│   ├── DMSorNOISE.csv（文件夹）                 # 输入文件、噪声文件的概率分布文件
│   ├── DMS.*.bin                              # DMS开头的文件为输入文件
│   ├── NOISE.*.bin                            # NOISE开头的文件为噪声文件
│   ├── BSC.*.bin                              # BSC开头的文件为输出文件
│   ├── results.csv                            # 实验结果文件（实验值）
│   └── results.expect.csv                     # 实验结果预期文件（理论值）
├── unit-test/                           # 单元测试数据目录
│   ├── DMSorNOISE.csv（文件夹）                 # 单元测试输入文件、噪声文件的概率分布文件
│   ├── result（文件夹）                         # 放置单元测试输出文件
│   ├── DMS.*.bin                              # DMS开头的文件为单元测试输入文件
│   ├── NOISE.*.bin                            # NOISE开头的文件为单元测试噪声文件
│   ├── BSC.*.bin                              # BSC开头的文件为单元测试输出文件
│   ├── results.csv                            # 单元测试结果文件（实验值）
│   └── results.expect.csv                     # 单元测试结果预期文件（理论值）
├── lab3.1 二元对称信道（BSC）仿真_实验报告.docx    
├── lab3.1 单元测试报告.docx                
├── byteChannel.py                       # 二元对称信道仿真程序
├── calcBSCInfo.py                       # BSC信道信息计算程序
├── experiment.cmd                       # 实验运行脚本（在experiment目录下运行）
├── README.md                            # 说明文档
└── unit-test.cmd                        # 单元测试运行脚本（在unit-test目录下运行）
```

## 注意事项
- 一定要保证输入文件和噪声文件的准确性（即概率分布文件一定要准确，且保留的小数数位不能太少），否则会对实验结果产生较大影响。
- 输入文件和噪声文件的最好都比较长，否则计算结果会不准确。（本组已尝试过len=1000，实验值与理论值误差会非常大，因为绝大多数(x_byte, y_byte) 组合在样本中从未出现，其概率被错误地估计为0）
- 输出文件会覆盖同名文件，需确保路径正确。
- 若噪声文件比输入文件短，不足部分会自动补零。
- 使用.cmd的脚本调用calcBSCInfo.py批量时，需要先确保理论值results.expect.csv存在。

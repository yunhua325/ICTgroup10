@echo off
REM 这个批处理文件用来让你在命令行直接输入 calcInfo 来运行 Python 程序
python "%~dp0calcInfo.py" %*

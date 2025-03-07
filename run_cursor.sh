#!/bin/bash
# 激活 conda 环境
source ~/miniconda3/etc/profile.d/conda.sh  # 请根据你的 miniconda 安装路径调整
conda activate robodiff                  # robodiff 为你的环境名称

# 取消可能影响运行的环境变量（例如 PYTHONHOME）
unset PYTHONHOME

# 启动 cursor（假设 cursor 的可执行文件路径正确）
/path/to/cursor/executable "$@" 
#!/bin/bash
# 医学文献检索系统运行脚本

# 检查是否提供了疾病名称
if [ -z "$1" ]; then
    echo "使用方法: ./run.sh <疾病名称> [其他参数]"
    echo "示例: ./run.sh 糖尿病"
    echo "示例: ./run.sh 高血压 --max-results 50"
    exit 1
fi

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.installed" ]; then
    echo "安装依赖包..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到 .env 文件，请从 .env.example 复制并配置"
    echo "执行: cp .env.example .env"
    echo "然后编辑 .env 文件填入你的 API 密钥"
    exit 1
fi

# 运行程序
echo "开始运行..."
python3 src/main.py --disease "$@"

# 保持虚拟环境激活状态
echo ""
echo "程序运行完成！"

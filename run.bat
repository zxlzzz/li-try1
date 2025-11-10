@echo off
REM 医学文献检索系统运行脚本 (Windows)

if "%1"=="" (
    echo 使用方法: run.bat 疾病名称 [其他参数]
    echo 示例: run.bat 糖尿病
    echo 示例: run.bat 高血压 --max-results 50
    exit /b 1
)

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.7+
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
if not exist "venv\.installed" (
    echo 安装依赖包...
    pip install -r requirements.txt
    echo. > venv\.installed
)

REM 检查 .env 文件
if not exist ".env" (
    echo 警告: 未找到 .env 文件，请从 .env.example 复制并配置
    echo 执行: copy .env.example .env
    echo 然后编辑 .env 文件填入你的 API 密钥
    exit /b 1
)

REM 运行程序
echo 开始运行...
python src\main.py --disease %*

echo.
echo 程序运行完成！
pause

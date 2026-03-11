@echo off
chcp 65001
cd %~dp0
if not exist .run (
    echo 正在安装依赖……
    pip install -r requirements.txt
    echo.>.run
)
echo 正在复制文件
rd /s /q run_build 2>nul
mkdir run_build
copy main.py run_build\main.py
xcopy /s /e /y tools run_build
cd run_build
python main.py
cd ..
@echo off
chcp 65001
cd %~dp0
if not exist .run (
    echo 正在安装依赖……
    pip install -r requirements.txt
    echo.>.run
)
echo 正在复制文件
main\adb.exe kill-server 2>nul
rd /s /q main 2>nul
mkdir main
copy main.py main\main.py
xcopy /s /e /y scripts main
xcopy /s /e /y include main
xcopy /s /e /y tools main
cd main
python main.py
cd ..

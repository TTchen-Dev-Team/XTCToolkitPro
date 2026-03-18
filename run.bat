@echo off
chcp 65001
cd %~dp0
if not exist .run (
    echo 正在安装依赖……
    pip install -r requirements.txt
    echo 请下载adb调试工具、scrcpy等相关工具至tools文件夹！
    pause
    if not exist tools (
        goto check
    )
)
:start
echo.>.run
echo 正在尝试结束adb服务……
main\adb.exe kill-server 2>nul
echo 正在复制文件
rd /s /q main 2>nul
mkdir main
copy main.py main\main.py
xcopy /s /e /y scripts main
xcopy /s /e /y include main
xcopy /s /e /y tools main
cd main
python main.py
cd ..
exit /b
:check
echo 未检测到tools文件夹！
echo 请下载adb调试工具、scrcpy等相关工具至tools文件夹！
pause
if not exist tools (
    goto check
)
goto start
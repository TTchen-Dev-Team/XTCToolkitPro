@echo off
chcp 65001 > nul
INFO 正在复制文件……
adb wait-for-device push %1 /sdcard/Download/temp_module.zip
if %errorlevel% neq 0 (
    ERROR 安装失败！
    exit /b 1
)
INFO 正在安装模块……
adb wait-for-device shell "su -c magisk--install-module /sdcard/Download/temp_module.zip"
if %errorlevel% neq 0 (
    ERROR 安装失败！
    INFO 清理临时文件……
    adb wait-for-device shell rm /sdcard/Download/temp_module.zip
    exit /b 1
)
INFO 清理临时文件……
adb wait-for-device shell rm /sdcard/Download/temp_module.zip
if %errorlevel% neq 0 (
    ERROR 安装失败！
    exit /b 2
)
DONE 安装成功！
@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set "warningMsg=[WARN]"
echo | set /p="[33m%warningMsg%[0m"
echo %*

endlocal
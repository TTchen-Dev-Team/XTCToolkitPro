@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set "errorMsg=[ERROR]"
echo | set /p="[31m%errorMsg%[0m"
echo %*

endlocal
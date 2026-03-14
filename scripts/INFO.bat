@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set "infoMsg=[INFO]"
echo | set /p="[34m%infoMsg%[0m"
echo %*

endlocal
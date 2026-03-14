@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set "infoMsg=[DONE]"
echo | set /p="[32m%infoMsg%[0m"
echo %*

endlocal
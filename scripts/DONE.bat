@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
set "infoMsg=[DONE]"
echo | set /p="[32m%infoMsg%[0m"
echo %*
endlocal
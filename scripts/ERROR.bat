@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
set "infoMsg=[ERROR]"
echo | set /p="[31m%infoMsg%[0m"
echo %*
endlocal
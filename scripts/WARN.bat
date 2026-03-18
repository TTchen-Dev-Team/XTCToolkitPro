@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
set "infoMsg=[WARN]"
echo | set /p="[33m%infoMsg%[0m"
echo %*
endlocal
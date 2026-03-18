@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
set "infoMsg=[DEBUG]"
echo | set /p="[35m%infoMsg%[0m"
echo %*
endlocal
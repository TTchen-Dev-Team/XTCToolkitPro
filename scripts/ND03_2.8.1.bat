@echo off
chcp 65001
cd /d %~dp0
call .\fh_loader.exe --port=\\.\COM6 --memoryname=EMMC --search_path=. --sendxml=.\EDL\ND03_2.8.1\rawprogram0.xml --noprompt
if %errorlevel% neq 0 (
    exit /b 1
)
call .\fh_loader.exe --port=\\.\COM6 --memoryname=EMMC --search_path=. --sendxml=.\EDL\ND03_2.8.1\rawprogram1.xml --noprompt
if %errorlevel% neq 0 (
    exit /b 1
)
call .\fh_loader.exe --port=\\.\COM6 --memoryname=EMMC --search_path=. --sendxml=.\EDL\ND03_2.8.1\rawprogram2.xml --noprompt
if %errorlevel% neq 0 (
    exit /b 1
)
call .\fh_loader.exe --port=\\.\COM6 --memoryname=EMMC --search_path=. --sendxml=.\EDL\ND03_2.8.1\patch0.xml --noprompt
if %errorlevel% neq 0 (
    exit /b 1
)
exit /b 0
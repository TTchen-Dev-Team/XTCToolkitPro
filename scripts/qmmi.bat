@echo off
chcp 65001

set /p model=%1
if "!model!" == "1" set innermodel=I20&goto FLASH-QMMI 
if "!model!" == "2" set innermodel=I25&goto FLASH-QMMI
if "!model!" == "3" set innermodel=I25C&goto FLASH-QMMI
if "!model!" == "4" set innermodel=I25D&goto FLASH-QMMI
if "!model!" == "5" set innermodel=I32&goto FLASH-QMMI
if "!model!" == "6" set innermodel=ND07&goto FLASH-QMMI
if "!model!" == "7" set innermodel=ND01&goto FLASH-QMMI
if "!model!" == "8" set innermodel=ND03&goto FLASH-QMMI-S

:FLASH-QMMI
call INFO 您的机型: %innermodel%
call INFO 请接入要刷写的设备
adb wait-for-device reboot edl >nul
device_check qcom_edl&&ECHO.
call qcomport
call INFO 复制文件到临时目录
copy /Y .\EDL\misc\misc.img .\tmp\misc.img
copy /Y .\EDL\misc\misc_%innermodel%.xml .\tmp\misc.xml
call INFO 发送引导
call QSaharaServer.bat -p \\.\COM%chkdev__edl__port% -s 13:".\EDL\msm8937.mbn"
call INFO 开始刷写misc
call fh_loader --port=\\.\COM%chkdev_edl_port% --memoryname=emmc --search_path=tmp\ --sendxml=tmp\misc.xml --noprompt
call INFO 重启手表
call qfh_loader --port=\\.\COM%chkdev_edl_port% --memoryname=emmc --search_path=tmp\ --sendxml=reboot.xml --noprompt
call INFO 删除临时文件
del /Q /F .\tmp\misc.xml
del /Q /F .\tmp\misc.img
call INFO 已进入qmmi模式!
call INFO 三秒后跳转到对应界面
timeout /t 3 /nobreak >nul
exit /b

:FLASH-QMMI-S
call INFO 您的机型: %innermodel%
call INFO 请接入要刷写的设备
adb wait-for-device reboot edl >nul
device_check qcom_edl&&ECHO.
call qcomport
call INFO 复制文件到临时目录
copy /Y .\EDL\misc\misc.img .\tmp\misc.img
copy /Y .\EDL\misc\misc_ND03.xml .\tmp\misc.xml
call INFO 发送引导
call QSaharaServer.bat -p \\.\COM%chkdev__edl__port% -s 13:".\EDL\prog_firehose_ddr.elf"
call INFO 开始刷写misc
call fh_loader --port=\\.\COM%chkdev_edl_port% --memoryname=emmc --search_path=tmp\ --sendxml=tmp\misc.xml --noprompt
call INFO 重启手表
call qfh_loader --port=\\.\COM%chkdev_edl_port% --memoryname=emmc --search_path=tmp\ --sendxml=reboot.xml --noprompt
call INFO 删除临时文件
del /Q /F .\tmp\misc.xml
del /Q /F .\tmp\misc.img
call INFO 已进入qmmi模式!
call INFO 三秒后跳转到对应界面
timeout /t 3 /nobreak >nul
exit /b

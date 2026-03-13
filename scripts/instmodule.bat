adb wait-for-device push %1 /sdcard/Download/temp_module.zip
adb wait-for-device shell "su -c magisk--install-module /sdcard/Download/temp_module.zip"
adb wait-for-device shell rm /sdcard/Download/temp_module.zip
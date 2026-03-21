from msvcrt import getch

from prompt_toolkit import print_formatted_text, HTML, prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

import tkinter as tk
from tkinter import filedialog

import os

import traceback

import getcode

import random

import requests

version = "v0.2.6-alpha.1"
version_short = "0.2.6a1"

debug_mode = True
update_mode = False

style = Style.from_dict({
    'error': 'fg:ansired',
    'warning': 'fg:ansiyellow',
    'success': 'fg:ansigreen',
    'info': 'fg:ansiblue',
    'debug': 'fg:ansipurple'
})

error = "<error>[ERROR]</error>"
warning = "<warning>[WARN]</warning>"
success = "<success>[DONE]</success>"
info = "<info>[INFO]</info>"
debug = "<debug>[DEBUG]</debug>"

def clear():
    os.system("cls")

def check_update():
    if update_mode:
        print_formatted_text(HTML(info+"正在检测更新……"), style=style)
        try:
            response = requests.get("https://api.github.com/repos/TTWatchBox-Team/TTWatchBox/releases/latest")
            version_now = response.json()["tag_name"]
            if version_now != version:
                print_formatted_text(HTML(info+"检测到新版本，请前往 GitHub 下载！"), style=style)
            print_formatted_text(HTML(info+"没有到新版本"), style=style)
        except Exception as e:
            print_formatted_text(HTML(error+f"检测更新失败！错误原因：{e}！"), style=style)
            if debug_mode:
                print_formatted_text(HTML(debug+"详细错误原因："), style=style)
                traceback.print_exc()
    else:
        print_formatted_text(HTML(warning+f"检测更新已被禁用！"), style=style)

def pre_menu():
    clear()
    os.system("lolcat logo.txt")
    print_formatted_text(HTML(info+"欢迎来到TTWatchBox！"), style=style)
    print_formatted_text(HTML(info+"正在启动adb服务……"), style=style)
    if os.system("adb start-server"):
        print_formatted_text(HTML(error+"启动失败！"), style=style)
    else:
        print_formatted_text(HTML(success+"启动完成！"), style=style)
    check_update()
    print_formatted_text(HTML(warning+"你现在正在使用开发版本"), style=style)
    if debug_mode:
        print_formatted_text(HTML(debug+"调试模式已开启！"), style=style)
    print_formatted_text(HTML(warning+"关于版权：由于玩机工具或多或少都会涉及版权问题，因此本工具仅供技术交流，请不要商用，下载后24小时删除！"), style=style)
    print_formatted_text(HTML(warning+"关于版权：如果您实在觉得我们严重侵犯了您的版权，请立刻联系作者整改删除"), style=style)
    print_formatted_text(HTML(warning+"关于解绑：本工具不提供任何解绑服务，如果您捡到了手表，请立刻联系当地110机关归还原主"), style=style)
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键进入 &lt;</ansibrightblack>"), style=style, end='')
    getch()

def about():
    clear()
    os.system("lolcat logo.txt")
    print("="*50)
    print("作者 TT_chen")
    print("TTWatchBox Team 开发")
    print("="*50)
    print("开发版本 "+version)
    print("开发版本存在较多未知的bug，非开发人员请勿使用此版本！！！")
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键退出 &lt;</ansibrightblack>"), style=style, end='')
    getch()

def debug_menu():
    global debug_mode
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        result = choice(message="",options=[
            ("color","色卡"),
            ("off","关闭调试模式[仅本次运行]"),
            ("exit","退出")])
        if result == "color":
            clear()
            print_formatted_text(HTML(info+"信息"), style=style)
            print_formatted_text(HTML(warning+"警告"), style=style)
            print_formatted_text(HTML(error+"错误"), style=style)
            print_formatted_text(HTML(success+"成功"), style=style)
            print_formatted_text(HTML(debug+"调试"), style=style)
            print()
            os.system("INFO bat信息")
            os.system("WARN bat警告")
            os.system("ERROR bat错误")
            os.system("DONE bat成功")
            os.system("DEBUG bat调试")
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "off":
            debug_mode = False
            return
        elif result == "exit":
            break
    clear()

def tools():
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        result = choice(message="",options=[
            ("scrcpy","传屏"),
            ("image","导入图片"),
            ("vedio","导入视频"),
            ("getcode_zj","计算自检校验码"),
            ("getcode_adb","计算ADB校验码[仅支持V2以下]"),
            ("qmmi","进入qmmi"),
            ("exit","退出")])
        if result == "exit":
            break
        elif result == "scrcpy":
            clear()
            print_formatted_text(HTML(info+"正在打开传屏……"), style=style)
            if os.system("scrcpy"):
                print_formatted_text(HTML(error+"传屏失败！"), style=style)
            else:
                print_formatted_text(HTML(success+"传屏完成！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "image":
            clear()
            root = tk.Tk()
            root.withdraw()
            file_types = [
                ("图片", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.ai *.cdr *.eps"),
                ("所有文件", "*.*")
            ]
            file_path = filedialog.askopenfilename(
                title="选择图片",
                filetypes=file_types
            )
            root.destroy()
            if file_path:
                os.system("device_check adb")
                print()
                if os.system("adb wait-for-device push \""+file_path+"\" /storage/emulated/0/DCIM/Camera"):
                    print_formatted_text(HTML(error+"传入失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"传入完成！"), style=style)
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        elif result == "vedio":
            clear()
            root = tk.Tk()
            root.withdraw()
            file_types = [
                ("视频", "*.mp4"),
                ("所有文件", "*.*")
            ]
            file_path = filedialog.askopenfilename(
                title="选择视频",
                filetypes=file_types
            )
            root.destroy()
            if file_path:
                os.system("device_check adb")
                print()
                if os.system("adb wait-for-device push \""+file_path+"\" /storage/emulated/0/DCIM/Video/TTWatchBox"+str(random.randint(11111,99999))+".mp4"):
                    print_formatted_text(HTML(error+"传入失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"传入完成！"), style=style)
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        elif result == "getcode_zj":
            clear()
            print_formatted_text(HTML(info+"请输入要计算的校验码："), style=style, end="")
            code = input()
            new_code = getcode.get_code(code, "zj")
            if new_code:
                print_formatted_text(HTML(info+"动态校验码："+new_code), style=style, end="")
            else:
                print_formatted_text(HTML(error+"校验码格式错误！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "getcode_adb":
            clear()
            print_formatted_text(HTML(info+"请输入要计算的校验码："), style=style, end="")
            code = input()
            new_code = getcode.get_code(code, "adb")
            if new_code:
                print_formatted_text(HTML(info+"动态校验码："+new_code), style=style, end="")
            else:
                print_formatted_text(HTML(error+"校验码格式错误！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
            """
        elif result == "qmmi":
            qmmi()"""
        else:
            clear()
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

def apk_menu():
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        result = choice(message="",options=[
            ("install","安装应用"),
            ("installmodule","安装模块"),
            ("exit","退出")])
        if result == "exit":
            break
        elif result == "install":
            clear()
            root = tk.Tk()
            root.withdraw()
            file_types = [
                ("APK文件", "*.apk"),
                ("所有文件", "*.*")
            ]
            file_path = filedialog.askopenfilename(
                title="选择APK文件",
                filetypes=file_types
            )
            root.destroy()
            if file_path:
                os.system("device_check adb")
                print()
                if os.system("adb wait-for-device install \""+file_path+"\""):
                    print_formatted_text(HTML(error+"安装失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"安装完成！"), style=style)
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        elif result == "installmodule":
            clear()
            print_formatted_text(HTML(warning+"安装模块需谨慎，操作不慎可能导致设备变砖！！！"), style=style)
            root = tk.Tk()
            root.withdraw()
            file_types = [
                ("ZIP文件", "*.zip"),
                ("所有文件", "*.*")
            ]
            file_path = filedialog.askopenfilename(
                title="选择ZIP文件",
                filetypes=file_types
            )
            root.destroy()
            if file_path:
                os.system("device_check adb")
                print()
                os.system("instmodule \""+file_path+"\"")
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        else:
            clear()
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

def links():
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        result = choice(message="",options=[
            ("0","超级恢复文件"),
            ("1","应用合集"),
            ("2","早茶の网盘备份"),
            ("exit","退出")])
        links_list=[
            "https://www.123865.com/s/Q5JfTd-hEbWH",
            "https://www.123684.com/s/Q5JfTd-ZEbWH",
            "https://www.123865.com/s/nFXhvd-Fdpod"
        ]
        if result == "exit":
            break
        else:
            os.system("start "+links_list[int(result)])

def menu():
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        options=[
            ("root","一键root"),
            ("apks","应用与模块管理"),
            ("cmd","在此处打开cmd[含adb调试环境]"),
            ("about","关于脚本"),
            ("tools","常用工具"),
            ("links","链接合集"),
            ("dev_tools","高级菜单"),
            ("wifi","无线连接[尝鲜版]"),
            ("mods","模块商店"),
            ("check_update","检测更新"),
            ("exit","退出")]
        if debug_mode:
            options.append(("debug","调试菜单"))
        result = choice(message="",options=options)
        if result == "cmd":
            clear()
            print_formatted_text(HTML(info+"已进入cmd，输入exit退出"), style=style)
            os.system("set \"PROMPT=(TTWatchBox) %PROMPT%\" && cmd")
        elif result == "about":
            about()
        elif result == "exit":
            clear()
            os.system("adb kill-server")
            break
        elif result == "debug":
            debug_menu()
        elif result == "tools":
            tools()
        elif result == "apks":
            apk_menu()
        elif result == "wifi":
            clear()
            adb_ip = prompt("请输入IP地址：", history=FileHistory('history_ip.txt'), auto_suggest=AutoSuggestFromHistory())
            adb_port = prompt("请输入端口：", history=FileHistory('history_port.txt'), auto_suggest=AutoSuggestFromHistory())
            os.system("adb connect "+adb_ip+":"+adb_port)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "links":
            links()
        elif result == "check_update":
            clear()
            check_update()
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        else:
            clear()
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

if __name__ == "__main__":
    try:
        os.system("title TTWatchBox"+version_short+" by TTchen")
        pre_menu()
        menu()
    except KeyboardInterrupt:
        clear()
        print_formatted_text(HTML(warning+"检测到用户中断，正在安全退出程序……"), style=style)
        os.system("adb kill-server")
        print_formatted_text(HTML(info+"退出成功！"), style=style)
    except Exception as e:
        clear()
        print_formatted_text(HTML(error+f"程序出现错误！错误原因：{e}，请立刻反馈于开发者！！！"), style=style)
        if debug_mode:
            print_formatted_text(HTML(debug+"详细错误原因："), style=style)
            traceback.print_exc()

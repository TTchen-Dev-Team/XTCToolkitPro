from msvcrt import getch

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import choice

import tkinter as tk
from tkinter import filedialog

import sys

import os

import getcode

import random

style = Style.from_dict({
    'error': 'fg:ansired',
    'warning': 'fg:ansiyellow',
    'success': 'fg:ansigreen',
    'info': 'fg:ansiblue',
    'debug': 'fg:violet'
})

error = "<error>[ERROR]</error>"
warning = "<warning>[WARN]</warning>"
success = "<success>[DONE]</success>"
info = "<info>[INFO]</info>"
debug = "<debug>[DEBUG]</debug>"

def clear():
    os.system("cls")

def pre_menu():
    clear()
    os.system("lolcat logo.txt")
    print_formatted_text(HTML(info+"欢迎来到TTWatchBox！"), style=style)
    print_formatted_text(HTML(info+"正在启动adb服务……"), style=style)
    if os.system("adb start-server"):
        print_formatted_text(HTML(error+"启动失败！"), style=style)
    else:
        print_formatted_text(HTML(success+"启动完成！"), style=style)
    print_formatted_text(HTML(warning+"你现在正在使用开发版本"), style=style)
    print_formatted_text(HTML(warning+"调试模式已开启！"), style=style)
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
    print("开发版本 v0.2.5-alpha.1")
    print("开发版本存在较多未知的bug，非开发人员请勿使用此版本！！！")
    print("本版本bug比一般开发版本更多，请谨慎使用！！！")
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键退出 &lt;</ansibrightblack>"), style=style, end='')
    getch()

def debug_menu():
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        result = choice(message="",options=[
            ("color","色卡"),
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
        elif result == "exit":
            break
    clear()

"""
def qmmi():
    while True:
        clear()
        os.system("lolcat logo.txt")
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 自由，从每一次突破开始 -"), style=style, end='')
        result = choice(message="",options=[
            ("1","Z6DFB"),
            ("2","Z7"),
            ("3","Z7A"),
            ("4","Z7S"),
            ("5","Z8"),
            ("6","Z8A"),
            ("7","Z9"),
            ("8","Z10"),
            ("exit","退出")])
        if result == "exit":
            break
        else:
            clear()
            os.system("qmmi "+result)
"""

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
                if os.system("device_check adb && adb wait-for-device push \""+file_path+"\" /storage/emulated/0/DCIM/Camera"):
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
                if os.system("device_check adb && adb wait-for-device push \""+file_path+"\" /storage/emulated/0/DCIM/Video/TTWatchBox"+str(random.randint(11111,99999))+".mp4"):
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
                if os.system("device_check adb && adb wait-for-device install \""+file_path+"\""):
                    print_formatted_text(HTML(error+"安装失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"安装完成！"), style=style)
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        elif result == "installmodule":
            clear()
            print_formatted_text(HTML(warning+"安装模块需谨慎，操作不可能导致设备变砖！！！"), style=style)
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
                if os.system("instmodule \""+file_path+"\""):
                    print_formatted_text(HTML(error+"安装失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"安装完成！"), style=style)
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
        result = choice(message="",options=[
            ("root","一键root"),
            ("apks","应用与模块管理"),
            ("cmd","在此处打开cmd[含adb调试环境]"),
            ("about","关于脚本"),
            ("tools","常用工具"),
            ("links","链接合集"),
            ("dev_tools","高级菜单"),
            ("wifi","无线连接[尝鲜版]"),
            ("mods","模块商店"),
            ("debug","调试菜单"),
            ("exit","退出")])
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
            print_formatted_text(HTML(info+"请输入IP地址："), style=style, end="")
            adb_ip = input()
            print_formatted_text(HTML(info+"请输入端口："), style=style, end="")
            adb_port = input()
            os.system("adb connect "+adb_ip+":"+adb_port)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "links":
            links()
        else:
            clear()
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

if __name__ == "__main__":
    os.system("title TTWatchBox by TTchen")
    pre_menu()
    menu()

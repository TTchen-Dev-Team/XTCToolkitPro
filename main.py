from msvcrt import getch

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import choice

import tkinter as tk
from tkinter import filedialog

import os

import getcode

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

logo =r"""
 __  _______ ____ _____           _ _    _ _   ____            
 \ \/ /_   _/ ___|_   _|__   ___ | | | _(_) |_|  _ \ _ __ ___  
  \  /  | || |     | |/ _ \ / _ \| | |/ / | __| |_) | '__/ _ \ 
  /  \  | || |___  | | (_) | (_) | |   &lt;| | |_|  __/| | | (_) |
 /_/\_\ |_| \____| |_|\___/ \___/|_|_|\_\_|\__|_|   |_|  \___/
"""

def pre_menu():
    os.system("cls")
    print_formatted_text(HTML(logo), style=style)
    print_formatted_text(HTML(info+"欢迎来到XTCToolkitPro！"), style=style)
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
    os.system("cls")
    print_formatted_text(HTML(logo), style=style)
    print("="*50)
    print("作者 TT_chen & 衍曲")
    print("TTchen Dev Team 开发")
    print("="*50)
    print("开发版本 v0.2.0-alpha.1")
    print("开发版本存在较多未知的bug，非开发人员请勿使用此版本！！！")
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键退出 &lt;</ansibrightblack>"), style=style, end='')
    getch()

def debug_menu():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 不被定义，才能创造定义 -"), style=style, end='')
        result = choice(message="",options=[
            ("color","色卡"),
            ("exit","退出")])
        if result == "color":
            os.system("cls")
            print_formatted_text(HTML(info+"信息"), style=style)
            print_formatted_text(HTML(warning+"警告"), style=style)
            print_formatted_text(HTML(error+"错误"), style=style)
            print_formatted_text(HTML(success+"成功"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "exit":
            break
    os.system("cls")

def tools():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 不被定义，才能创造定义 -"), style=style, end='')
        result = choice(message="",options=[
            ("scrcpy","传屏"),
            ("image","导入图片"),
            ("getcode_zj","计算自检校验码"),
            ("getcode_adb","计算ADB校验码[仅支持V2以下]"),
            ("exit","退出")])
        if result == "exit":
            break
        elif result == "scrcpy":
            os.system("cls")
            print_formatted_text(HTML(info+"正在打开传屏……"), style=style)
            if os.system("scrcpy"):
                print_formatted_text(HTML(error+"传屏失败！"), style=style)
            else:
                print_formatted_text(HTML(success+"传屏完成！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        elif result == "image":
            os.system("cls")
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
                if os.system("adb push \""+file_path+"\" /storage/emulated/0/DCIM/Camera"):
                    print_formatted_text(HTML(error+"传入失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"传入完成！"), style=style)
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        elif result == "getcode_zj":
            os.system("cls")
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
            os.system("cls")
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
        else:
            os.system("cls")
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

def apk_menu():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 不被定义，才能创造定义 -"), style=style, end='')
        result = choice(message="",options=[
            ("install","安装应用"),
            ("exit","退出")])
        if result == "exit":
            break
        elif result == "install":
            os.system("cls")
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
                if os.system("adb install \""+file_path+"\""):
                    print_formatted_text(HTML(error+"安装失败！"), style=style)
                else:
                    print_formatted_text(HTML(success+"安装完成！"), style=style)
                print()
                print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
                getch()
        else:
            os.system("cls")
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

def links():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 不被定义，才能创造定义 -"), style=style, end='')
        result = choice(message="",options=[
            ("0","超级恢复文件（来自ATB）"),
            ("1","应用合集"),
            ("exit","退出")])
        links_list=[
            "https://www.123865.com/s/Q5JfTd-hEbWH",
            "https://www.123684.com/s/Q5JfTd-ZEbWH"
        ]
        if result == "exit":
            break
        else:
            os.system("start "+links_list[int(result)])

def menu():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style)
        print_formatted_text(HTML(info+"- 不被定义，才能创造定义 -"), style=style, end='')
        result = choice(message="",options=[
            ("root","一键root"),
            ("apks","应用与模块管理"),
            ("cmd","在此处打开cmd[含adb调试环境]"),
            ("about","关于脚本"),
            ("tools","常用工具"),
            ("links","链接合集"),
            ("more_menu","高级菜单"),
            ("wifi","无线连接[尝鲜版]"),
            ("debug","调试菜单"),
            ("exit","退出")])
        if result == "cmd":
            os.system("cls")
            print_formatted_text(HTML(info+"已进入cmd，输入exit退出"), style=style)
            os.system("cmd")
        elif result == "about":
            about()
        elif result == "exit":
            os.system("cls && adb kill-server")
            break
        elif result == "debug":
            debug_menu()
        elif result == "tools":
            tools()
        elif result == "apks":
            apk_menu()
        elif result == "wifi":
            os.system("cls")
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
            os.system("cls")
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print()
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

if __name__ == "__main__":
    os.system("title \"XTCToolkitPro by TTchen & 衍曲\"")
    pre_menu()
    menu()

from msvcrt import getch

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import choice

import os

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

logo = """████████╗████████╗██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗██████╗  ██████╗ ██╗  ██╗
╚══██╔══╝╚══██╔══╝██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██╔═══██╗╚██╗██╔╝
   ██║      ██║   ██║ █╗ ██║███████║   ██║   ██║     ███████║██████╔╝██║   ██║ ╚███╔╝
   ██║      ██║   ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║██╔══██╗██║   ██║ ██╔██╗ 
   ██║      ██║   ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║██████╔╝╚██████╔╝██╔╝ ██╗
   ╚═╝      ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝"""

def pre_menu():
    os.system("cls")
    print_formatted_text(HTML(logo), style=style)
    print_formatted_text(HTML(warning+"你现在正在使用开发版本"), style=style)
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键进入 &lt;</ansibrightblack>"), style=style, end='')
    getch()

def about():
    os.system("cls")
    print_formatted_text(HTML(logo), style=style)
    print("="*50)
    print("作者 TT_chen")
    print("="*50)
    print("开发版本 v0.1.0")
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键退出 &lt;</ansibrightblack>"), style=style, end='')
    getch()

def debug():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style, end='')
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
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style, end='')
        result = choice(message="",options=[
            ("scrcpy","传屏"),
            ("install","安装应用"),
            ("exit","退出")])
        if result == "exit":
            break
        elif result == "scrcpy":
            os.system("cls")
            print_formatted_text(HTML(info+"正在打开传屏……"), style=style)
            if os.system("scrcpy"):
                print_formatted_text(HTML(error+"传屏失败！"), style=style)
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()
        else:
            os.system("cls")
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

def menu():
    while True:
        os.system("cls")
        print_formatted_text(HTML(logo), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style, end='')
        result = choice(message="",options=[
            ("root","一键root"),
            ("apks","应用与模块管理"),
            ("cmd","在此处打开cmd[含adb调试环境]"),
            ("about","关于脚本"),
            ("tools","常用工具"),
            ("menu","高级菜单"),
            ("debug","调试菜单"),
            ("exit","退出")])
        if result == "cmd":
            os.system("cls")
            print_formatted_text(HTML(info+"已进入cmd，输入exit退出"), style=style)
            os.system("cmd")
        elif result == "about":
            about()
        elif result == "exit":
            os.system("cls")
            break
        elif result == "debug":
            debug()
        elif result == "tools":
            tools()
        else:
            os.system("cls")
            print_formatted_text(HTML(warning+"功能开发中！"), style=style)
            print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键继续 &lt;</ansibrightblack>"), style=style, end='')
            getch()

if __name__ == "__main__":
    os.system("title TTWatchBox by TTchen")
    pre_menu()
    menu()
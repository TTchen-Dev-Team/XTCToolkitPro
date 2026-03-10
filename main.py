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
    print_formatted_text(HTML("<ansiwhite>"+logo+"</ansiwhite>"), style=style)
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键进入  &lt;</ansibrightblack>"), style=style, end='')
    getch()

def about():
    os.system("cls")
    print_formatted_text(HTML("<ansiwhite>"+logo+"</ansiwhite>"), style=style)
    print("="*50)
    print("作者 TT_chen")
    print("="*50)
    print("开发版本 v0.1.0")
    print()
    print_formatted_text(HTML("<ansibrightblack>&gt; 请按任意键退出  &lt;</ansibrightblack>"), style=style, end='')
    getch()

def menu():
    while True:
        os.system("cls")
        print_formatted_text(HTML("<ansiwhite>"+logo+"</ansiwhite>"), style=style)
        print_formatted_text(HTML(info+"请使用方向键/数字键选择一个选项，按Enter确认。"), style=style, end='')
        result = choice(message="",options=[
            ("1","在此处打开cmd"),
            ("2","关于脚本"),
            ("3","退出")])
        if result == "1":
            os.system("cls && cmd")
        elif result == "2":
            about()
        elif result == "3":
            break
    os.system("cls")

if __name__ == "__main__":
    os.system("title TTWatchBox by TTchen")
    pre_menu()
    menu()
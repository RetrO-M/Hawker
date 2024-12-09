import time
import os
import shutil
from colorama import Fore, init

init()

ascii1 = f"""
{Fore.LIGHTCYAN_EX}██████╗ ███████╗ █████╗ ██████╗ ██╗   ██╗         
██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝         
██████╔╝█████╗  ███████║██║  ██║ ╚████╔╝          
██╔══██╗██╔══╝  ██╔══██║██║  ██║  ╚██╔╝           
██║  ██║███████╗██║  ██║██████╔╝   ██║            
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝
{Fore.LIGHTWHITE_EX}            ╔═══════════╗
          ╔═╝███████████╚═╗
         ╔╝███████████████╚╗
         ║█╔█████████████╗█║
         ╚╦╝███  ███  ███╚╦╝
         ╔╝██    ███    ██╚╗
         ║██ {Fore.LIGHTRED_EX} •{Fore.LIGHTWHITE_EX}  ███ {Fore.LIGHTRED_EX} •{Fore.LIGHTWHITE_EX}  ██║
         ║██    █████    ██║
         ╚╗███████████████╔╝
      ╔═╗ ╚══╦╝██ █ ██╚╦══╝ ╔═╗
      ║█║    ║█████████║    ║█║
      ║█║    ║█║██║██║█║    ║█║ 
      ║█║    ╚═╩══╩══╩═╝    ║█║
     ╔╝█╚══╗             ╔══╝█╚╗
    ╔╝█████║ ╔═╦══╦══╦═╗ ║█████╚╗
    ║██████║ ║█║██║██║█║ ║██████║
             ║█████████║
"""
ascii2 = f"""
{Fore.LIGHTCYAN_EX}██████╗ ███████╗ █████╗ ██████╗ ██╗   ██╗         
██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝         
██████╔╝█████╗  ███████║██║  ██║ ╚████╔╝          
██╔══██╗██╔══╝  ██╔══██║██║  ██║  ╚██╔╝           
██║  ██║███████╗██║  ██║██████╔╝   ██║            
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝
  {Fore.LIGHTWHITE_EX}          ╔═══════════╗
          ╔═╝███████████╚═╗
         ╔╝███████████████╚╗
         ║█╔█████████████╗█║
         ╚╦╝███  ███  ███╚╦╝
         ╔╝██    ███    ██╚╗
         ║██  {Fore.LIGHTRED_EX}•{Fore.LIGHTWHITE_EX}  ███ {Fore.LIGHTRED_EX} • {Fore.LIGHTWHITE_EX} ██║
         ║██    █████    ██║
         ╚╗███████████████╔╝
      ╔═╗ ╚══╦╝██ █ ██╚╦══╝ ╔═╗
      ║█║    ║█████████║    ║█║
      ║█║    ║█║██║██║█║    ║█║ 
      ║█║    ╚═╩══╩══╩═╝    ║█║
     ╔╝█╚══╗ ╔═╦══╦══╦═╗ ╔══╝█╚╗
    ╔╝█████║ ║█║██║██║█║ ║█████╚╗
    ║██████║ ║█████████║ ║██████║
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_ascii(ascii_art):
    columns, rows = shutil.get_terminal_size()
    ascii_lines = ascii_art.strip().split('\n')
    num_lines = len(ascii_lines)
    max_width = max(len(line) for line in ascii_lines)

    vertical_margin = (rows - num_lines) // 2
    horizontal_margin = (columns - max_width) // 2

    return '\n' * vertical_margin + '\n'.join(' ' * horizontal_margin + line for line in ascii_lines)

def start_time():
    duration = 5
    start_time = time.time()

    while time.time() - start_time < duration:
        clear_screen()
        print(center_ascii(ascii1))
        time.sleep(0.1)

        clear_screen()
        print(center_ascii(ascii2))
        time.sleep(0.2)

    clear_screen()

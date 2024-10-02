from colorama import Fore, Back, Style, init

init()

def underline_text(text):
    print(Back.WHITE + Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)

def command2():
    underline_text("Command           |       Description                          ")
    print(
        f"""  phone           |       View information about a phone number
  email           |       Show information by email
  ip              |       View information about an IP address
  search          |       View a person's social media using their username"""
    )


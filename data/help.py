from colorama import Fore, Back, Style, init

init()

def underline_text(text):
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + text + Style.RESET_ALL)

def help():
    print(
           f"""{Fore.WHITE} 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠖⠋⠉⠉⠉⣫⣒⠲⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠎⠀⠀⠀⠀⠀⠚⣳⢿⣦⡄⠈⠳⡀⠀⣠⡤⠤⣄⠀⠀⠀⢀⣤⣤⣶⣶⣤⣀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⣮⣭⡀⠀⠀⠀⠀⠻⣌⡿⠃⠀⠀⠘⣼⠁⠀⠀⠈⠳⡄⠀⣯⢹⣿⣭⡖⠒⠺⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⢰⡹⣇⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⢹⡀⠘⡟⠁⠀⢳⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⣄⡀⣧⠀⠉⠉⠀⡀⠀⠀⣀⡼⡆⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⢷⠀⢹⡀⠀⠈⣇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡎⠀⠀⠀⠉⢿⡄⠀⠀⠀⠙⠋⠉⠁⠀⠉⠀⠀⠀⠀⠀⠀⡇⠀⢰⡀⠀⠀⠘⣆⠀⡇⠀⠀⢸⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⢣⠀⠀⠀⠘⣦⠇⠀⠀⢀⡇⠀
⠀⠀⠀⠀⠀⣠⠤⢤⠀⠀⠀⢸⠀⠀⠀⠀⢠⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠋⠀⠀⠀⠈⢳⣄⠀⠀⠉⠀⠀⠀⢸⠁⠀
⠀⠀⠀⣠⣾⡿⠧⠈⣧⠀⠀⢸⡄⠀⠀⠀⢠⡇⠀⠀⠀⠉⠙⠒⠒⠒⠤⠤⠤⠴⠒⠉⠀⠀⠀⠀⠀⠀⢸⠘⢦⡀⠀⠀⠀⢀⡟⠀⠀
⠀⣴⣿⣽⠇⠀⢀⣠⠾⢧⠀⠈⡇⠀⠀⠀⠠⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠈⠉⠓⠋⠁⠀⠀⠀
⣞⣥⡴⠒⠲⣶⠋⠀⠀⠘⣆⠀⢳⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠉⠁⠀⠀⢹⡄⠀⠀⠀⠈⠑⠚⠀⠀⠀⣸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢷⡀⠀⠀⠀⠀⠀⠀⠀⢀⠇⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        {Fore.RESET}"""
        + f"\t{Fore.BLUE}- {Fore.YELLOW}Educational Purposes Only{Fore.RESET}\n"
    )
    underline_text("\tI'm not encouraging anyone to harass or hack, please respect!")
    print(
        f"""   
{Fore.MAGENTA}-{Fore.GREEN} This OSINT tool has been created to assist cybersecurity professionals, law enforcement, and security 
researchers in conducting legal and ethical investigations on email addresses, in compliance with applicable 
laws. Any malicious use, such as harassment, fraud, or illegal activities, is strictly prohibited.

{Fore.MAGENTA}-{Fore.GREEN} The creator of this tool disclaims any responsibility for improper use. Any attempt to exploit this tool
for illegal purposes may result in legal consequences. Please use this tool responsibly and only for legitimate 
investigative purposes.

{Fore.MAGENTA}-{Fore.GREEN} We encourage all users to exercise common sense and integrity when utilizing this tool. The goal of this
tool is to promote transparency and security on the Internet, not to facilitate harmful or malicious behavior. Be aware of the 
ethical implications of your actions and remember that cybersecurity relies on respecting and protecting others.

{Fore.WHITE} Type “command” or “! » to display the tool commands
    {Fore.RESET}"""
    )

import re
from colorama import Fore, init

init()

async def check_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    if re.match(email_regex, email):
        print(f"{Fore.GREEN}Valid email format -> {email}")
    else:
        print(f"{Fore.RED}Invalid email format -> {email}")

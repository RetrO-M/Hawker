import hashlib
import aiohttp
from colorama import Fore, init

init()

async def check_gravatar_email(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://en.gravatar.com/{email_hash}.json"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                display_name = data['entry'][0].get('displayName', 'Unknown')
                print(f"{Fore.YELLOW}Gravatar Account Found: https://gravatar.com/{display_name}")
            elif response.status == 404:
                print(f"{Fore.RED}No Gravatar account associated with this email -> EMAIL : {email}")
            else:
                print(f"Error : {Fore.RED}{response.status}")

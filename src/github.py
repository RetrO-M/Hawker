import aiohttp
from colorama import Fore, init

init()

async def check_github_email(email):
    url = f"https://api.github.com/search/users?q={email}+in:email"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.json()
                if result["total_count"] > 0:
                    print(f"{Fore.YELLOW}GitHub Account Found: https://github.com/{result['items'][0]['login']}")
                else:
                    print(f"{Fore.RED}No GitHub account associated with this email -> EMAIL : {email}")
            else:
                print(f"Error: {Fore.RED}{response.status}")

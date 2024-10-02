import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore, init

init()

async def pornhub(target: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://fr.pornhub.com/signup") as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                token = soup.find(attrs={'name': 'token'}).get('value')

            params = {'token': token}
            data = {
                'check_what': 'email', 
                'email': target
            }

            async with session.post("https://fr.pornhub.com/user/create_account_check", params=params, data=data) as api:
                response_json = await api.json()

                if response_json.get('email') == "create_account_passed":
                    print(f"{Fore.RED}No Pornhub account associated with this email")
                elif response_json.get('email') == "create_account_failed":
                    print(f"{Fore.YELLOW}Pornhub Account Found")
                else:
                    print(f"{Fore.RED}No Pornhub account associated with this email")

    except Exception as e:
        pass

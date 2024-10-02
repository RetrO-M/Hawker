import aiohttp
from colorama import Fore, init

init()

async def check_duolingo_email(target: str):
    url = "https://www.duolingo.com/2017-06-30/users"
    params = {'email': target}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    text_response = await response.text()

                    if '{"users":[]}' in text_response:
                        print(f"{Fore.RED}No Duolingo account associated with this email")
                    else:
                        valid = (await response.json())['users'][0]['username']
                        print(f"{Fore.YELLOW}Duolingo Account Found")

                else:
                    print(f"Error :{Fore.RED} {response.status}")

        except Exception as e:
            pass

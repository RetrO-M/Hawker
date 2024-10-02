import aiohttp
from colorama import Fore, init

init()

async def deezer(email: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://www.deezer.com/ajax/gw-light.php?method=deezer.getUserData&input=3&api_version=1.0&api_token=&cid=") as response:
                if response.status != 200:
                    print(f"{Fore.RED}No Pornhub account associated with this email")
                    return
                data = await response.json()
                token = data['results']['checkForm']

            params = {
                'method': 'deezer.emailCheck',
                'input': 3,
                'api_version': 1.0,
                'api_token': token,
            }
            json_data = {
                'EMAIL': email
            }

            async with session.post("https://www.deezer.com/ajax/gw-light.php", params=params, json=json_data) as response:
                if response.status != 200:
                    print(f"{Fore.RED}No Pornhub account associated with this email")
                    return
                data = await response.json()
                availability = data.get('results', {}).get('availability', False)
                
                if availability:
                    print(f"{Fore.RED}No Pornhub account associated with this email")
                else:
                    print(f"{Fore.YELLOW}Deezer Account Found")

    except Exception as e:
        pass

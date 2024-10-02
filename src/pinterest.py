import aiohttp
from colorama import Fore, init

init()

async def check_pinterest_email(email):
    params = {
        "source_url": "/",
        "data": '{"options": {"email": "'+ email +'"}, "context": {}}'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://www.pinterest.fr/resource/EmailExistsResource/get/", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data["resource_response"]["data"]:
                        print(f"{Fore.YELLOW}Pinterest Account Found")
                    else:
                        print(f"{Fore.RED}No Pinterest account associated with this email -> EMAIL : {email}")
                else:
                    print(f"{Fore.RED}No Pinterest account associated with this email -> EMAIL : {email}")
        except Exception as e:
            pass
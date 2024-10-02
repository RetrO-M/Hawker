import aiohttp
from colorama import Fore, init

init()

async def check_adobe_email(email: str):
    data = {
        "username": email,
        "usernameType": "EMAIL"
    }

    headers = {
        'x-ims-clientid': 'homepage_milo',
        'content-type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://auth.services.adobe.com/signin/v2/users/accounts", headers=headers, json=data) as r:
            try:
                response = await r.json()
                if response and 'authenticationMethods' in response[0]:
                    print(f"{Fore.YELLOW}Adobe Account Found")
                else:
                    print(f"{Fore.RED}No Adobe account associated with this email -> EMAIL : {email}")
            except Exception as e:
                pass

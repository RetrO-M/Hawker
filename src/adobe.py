import requests
from colorama import Fore, init

init()

def check_adobe_email(email: str):
    data = {
        "username": email,
        "usernameType": "EMAIL"
    }

    headers = {
        'x-ims-clientid': 'homepage_milo',
        'content-type': 'application/json'
    }

    try:
        r = requests.post("https://auth.services.adobe.com/signin/v2/users/accounts", headers=headers, json=data)
        response = r.json()

        if response and 'authenticationMethods' in response[0]:
            print(f"  {Fore.LIGHTWHITE_EX}Adobe Account Found")
        else:
            print(f"  {Fore.RED}No Adobe account")
    except Exception as e:
        pass

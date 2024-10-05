import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init()

def pornhub(target: str):
    try:
        with requests.Session() as session:
            response = session.get("https://fr.pornhub.com/signup")
            text = response.text
            soup = BeautifulSoup(text, 'html.parser')
            token = soup.find(attrs={'name': 'token'}).get('value')

            params = {'token': token}
            data = {
                'check_what': 'email',
                'email': target
            }

            response_api = session.post("https://fr.pornhub.com/user/create_account_check", params=params, data=data)
            response_json = response_api.json()

            if response_json.get('email') == "create_account_passed":
                print(f"  {Fore.RED}No Pornhub account")
            elif response_json.get('email') == "create_account_failed":
                print(f"  {Fore.LIGHTWHITE_EX}Pornhub Account Found")
            else:
                print(f"  {Fore.RED}No Pornhub account")

    except Exception as e:
        pass

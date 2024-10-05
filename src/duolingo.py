import requests
from colorama import Fore, init
from fake_useragent import UserAgent

ua = UserAgent()
useragent = ua.random

init()

def check_duolingo_email(target: str):
    url = "https://www.duolingo.com/2017-06-30/users"
    params = {'email': target}

    headers = {
        "User-Agent": useragent,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            text_response = response.text

            if '{"users":[]}' in text_response:
                print(f"  {Fore.RED}No Duolingo account")
            else:
                valid = response.json()['users'][0]['username']
                print(f"  {Fore.LIGHTWHITE_EX}Duolingo Account Found")

        else:
            print(f"  {Fore.RED}STATUS : {response.status_code}")

    except Exception as e:
        pass


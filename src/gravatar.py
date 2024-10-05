import hashlib
import requests
from colorama import Fore, init

init()

def check_gravatar_email(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://en.gravatar.com/{email_hash}.json"
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            display_name = data['entry'][0].get('displayName', 'Unknown')
            print(f"  {Fore.LIGHTWHITE_EX}https://gravatar.com/{display_name}")
        elif response.status_code == 404:
            print(f"  {Fore.RED}No Gravatar account")
        else:
            print(f"  {Fore.RED}STATUS : {response.status_code}")
    
    except Exception as e:
        pass


import requests
from colorama import Fore, init

init()

async def check_twitter_email(email):
    url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data["valid"]:
                print(f"{Fore.YELLOW}Twitter Account Found")
            else:
                print(f"{Fore.RED}No Twitter account associated with this email -> EMAIL : {email}")
        else:
            print(f"Error : {Fore.RED}{response.status_code}")
    except requests.exceptions.JSONDecodeError:
        pass

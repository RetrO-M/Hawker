import requests
from colorama import Fore, init

init()

def check_github_email(email):
    url = f"https://api.github.com/search/users?q={email}+in:email"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            if result["total_count"] > 0:
                print(f"  {Fore.LIGHTWHITE_EX}https://github.com/{result['items'][0]['login']}")
            else:
                print(f"  {Fore.RED}No GitHub account")
        else:
            print(f"  {Fore.RED}STATUS : {response.status_code}")
    
    except Exception as e:
        pass


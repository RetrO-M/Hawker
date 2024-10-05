import requests
from colorama import Fore, init

init()

def check_pinterest_email(email):
    params = {
        "source_url": "/",
        "data": '{"options": {"email": "' + email + '"}, "context": {}}'
    }
    
    try:
        response = requests.get("https://www.pinterest.fr/resource/EmailExistsResource/get/", params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["resource_response"]["data"]:
                print(f"  {Fore.LIGHTWHITE_EX}Pinterest Account Found")
            else:
                print(f"  {Fore.RED}No Pinterest account")
        else:
            print(f"  {Fore.RED}No Pinterest account")

    except Exception as e:
        pass


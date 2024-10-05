import requests
from colorama import Fore, init

init()

def check_spotify_email(target: str):
    url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            responseData = response.json()
            
            if responseData.get('status') == 20:
                print(f"  {Fore.LIGHTWHITE_EX}Spotify Account Found")
            else:
                print(f"  {Fore.RED}No Spotify account")
        else:
            print(f"  {Fore.RED}No Spotify accountl")

    except Exception as e:
        pass


import requests
from colorama import Fore, init

init()

def check_chess_email(email):
    url = f"https://www.chess.com/callback/email/available?email={email}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('isEmailAvailable') == True:
            print(f"  {Fore.RED}No Chess.com account") 
        elif data.get('isEmailAvailable') == False:
            print(f"  {Fore.LIGHTWHITE_EX}Chess.com Account Found") 
        else:
            print(f"  {Fore.RED}No Chess.com account") 
    except:
        print(f"  {Fore.RED}No Chess.com account")

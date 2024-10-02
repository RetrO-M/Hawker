import aiohttp
from colorama import Fore, init

init()

async def check_chess_email(email):
    url = f"https://www.chess.com/callback/email/available?email={email}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                data = await response.json()
                if data.get('isEmailAvailable') == True:
                    print(f"{Fore.RED}No Chess.com account associated with this email -> EMAIL : {email}") 
                elif data.get('isEmailAvailable') == False:
                    print(f"{Fore.YELLOW}Chess.com Account Found") 
                else:
                    print(f"{Fore.RED}No Chess.com account associated with this email -> EMAIL : {email}") 
            except:
                print(f"{Fore.RED}No Chess.com account associated with this email -> EMAIL : {email}") 

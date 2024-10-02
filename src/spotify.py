import aiohttp
from colorama import Fore, init

init()

async def check_spotify_email(target: str):
    url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
    
    async with aiohttp.ClientSession() as client:
        try:
            response = await client.get(url)

            try:
                responseData = await response.json()
                
                if responseData.get('status') == 20:
                    print(f"{Fore.YELLOW}Spotify Account Found")
                else:
                    print(f"{Fore.RED}No Spotify account associated with this email")
            except aiohttp.ContentTypeError:
                print(f"{Fore.RED}No Spotify account associated with this email")

        except Exception as e:
            pass

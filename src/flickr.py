import aiohttp
import re
from colorama import Fore, init

init()


async def check_flickr_email(email):
    url = "https://www.flickr.com/"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            html = await r.text()

    key_pattern = r'[a-f0-9]{32}'
    keys = re.findall(key_pattern, html)

    api_keys = set(keys)
    flickr_found = False

    if api_keys:
        for key in api_keys:
            api_url = "https://api.flickr.com/services/rest"

            params = {
                'method': 'flickr.people.findByEmail',
                'find_email': email,
                'api_key': key,
                'format': 'json',
                'nojsoncallback': 1
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params) as r:
                    try:
                        data = await r.json()
                        if 'user' in data:
                            print(f"{Fore.YELLOW}Flickr Account Found: https://www.flickr.com/people/{data['user']['nsid']}/")
                            flickr_found = True
                            break
                    except:
                        continue

    if not flickr_found:
        print(f"{Fore.RED}No Flickr account associated with this email -> EMAIL : {email}")

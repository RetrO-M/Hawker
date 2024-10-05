import requests
import re
from colorama import Fore, init

init()

def check_flickr_email(email):
    url = "https://www.flickr.com/"
    
    response = requests.get(url)
    html = response.text

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

            response = requests.get(api_url, params=params)
            try:
                data = response.json()
                if 'user' in data:
                    print(f"  {Fore.LIGHTWHITE_EX}https://www.flickr.com/people/{data['user']['nsid']}/")
                    flickr_found = True
                    break
            except:
                continue

    if not flickr_found:
        print(f"  {Fore.RED}No Flickr account")


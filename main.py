'''

                   .--~~,__      
      :-....,-------`~~'._.'     Twitter → @DeAn0nim0us
       `-,,,  ,_      ;'~U'      Github → RetrO-M
        _,-' ,'`-__; '--.        https://discord.gg/KRjzDPzDbx
       (_/'~~      """"(;
       Hawker OSINT Tool
    Hawker+ is a more advanced version of the OSINT tool that provides access to large databases for investigative purposes. This tool is intended for law enforcement 
    and cybersecurity professionals.

        → How to get Hawker+
            → 1. Reach out to me via Discord for further information and access to the tool. My Discord username is: "0.d4y".
            → To support the development of this tool, a donation of 1 XMR (Monero) is required. Please send the donation to the following Monero address:
            → Monero Address : 455RrwkuryVRioADddHWfGXrWHSLk4n1DHX36E4tKkBHScps4CeFwMWVemyqgWkL5eYf5L2zRVkgQB4Y9dwaechDKqQzC7p
            → After completing the donation, send me the following:
            → The transaction ID (txid) of your Monero transaction.
            → A screenshot of your donation confirmation.
            → Once I confirm your donation, I will provide you with the link to download the Hawker+ tool in a .7z archive format.

I am extremely sorry... for disappointing you if you really want me to add more files please tell me or you pay the Hawker +
If you want more files for the data breach, create an "Issue" on github and I'll add it, I promise.
'''

from colorama                                                 import Fore, init
from os                                                       import system, path, listdir
from requests                                                 import get, post, Session, RequestException, exceptions
from re                                                       import compile, search, IGNORECASE
from hashlib                                                  import sha1, sha256, md5
from bs4                                                      import BeautifulSoup
from random                                                   import choice
from time                                                     import sleep
from pefile                                                   import PE   
from datetime                                                 import datetime, UTC
from requests.exceptions                                      import HTTPError
from urllib.parse                                             import urlencode, urljoin
from warnings                                                 import filterwarnings
from cryptography.hazmat.primitives.ciphers                   import Cipher, algorithms, modes
from rich.progress                                            import Progress
from pprint                                                   import pprint

import os
import urllib.parse
import docx

init()
filterwarnings("ignore", category=UserWarning, module="cryptography")

def banner(title):
    width = 58
    title_len = len(title)

    left_padding = (width - 2 - title_len) // 2
    right_padding = width - 2 - title_len - left_padding

    print(f'\n{Fore.LIGHTWHITE_EX}╔' + '─' * (width - 2) + '╗')
    print(f'{Fore.LIGHTWHITE_EX}║' + ' ' * left_padding + Fore.LIGHTBLUE_EX + title + Fore.LIGHTWHITE_EX + ' ' * right_padding + '║')
    print(f'{Fore.LIGHTWHITE_EX}╚' + '─' * (width - 2) + '╝\n')

class Hawker:
    def __init__(self):
        self.folders = {
            'Collection #1':    'database/Collection_#1',
            'Pornhub':          'database/Pornhub',
            'Mega.nz':          'database/Mega.nz',
            'Comcast':          'database/Comcast',
            'Gmail':            'database/Gmail',
            'Ogusers':          'database/ogusers.com',
            'Exploit.in':       'database/Exploit.in',
            'Instagram':        'database/Instagram'
        }
        self.countries = {
            "FR": "camera/FR/camera.txt",
            "US": "camera/US/camera.txt",
            "RU": "camera/RU/camera.txt",
            "NL": "camera/NL/camera.txt",
            "CA": "camera/CA/camera.txt",
            "IT": "camera/IT/camera.txt",
            "DE": "camera/DE/camera.txt",
            "PL": "camera/PL/camera.txt",
            "SE": "camera/SE/camera.txt"
        }
        self.headers = {
            "User-Agent": choice([
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            ]),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com",
            "Origin": "https://www.google.com"
        }
        self.KEY = b"0123456789abcdef"

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def center_text(self, text, width):
        return text.center(width)

    def display_message(self, title, subtitle, duration=5):
        self.clear_terminal()
        terminal_width = os.get_terminal_size().columns

        title = self.center_text(title, terminal_width)
        subtitle = self.center_text(subtitle, terminal_width)

        print("\n" * 10)
        print(title)
        print(subtitle)
        print("\n" * 10)

        sleep(duration)
        self.clear_terminal()


#region Google Dorking

    def doxbin_search(self, text):
        query = f'"{text}" site:doxbin.com'
        url = "https://www.startpage.com/sp/search?"
        params = {
            'query': query,
            'cat': 'web',
            'pl': 'en',
            'num': 10
        }
        url_with_params = url + urlencode(params)
        try:
            response = get(url_with_params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'doxbin.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def pastebin_search(self, text):
        query = f"{text} site:pastebin.com"
        url = "https://www.startpage.com/sp/search?"
        params = {
            'query': query,
            'cat': 'web',
            'pl': 'en',
            'num': 10
        }
        url_with_params = url + urlencode(params)
        try:
            response = get(url_with_params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'pastebin.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None
    
    def pagesjaunes_search(self, text):
        query = f"{text} site:pagesjaunes.fr"
        url = "https://www.startpage.com/sp/search?"
        params = {
            'query': query,
            'cat': 'web',
            'pl': 'en',
            'num': 10
        }
        url_with_params = url + urlencode(params)
        try:
            response = get(url_with_params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'pagesjaunes.fr' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def whitepages_search(self, text):
        query = f"{text} site:whitepages.com"
        url = "https://www.startpage.com/sp/search?"
        params = {
            'query': query,
            'cat': 'web',
            'pl': 'en',
            'num': 10
        }
        url_with_params = url + urlencode(params)
        try:
            response = get(url_with_params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'whitepages.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

#endregion



#region Email Information


    def decrypt_file(self, file_path):
        with open(file_path, "rb") as file:
            iv = file.read(16)
            encrypted_data = file.read()

        decryptor = Cipher(algorithms.AES(self.KEY), modes.CBC(iv)).decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        return decrypted_data.rstrip(decrypted_data[-1:]).decode("utf-8", errors="ignore")

    def hash_password(self, password):
        sha256_hash = sha256(password.encode('utf-8')).hexdigest()
        return sha256_hash

    def search_database(self, email):
        found = False

        for folder_name, folder_path in self.folders.items():
            if not path.exists(folder_path):
                continue  

            for filename in listdir(folder_path):
                file_path = path.join(folder_path, filename)

                if path.isfile(file_path):
                    try:
                        decrypted_content = self.decrypt_file(file_path)

                        for line in decrypted_content.split("\n"):
                            if line.startswith(email + ":"):
                                password = line.split(":", 1)[1].strip()
                                hashed_password = self.hash_password(password)
                                print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTWHITE_EX}] {folder_name}: {Fore.LIGHTCYAN_EX}{hashed_password}")
                    except Exception:
                        continue

    def check_chess_email(self, email):
        url = f"https://www.chess.com/callback/email/available?email={email}"
        
        try:
            response = get(url, headers=self.headers)
            data = response.json()
        
            if data.get('isEmailAvailable') == True:
                pass
            elif data.get('isEmailAvailable') == False:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com Account Found") 
        except:
            pass

    def check_duolingo_email(self, target: str):
        url = "https://www.duolingo.com/2017-06-30/users"

        params = {
            'email': target
        }

        try:
            response = get(url, params=params, headers=self.headers)

            if response.status_code == 200:
                text_response = response.text

                if '{"users":[]}' in text_response:
                    pass
                else:
                    valid = response.json()['users'][0]['username']
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Duolingo Account Found")

        except Exception as e:
            pass

    def check_github_email(self, email):
        url = f"https://api.github.com/search/users?q={email}+in:email"
        
        try:
            response = get(url, headers=self.headers)
        
            if response.status_code == 200:
                result = response.json()
                if result["total_count"] > 0:
                    for user in result['items']:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} GitHub Profile: https://github.com/{user['login']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──ID:{Fore.LIGHTBLUE_EX} {user['id']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Login:{Fore.LIGHTBLUE_EX} {user['login']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Avatar URL:{Fore.LIGHTBLUE_EX} {user['avatar_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Type:{Fore.LIGHTBLUE_EX} {user['type']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──URL:{Fore.LIGHTBLUE_EX} {user['url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Repos URL:{Fore.LIGHTBLUE_EX} {user['repos_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Gists URL:{Fore.LIGHTBLUE_EX} {user['gists_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Following URL:{Fore.LIGHTBLUE_EX} {user['following_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Followers URL:{Fore.LIGHTBLUE_EX} {user['followers_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Events URL:{Fore.LIGHTBLUE_EX} {user['events_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}└──Received Events URL:{Fore.LIGHTBLUE_EX} {user['received_events_url']}")
        except Exception as e:
            pass

    def check_gravatar_email(self, email):
        email_hash = md5(email.strip().lower().encode()).hexdigest()
        url = f"https://en.gravatar.com/{email_hash}.json"
        
        try:
            response = get(url, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                if 'entry' in data:
                    entry = data['entry'][0]
                    display_name = entry.get('displayName', 'Unknown')
                    preferred_username = entry.get('preferredUsername', 'Unknown')
                    email_hash = entry.get('hash', 'Unknown')

                    photos = entry.get('photos', [])
                    photo_url = photos[0]['value'] if photos else 'No photo available'
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Gravatar Account Found")
                    print(f" {Fore.LIGHTWHITE_EX}├──Gravatar Profile:{Fore.LIGHTBLUE_EX} https://gravatar.com/{email_hash}")
                    print(f" {Fore.LIGHTWHITE_EX}├──Display Name:{Fore.LIGHTBLUE_EX} {display_name}")
                    print(f" {Fore.LIGHTWHITE_EX}├──Preferred Username:{Fore.LIGHTBLUE_EX} {preferred_username}")
                    print(f" {Fore.LIGHTWHITE_EX}├──Hash:{Fore.LIGHTBLUE_EX} {email_hash}")
                    print(f" {Fore.LIGHTWHITE_EX}└──Profile Photo:{Fore.LIGHTBLUE_EX} {photo_url}")
        except Exception as e:
            pass

    def check_pinterest_email(self, email):
        params = {
            "source_url": "/",
            "data": '{"options": {"email": "' + email + '"}, "context": {}}'
        }
        
        try:
            response = get("https://www.pinterest.fr/resource/EmailExistsResource/get/", params=params, headers=self.headers)
        
            if response.status_code == 200:
                data = response.json()
                if data["resource_response"]["data"]:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pinterest Account Found")

        except Exception as e:
            pass

    def pornhub(self, target: str):
        try:
            with Session() as session:
                response = session.get("https://fr.pornhub.com/signup")
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                token = soup.find(attrs={'name': 'token'}).get('value')

                params = {
                    'token': token
                }
                data = {
                    'check_what': 'email',
                    'email': target
                }

                response_api = session.post("https://fr.pornhub.com/user/create_account_check", params=params, data=data)
                response_json = response_api.json()

                if response_json.get('email') == "create_account_passed":
                    pass
                elif response_json.get('email') == "create_account_failed":
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pornhub Account Found")

        except Exception as e:
            pass

    def check_spotify_email(self, target: str):
        url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
        
        try:
            response = get(url, headers=self.headers)

            if response.status_code == 200:
                responseData = response.json()
            
                if responseData.get('status') == 20:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Spotify Account Found")

        except Exception as e:
            pass

    def check_twitter_email(self, email):
        url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
        
        try:
            response = get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if not data["valid"]:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Twitter Account Found")
        except Exception as e:
            pass

    def wordpress_email(self, email):
        response = get(f'https://public-api.wordpress.com/rest/v1.1/users/{email}/auth-options', headers=self.headers)

        if '"email_verified":true' in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Wordpress Account Found')

    def picsart(self, target: str):
        params = {
            'email_encoded': 1,
            'emails': target
        }
        try:
            response = get("https://api.picsart.com/users/email/existence", params=params, headers=self.headers)
            response.raise_for_status() 
            if response.json().get('status') == 'success':
                if response.json().get('response'):
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Picsart Account Found")

        except exceptions.RequestException as e:
            pass

    def bitmoji(self, email):
        URL = "https://bitmoji.api.snapchat.com/api/user/find"
        data = {
            'email': email
        }
        try:
            r = post(URL, headers=self.headers, data=data)

            if '"account_type":"bitmoji"' in r.text:
                print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitmoji Account Found')

        except Exception as e:
            pass

    def mewe(self, email):
        url = f'https://mewe.com/api/v2/auth/checkEmail?email={email}'
        response = get(url, headers=self.headers)
        if "Email already taken" in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Mewe Account Found')      

    def firefox(self, email):
        data = {
            'email': email
        }
        response = post('https://api.accounts.firefox.com/v1/account/status', data=data)
        if "true" in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Firefox Account Found') 

    def xnxx(self, email):
        response = get(f'https://www.xnxx.com/account/checkemail?email={email}')
        if "This email is already in use or its owner has excluded it from our website." in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} XnXX Account Found')

    def xvideos(self, email):
        params = {
            'email': email
        }
        response = get(f'https://www.xvideos.com/account/checkemail', params=params)
        if "This email is already in use or its owner has excluded it from our website." in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Xvideos Account Found')
 
    def Patreon(self, email):
        data = {
            'email': email
        }
        response = post('https://www.plurk.com/Users/isEmailFound', data=data)

        if "True" in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Patreon Account Found')      

    def Instagram(self, email):
        from fake_useragent import UserAgent
        ua = UserAgent()
        try:
            session = Session()
            headers = {
                'User-Agent': ua.random,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/accounts/emailsignup/',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Instagram-AJAX': '1',
            }

            response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
            if response.status_code != 200:
                return f"Error: {response.status_code}"

            cookies = session.cookies.get_dict()
            token = cookies.get('csrftoken')
            if not token:
                return "Error: Token Not Found."

            headers["x-csrftoken"] = token
            session.cookies.set('csrftoken', token)

            sleep(3)

            data = {"email": email}
            response = session.post(
                url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
                headers=headers,
                data=data,
                cookies=session.cookies
            )

            if response.status_code == 200:
                response_json = response.json()

                if "errors" in response_json and "email" in response_json["errors"]:
                    email_errors = response_json["errors"]["email"]
                    for error in email_errors:
                        if error.get("code") in ["email_sharing_limit", "email_is_taken"]:
                            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Instagram Account Found')
                            return True
                return False

            return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error: {e}"


    def wikileaks_search(self, text):
        URL = f'https://search.wikileaks.org/?query={text}&exact_phrase=&include_external_sources=True&order_by=newest_document_date&page=1'
        response = get(URL, headers=self.headers)
        
        if response.status_code != 200:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error retrieving the page.")
            return
        
        sleep(1)

        soup = BeautifulSoup(response.content, "lxml")
        divtag_var = soup.find_all('div', {'class': 'result'})
        if not divtag_var:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No results found for the search.")
            return
        
        URL_REGEX = compile(r'<h4><a href="(https://wikileaks.org\S+)">')
        SUBJ_REGEX = compile(r'<h4><a href="https://wikileaks.org\S+">\s?([^<]+)</a>')
        SENDR1_REGEX = compile(r'email:\s([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA0-9]{2,})')
        LEAK_REGEX = compile(r'leak-label">.*?<div><b>([^<]+)</b>')
        DATE_REGEX = compile(r'Created<br/>\n<span>(\d{4}-\d{2}-\d{2})</span>')

        for a in divtag_var:
            url_var = URL_REGEX.findall(str(a))
            date_var = DATE_REGEX.findall(str(a))
            subj_var = SUBJ_REGEX.findall(str(a))
            sendr1_var = SENDR1_REGEX.findall(str(a))
            leak_var = LEAK_REGEX.findall(str(a))
            sendr_var = sendr1_var[0] if sendr1_var else None
            date_var = date_var[0] if date_var else None
            subj_var = subj_var[0] if subj_var else None
            leak_var = leak_var[0] if leak_var else None
            
            if url_var or date_var or sendr_var or subj_var or leak_var:
                if date_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date:{Fore.LIGHTBLUE_EX} {date_var}')
                if sendr_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Sender:{Fore.LIGHTBLUE_EX} {sendr_var}')
                if subj_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Subject:{Fore.LIGHTBLUE_EX} {subj_var}')
                if url_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} URL:{Fore.LIGHTBLUE_EX} {url_var}')
                if leak_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Leak:{Fore.LIGHTBLUE_EX} {leak_var}')
                print('\n')

    def extract_links_ahmia(self, email):
        encoded_email = urllib.parse.quote(email)
        url = f"https://ahmia.fi/search/?q={encoded_email}"
        
        response = get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']

                if '/search/redirect?' in href:
                    redirect_url = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('redirect_url', [None])[0]
                    
                    if redirect_url:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} .onion link found:{Fore.LIGHTBLUE_EX} {redirect_url}")

    def hudsonrock_api_email(self, text):
        try:
            url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={text}"
            response = get(url)
            response.raise_for_status()
            stealers_data = response.json().get('stealers', [])

            if stealers_data:
                for data in stealers_data:
                    computer_name = data.get('computer_name', '/')
                    operating_system = data.get('operating_system', '/')
                    ip = data.get('ip', '/')
                    malware_path = data.get('malware_path', '/')
                    date_compromised = data.get('date_compromised', '/')
                    antiviruses = data.get('antiviruses', '/')
                    top_logins = data.get('top_logins', [])
                    top_passwords = data.get('top_passwords', [])
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} STEALERS: ")
                    print(f" {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTBLUE_EX} ", computer_name)
                    print(f" {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTBLUE_EX} ", operating_system)
                    print(f" {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTBLUE_EX} ", ip)
                    print(f" {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTBLUE_EX} ", malware_path)
                    print(f" {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTBLUE_EX} ", date_compromised)
                    print(f" {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTBLUE_EX} ", antiviruses)
                    print(f" {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTBLUE_EX} ", ', '.join(top_logins))
                    print(f" {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTBLUE_EX} ", ', '.join(top_passwords), "\n")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")
        except HTTPError as http_err:
            print(f"{Fore.LIGHTRED_EX}[ERROR] HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Other error occurred: {err}")
#endregion


#region Phone information


    def get_phone_info(self, phone_number):
        url = f"http://phone-number-api.com/json/?number={phone_number}"
        response = get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
#endregion


#region IP information

    def hudsonrock_api_ip(self, text):
        try:
            url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-ip?ip={text}"
            response = get(url)
            response.raise_for_status()
            stealers_data = response.json().get('stealers', [])

            if stealers_data:
                for data in stealers_data:
                    computer_name = data.get('computer_name', '/')
                    operating_system = data.get('operating_system', '/')
                    ip = data.get('ip', '/')
                    malware_path = data.get('malware_path', '/')
                    date_compromised = data.get('date_compromised', '/')
                    antiviruses = data.get('antiviruses', '/')
                    top_logins = data.get('top_logins', [])
                    top_passwords = data.get('top_passwords', [])
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} STEALERS: ")
                    print(f" {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTBLUE_EX} ", computer_name)
                    print(f" {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTBLUE_EX} ", operating_system)
                    print(f" {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTBLUE_EX} ", ip)
                    print(f" {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTBLUE_EX} ", malware_path)
                    print(f" {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTBLUE_EX} ", date_compromised)
                    print(f" {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTBLUE_EX} ", antiviruses)
                    print(f" {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTBLUE_EX} ", ', '.join(top_logins))
                    print(f" {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTBLUE_EX} ", ', '.join(top_passwords), "\n")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")
        except HTTPError as http_err:
            print(f"{Fore.LIGHTRED_EX}[ERROR] HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Other error occurred: {err}")

    def geolocation_ip(self, ip):
        url = f"https://ipwhois.app/json/{ip}"
        respon = get(url, headers=self.headers)
        if respon.status_code == 200:
            result = respon.json() 
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP : ", result.get("ip"))
            print(f" {Fore.LIGHTWHITE_EX}├──Country :{Fore.LIGHTBLUE_EX} ", result.get("country"))
            print(f" {Fore.LIGHTWHITE_EX}├──Region :{Fore.LIGHTBLUE_EX} ", result.get("region"))
            print(f" {Fore.LIGHTWHITE_EX}├──City :{Fore.LIGHTBLUE_EX} ", result.get("city"))
            print(f" {Fore.LIGHTWHITE_EX}├──Location : {Fore.LIGHTBLUE_EX}", f"{result.get('latitude')}, {result.get('longitude')}")
            print(f" {Fore.LIGHTWHITE_EX}├──ISP : {Fore.LIGHTBLUE_EX}", result.get("isp"))
            print(f" {Fore.LIGHTWHITE_EX}└──ASN : {Fore.LIGHTBLUE_EX}", result.get("asn"))
        else:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Unable to fetch data for IP: {ip}")
#endregion

#region Cameras

    def check_cameras(self):
        for country_code, path in self.countries.items():
            if os.path.exists(path):
                print()
                decrypted_content = self.decrypt_file(path)
                for line in decrypted_content.split("\n"):
                    url = line.strip()
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} (Camera {country_code}) :{Fore.LIGHTBLUE_EX} {url}")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} The file for {country_code} does not exist.")

#endregion


#region Personal information

    def algolia(self, fullname):
        encoded_username = urllib.parse.quote(fullname)
        url = f"https://hn.algolia.com/api/v1/search?query={encoded_username}"
        response = get(url)
        if response.status_code == 200:
            data = response.json()
            for hit in data['hits']:
                if 'title' in hit:
                    title = hit['title']
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Title:{Fore.LIGHTBLUE_EX} {title}")
                if 'url' in hit:
                    url = hit['url']
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} URL:{Fore.LIGHTBLUE_EX} {url}")
                print()
#endregion


#region Bitcoin Information

    def get_bitcoin_info(self, bitcoin):
        url = f"https://blockchain.info/rawaddr/{bitcoin}"
        
        try:
            response = get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} ERROR : {response.status_code}")
                return
            
            data = response.json()

            total_balance = data.get('final_balance', 0) / 1e8
            total_transactions = data.get('n_tx', 0)
            total_received = data.get('total_received', 0) / 1e8 
            total_sent = data.get('total_sent', 0) / 1e8 

            first_tx_time = 'None'
            if data.get('txs', []):
                first_tx_time = data['txs'][0].get('time', 'None')

            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitcoin :{Fore.LIGHTBLUE_EX} {bitcoin}")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Balance :{Fore.LIGHTBLUE_EX} {total_balance} BTC")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Transactions : {Fore.LIGHTBLUE_EX}{total_transactions}")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Received : {Fore.LIGHTBLUE_EX}{total_received} BTC")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Sent :{Fore.LIGHTBLUE_EX} {total_sent} BTC")
            print(f" {Fore.LIGHTWHITE_EX}└──First Transaction (timestamp) :{Fore.LIGHTBLUE_EX} {first_tx_time}")
            
        except Exception as e:
            pass

#endregion



#region PyInstaller

    def get_pe_info(self, file):
        file_path = file
        try:
            pe = PE(file_path)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} File Name : {path.basename(file_path)}")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} File size : {path.getsize(file_path)} octets")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Entrypoint : 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:X}")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ImageBase : 0x{pe.OPTIONAL_HEADER.ImageBase:X}")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Machine : {hex(pe.FILE_HEADER.Machine)}")
            timestamp = pe.FILE_HEADER.TimeDateStamp
            if timestamp > 0:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} TimeDateStamp : {datetime.fromtimestamp(timestamp, UTC)}")
            for section in pe.sections:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {section.Name.decode().strip()} - VA: {hex(section.VirtualAddress)}, Size: {section.Misc_VirtualSize}, Entropie: {section.get_entropy()}")
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {entry.dll.decode()} : {[imp.name.decode() if imp.name else 'Ordinal' for imp in entry.imports]}")
            with open(file_path, "rb") as f:
                content = f.read()
                match = search(rb'python(\d{2,3})', content, IGNORECASE)
                if match:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Version Python : Python{match.group(1).decode()}")
            with open(file_path, "rb") as f:
                file_data = f.read()
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} MD5 : {md5(file_data).hexdigest()}")
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SHA-1 : {sha1(file_data).hexdigest()}")
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SHA-256 : {sha256(file_data).hexdigest()}")
            pe.close()
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {e}")

#endregion

#region MAC Information

    def mac_address_lookup(self, mac):
        url = f"https://api.maclookup.app/v2/macs/{mac}"
        
        try:
            response = get(url, headers=self.headers)
            response.raise_for_status() 
            data = response.json()
            
            if data.get("success") and data.get("found"):
                return data
            else:
                return {"error": "Information not found for this MAC address."}
        except exceptions.RequestException as e:
            return {"error": str(e)}
        
#endregion

#region VIN Information

    def get_vehicle_info(self, vin):
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
        response = get(url)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("Results", [])

            make = next((entry["Value"] for entry in results if entry["Variable"] == "Make"), "N/A")
            model = next((entry["Value"] for entry in results if entry["Variable"] == "Model"), "N/A")
            year = next((entry["Value"] for entry in results if entry["Variable"] == "Model Year"), "N/A")
            vehicle_type = next((entry["Value"] for entry in results if entry["Variable"] == "Vehicle Type"), "N/A")

            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Make :", make)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Model :", model)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Year :", year)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Type :", vehicle_type)

#endregion

#region MetaData docx
    def extract_metadata(self, docx_file):
        doc = docx.Document(docx_file)
        core_properties = doc.core_properties

        metadata = {}

        for prop in dir(core_properties):
            if prop.startswith('__'):
                continue
            value = getattr(core_properties, prop)
            if callable(value):
                continue
            if prop == 'created' or prop == 'modified' or prop == 'last_printed':
                if value:
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    value = None
            metadata[prop] = value  

        try:
            custom_properties = core_properties.custom_properties
            if custom_properties:
                metadata['custom_properties'] = {}
                for prop in custom_properties:
                    metadata['custom_properties'][prop.name] = prop.value
        except AttributeError:
            pass
        return metadata
#endregion

#region PDF information
    def extract_pdf_metadata(self, pdf_path):
        with open(pdf_path, "rb") as file:
            content = file.read().decode(errors='ignore')
            
            patterns = {
                "Creator": r"/Creator \((.*?)\)",
                "Producer": r"/Producer \((.*?)\)",
                "CreationDate": r"/CreationDate \((.*?)\)",
                "ModDate": r"/ModDate \((.*?)\)",
                "Keywords": r"/Keywords \((.*?)\)",
                "Author": r"/Author \((.*?)\)",
                "Marked": r"/Marked (true|false)",
                "Suspects": r"/Suspects (true|false)",
                "DisplayDocTitle": r"/DisplayDocTitle (true|false)",
                "Count": r"/Count (\d+)",
                "PDF Version": r"%PDF-(\d+\.\d+)",
                "Lang": r"/Lang \((.*?)\)",
                "Width": r"/Width (\d+)",
                "Height": r"/Height (\d+)",
                "Title": r"/Title <([0-9A-Fa-f]+)>"
            }
            
            results = {}
            for key, pattern in patterns.items():
                match = search(pattern, content)
                if match:
                    results[key] = match.group(1)
            
            if results:
                for key, value in results.items():
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {key}: {value}")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No MetaData")
#endregion


def title():
    system('clear || cls')
    banner = rf'''{Fore.LIGHTBLUE_EX}
  _    _                _                ____   _____ _____ _   _ _______ 
 | |  | |              | |              / __ \ / ____|_   _| \ | |__   __|
 | |__| | __ ___      _| | _____ _ __  | |  | | (___   | | |  \| |  | |   
 |  __  |/ _` \ \ /\ / / |/ / _ \ '__| | |  | |\___ \  | | | . ` |  | |   
 | |  | | (_| |\ V  V /|   <  __/ |    | |__| |____) |_| |_| |\  |  | |
 |_|  |_|\__,_| \_/\_/ |_|\_\___|_|     \____/|_____/|_____|_| \_|  |_|   

                   .--~~,__      Good luck with your investigations.
      :-....,-------`~~'._.'     Twitter → @DeAn0nim0us
       `-,,,  ,_      ;'~U'      Github → RetrO-M
        _,-' ,'`-__; '--.        Discord Hawker → https://discord.gg/KRjzDPzDbx (NEW SERVER)
       (_/'~~      """"(;
   Do you want this version to improve, make an issue on github.
  {Fore.LIGHTWHITE_EX}01 {Fore.LIGHTCYAN_EX}→ Email Information
  {Fore.LIGHTWHITE_EX}02 {Fore.LIGHTCYAN_EX}→ Phone Information
  {Fore.LIGHTWHITE_EX}03 {Fore.LIGHTCYAN_EX}→ IP Information
  {Fore.LIGHTWHITE_EX}04 {Fore.LIGHTCYAN_EX}→ Camera Information
  {Fore.LIGHTWHITE_EX}05 {Fore.LIGHTCYAN_EX}→ Personal Information
  {Fore.LIGHTWHITE_EX}06 {Fore.LIGHTCYAN_EX}→ Bitcoin Information
  {Fore.LIGHTWHITE_EX}07 {Fore.LIGHTCYAN_EX}→ PyInstaller Information
  {Fore.LIGHTWHITE_EX}08 {Fore.LIGHTCYAN_EX}→ MAC Information
  {Fore.LIGHTWHITE_EX}09 {Fore.LIGHTCYAN_EX}→ VIN Information
  {Fore.LIGHTWHITE_EX}10 {Fore.LIGHTCYAN_EX}→ PDF Information
  {Fore.LIGHTWHITE_EX}11 {Fore.LIGHTCYAN_EX}→ Docx Information

  {Fore.LIGHTWHITE_EX}00 {Fore.LIGHTCYAN_EX}→ Hawker+
   '''
    print(banner)

def main():
    haw = Hawker()
    haw.display_message("Donate Monero to support me, Thank you <3", "455RrwkuryVRioADddHWfGXrWHSLk4n1DHX36E4tKkBHScps4CeFwMWVemyqgWkL5eYf5L2zRVkgQB4Y9dwaechDKqQzC7p", 3)
    haw.display_message("RetrO-M", "Remember to use legally, I wish you a good investigation", 2)
    while True:
        title()
        print(f'{Fore.LIGHTBLUE_EX}┌───[{Fore.LIGHTCYAN_EX}HAWKER{Fore.LIGHTBLUE_EX}@{Fore.LIGHTCYAN_EX}root{Fore.LIGHTBLUE_EX}]~[{Fore.LIGHTCYAN_EX}/{Fore.LIGHTBLUE_EX}]')
        command = input(f'{Fore.LIGHTBLUE_EX}└──{Fore.BLUE}>{Fore.LIGHTWHITE_EX} ')

        if command == "01" or command == "1":
            email = input(f"{Fore.LIGHTBLUE_EX}Email{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "Data Breach": [haw.search_database],
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "Social Networks": [haw.check_github_email, haw.picsart, haw.pornhub, haw.check_spotify_email, haw.check_twitter_email, haw.check_chess_email, haw.check_duolingo_email, haw.check_gravatar_email, haw.check_pinterest_email, haw.bitmoji, haw.mewe, haw.firefox, haw.xnxx, haw.xvideos, haw.Patreon, haw.Instagram],
                "Hudsonrock API": [haw.hudsonrock_api_email],
                "WikiLeaks": [haw.wikileaks_search]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(email)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(email)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    else:
                        func(email)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "02" or command == "2":
            phone = input(f"{Fore.LIGHTBLUE_EX}Phone{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "Phone Information": [haw.get_phone_info]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(phone)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(phone)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "get_phone_info":
                        data = func(phone)
                        if data:
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number:{Fore.LIGHTBLUE_EX}", data.get('query'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Status:{Fore.LIGHTBLUE_EX}", data.get('status'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Type:{Fore.LIGHTBLUE_EX}", data.get('numberType'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid:{Fore.LIGHTBLUE_EX}", data.get('numberValid'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid for Region:{Fore.LIGHTBLUE_EX}", data.get('numberValidForRegion'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country Code:{Fore.LIGHTBLUE_EX}", data.get('numberCountryCode'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Area Code:{Fore.LIGHTBLUE_EX}", data.get('numberAreaCode'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} E.164 Format:{Fore.LIGHTBLUE_EX}", data.get('formatE164'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} National Format:{Fore.LIGHTBLUE_EX}", data.get('formatNational'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} International Format:{Fore.LIGHTBLUE_EX}", data.get('formatInternational'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Continent:{Fore.LIGHTBLUE_EX}", data.get('continent'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country:{Fore.LIGHTBLUE_EX}", data.get('countryName'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Region:{Fore.LIGHTBLUE_EX}", data.get('regionName'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} City:{Fore.LIGHTBLUE_EX}", data.get('city'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Latitude:{Fore.LIGHTBLUE_EX}", data.get('lat'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Longitude:{Fore.LIGHTBLUE_EX}", data.get('lon'))
                            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Timezone:{Fore.LIGHTBLUE_EX}", data.get('timezone'))
                    else:
                        func(phone)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "03" or command == "3":
            ip = input(f"{Fore.LIGHTBLUE_EX}IP  {Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "Hudsonrock API": [haw.hudsonrock_api_ip],
                "IP Information": [haw.geolocation_ip]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(ip)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(ip)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    else:
                        func(ip)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "04" or command == "4":
            categories = {
                "Cameras": [haw.check_cameras],
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    func()
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")

        elif command == "05" or command == "5":
            fullname = input(f"{Fore.LIGHTBLUE_EX}IP  {Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "News": [haw.algolia],
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "PagesJaunes": [haw.pagesjaunes_search],
                "WhitePages": [haw.whitepages_search]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(fullname)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(fullname)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "pagesjaunes_search":
                        pagesjaunes_results = func(fullname)
                        if pagesjaunes_results:
                            for link in pagesjaunes_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PagesJaunes {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "whitepages_search":
                        whitepages_results = func(fullname)
                        if whitepages_results:
                            for link in whitepages_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} WhitePages {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    else:
                        func(fullname)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "06" or command == "6":
            bitcoin = input(f"{Fore.LIGHTBLUE_EX}Bitcoin{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "BlockChain": [haw.get_bitcoin_info]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(bitcoin)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(bitcoin)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    else:
                        func(bitcoin)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "07" or command == "7":
            file = input(f"{Fore.LIGHTBLUE_EX}File .exe{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "PyInstaller Information": [haw.get_pe_info]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    func(file)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "08" or command == "8":
            mac = input(f"{Fore.LIGHTBLUE_EX}MAC Address{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "MAC Information": [haw.get_pe_info]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(mac)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(mac)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "get_pe_info":
                        result = haw.mac_address_lookup(mac)
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} MAC Prefix: {result.get('macPrefix', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Company: {result.get('company', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Address: {result.get('address', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country: {result.get('country', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} MAC Block Start: {result.get('blockStart', 'N/A')} - {result.get('blockEnd', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Block Size: {result.get('blockSize', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Block Type: {result.get('blockType', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Updated on: {result.get('updated', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Is Random: {result.get('isRand', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Is Private: {result.get('isPrivate', 'N/A')}")
                    else:
                        func(mac)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "09" or command == "9":
            vin_number = input(f"{Fore.LIGHTBLUE_EX}VIN{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            categories = {
                "Ahmia": [haw.extract_links_ahmia],
                "Doxbin": [haw.doxbin_search],
                "PasteBin": [haw.pastebin_search],
                "VIN Information": [haw.get_vehicle_info]
            }   
            with Progress() as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    sleep(0.1)
            for category, functions in categories.items():
                banner(category)
                for func in functions:
                    if func.__name__ == "pastebin_search":
                        pastebin_results = func(vin_number)
                        if pastebin_results:
                            for link in pastebin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    elif func.__name__ == "doxbin_search":
                        doxbin_results = func(vin_number)
                        if doxbin_results:
                            for link in doxbin_results:
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Doxbin {Fore.LIGHTCYAN_EX}→{Fore.LIGHTBLUE_EX} {link}")
                    else:
                        func(vin_number)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "00" or command == "0":
            print(
                f'''{Fore.LIGHTWHITE_EX}
Hawker+ is not yet available, if you want to be notified when it arrives, join the discord
https://discord.gg/KRjzDPzDbx

Hawker+ is a more advanced version of the OSINT tool that provides access to large databases for investigative purposes. 
This tool is intended for law enforcement and cybersecurity professionals.

1. Contact Me: Reach out to me via Discord for further information and access to the tool. 
My Discord username is: `0.d4y`.

2. Make a Donation: To support the development of this tool, a donation of **1 XMR (Monero)** is required. Please send the 
donation to the following 

Monero address: 455RrwkuryVRioADddHWfGXrWHSLk4n1DHX36E4tKkBHScps4CeFwMWVemyqgWkL5eYf5L2zRVkgQB4Y9dwaechDKqQzC7p

3. Confirmation: After completing the donation, send me the following:
    - The transaction ID (txid)** of your Monero transaction.
    - A screenshot** of your donation confirmation.

4. Receive the Tool: Once I confirm your donation, I will provide you with the link to 
download the Hawker+ tool in a `.7z` archive format.
                '''
            )
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")

        elif command == "11":
            docx_path = input(f"{Fore.LIGHTBLUE_EX}DOCX File{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            metadata = haw.extract_metadata(docx_path)
            pprint(metadata) 
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "10":
            pdf_path = input(f"{Fore.LIGHTBLUE_EX}PDF File{Fore.LIGHTWHITE_EX} →{Fore.LIGHTWHITE_EX} ")
            haw.extract_pdf_metadata(pdf_path)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
if __name__ == "__main__":
    main()


"""
In the next update I will make the code cleaner.
"""

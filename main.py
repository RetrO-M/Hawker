from warnings                                                 import filterwarnings
from cryptography.hazmat.primitives.ciphers                   import Cipher, algorithms, modes
from colorama                                                 import Fore, init
from os                                                       import system, path, listdir
from requests                                                 import get, post, Session, RequestException, exceptions
from re                                                       import compile, search, IGNORECASE
from hashlib                                                  import sha1, sha256, md5
from bs4                                                      import BeautifulSoup
from random                                                   import choice
from urllib.parse                                             import urlencode, urljoin, quote
from time                                                     import sleep
from json                                                     import dumps
from pefile                                                   import PE   
from datetime                                                 import datetime, UTC
import os

init()
filterwarnings("ignore", category=UserWarning, module="cryptography")

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
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71"
            ]),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com",
            "Origin": "https://www.google.com"
        }
        self.KEY = b"0123456789abcdef"

#region Email Information 
    def decrypt_file(self, file_path):
        with open(file_path, "rb") as file:
            iv = file.read(16)
            encrypted_data = file.read()

        decryptor = Cipher(algorithms.AES(self.KEY), modes.CBC(iv)).decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        return decrypted_data.rstrip(decrypted_data[-1:]).decode("utf-8", errors="ignore")

    def mask_password(self, password):
        if len(password) > 2:
            return password[0] + "*" * (len(password) - 2) + password[-1]
        return "*" * len(password)

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
                                masked_password = self.mask_password(password)
                                print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTWHITE_EX}] Compromised password {folder_name}: {Fore.LIGHTCYAN_EX}{masked_password}")
                    except Exception:
                        continue
    


    def check_chess_email(self, email):
        url = f"https://www.chess.com/callback/email/available?email={email}"
        
        try:
            response = get(url, headers=self.headers)
            data = response.json()
        
            if data.get('isEmailAvailable') == True:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Chess.com account") 
            elif data.get('isEmailAvailable') == False:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com Account Found") 
            else:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com account") 
        except:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Chess.com account")

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
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Duolingo account")
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
                        print(f" {Fore.LIGHTWHITE_EX}├──ID:{Fore.LIGHTRED_EX} {user['id']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Login:{Fore.LIGHTRED_EX} {user['login']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Avatar URL:{Fore.LIGHTRED_EX} {user['avatar_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Type:{Fore.LIGHTRED_EX} {user['type']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──URL:{Fore.LIGHTRED_EX} {user['url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Repos URL:{Fore.LIGHTRED_EX} {user['repos_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Gists URL:{Fore.LIGHTRED_EX} {user['gists_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Following URL:{Fore.LIGHTRED_EX} {user['following_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Followers URL:{Fore.LIGHTRED_EX} {user['followers_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}├──Events URL:{Fore.LIGHTRED_EX} {user['events_url']}")
                        print(f" {Fore.LIGHTWHITE_EX}└──Received Events URL:{Fore.LIGHTRED_EX} {user['received_events_url']}")
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No GitHub account found for this email.")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {response.status_code}")
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} An error occurred: {e}")

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
                    print(f" {Fore.LIGHTWHITE_EX}├──Gravatar Profile:{Fore.LIGHTRED_EX} https://gravatar.com/{email_hash}")
                    print(f" {Fore.LIGHTWHITE_EX}├──Display Name:{Fore.LIGHTRED_EX} {display_name}")
                    print(f" {Fore.LIGHTWHITE_EX}├──Preferred Username:{Fore.LIGHTRED_EX} {preferred_username}")
                    print(f" {Fore.LIGHTWHITE_EX}├──Hash:{Fore.LIGHTRED_EX} {email_hash}")
                    print(f" {Fore.LIGHTWHITE_EX}└──Profile Photo:{Fore.LIGHTRED_EX} {photo_url}")
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Gravatar account found.")
            elif response.status_code == 404:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Gravatar account associated with this email.")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {response.status_code}")
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} An error occurred: {e}")

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
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pinterest account")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pinterest account")

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
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pornhub account")
                elif response_json.get('email') == "create_account_failed":
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pornhub Account Found")
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pornhub account")

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
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Spotify account")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Spotify account")

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
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Twitter account")
        except Exception as e:
            pass

    def wordpress_email(self, email):
        response = get(f'https://public-api.wordpress.com/rest/v1.1/users/{email}/auth-options', headers=self.headers)

        if '"email_verified":true' in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Wordpress Account Found')
        else:
            print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Wordpress account')

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
                else:
                    print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Picsart Account")

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
            else:
                print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Bitmoji Account')

        except Exception as e:
            pass

    def mewe(self, email):
        url = f'https://mewe.com/api/v2/auth/checkEmail?email={email}'
        response = get(url, headers=self.headers)
        if "Email already taken" in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Mewe Account Found')
        else:
            print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Mewe Account')        

    def firefox(self, email):
        data = {
            'email': email
        }
        response = post('https://api.accounts.firefox.com/v1/account/status', data=data)
        if "true" in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Firefox Account Found')
        else:
            print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Firefox Account')   

    def xnxx(self, email):
        response = get(f'https://www.xnxx.com/account/checkemail?email={email}')
        if "This email is already in use or its owner has excluded it from our website." in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} XnXX Account Found')
        else:
            print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No XnXX Account')   

    def xvideos(self, email):
        params = {
            'email': email
        }
        response = get(f'https://www.xvideos.com/account/checkemail', params=params)
        if "This email is already in use or its owner has excluded it from our website." in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Xvideos Account Found')
        else:
            print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Xvideos Account')  
 
    def Patreon(self, email):
        data = {
            'email': email
        }
        response = post('https://www.plurk.com/Users/isEmailFound', data=data)

        if "True" in response.text:
            print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Patreon Account Found')
        else:
            print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Patreon Account')        

    def hudsonrock_api_email(self, text):
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={text}"
        response = get(url, headers=self.headers)
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
                print(f" {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTRED_EX} ", computer_name)
                print(f" {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTRED_EX} ", operating_system)
                print(f" {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTRED_EX} ", ip)
                print(f" {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTRED_EX} ", malware_path)
                print(f" {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTRED_EX} ", date_compromised)
                print(f" {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTRED_EX} ", antiviruses)
                print(f" {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTRED_EX} ", ', '.join(top_logins))
                print(f" {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTRED_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")

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
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date:{Fore.LIGHTRED_EX} {date_var}')
                if sendr_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Sender:{Fore.LIGHTRED_EX} {sendr_var}')
                if subj_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Subject:{Fore.LIGHTRED_EX} {subj_var}')
                if url_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} URL:{Fore.LIGHTRED_EX} {url_var}')
                if leak_var:
                    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Leak:{Fore.LIGHTRED_EX} {leak_var}')
                print('\n')


#endregion

#region Phone Information

    def get_phone_info(self, phone_number):
        url = f"http://phone-number-api.com/json/?number={phone_number}"
        response = get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def hudsonrock_api_email(self, text):
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={text}"
        response = get(url, headers=self.headers)
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
                print(f" {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTRED_EX} ", computer_name)
                print(f" {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTRED_EX} ", operating_system)
                print(f" {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTRED_EX} ", ip)
                print(f" {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTRED_EX} ", malware_path)
                print(f" {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTRED_EX} ", date_compromised)
                print(f" {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTRED_EX} ", antiviruses)
                print(f" {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTRED_EX} ", ', '.join(top_logins))
                print(f" {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTRED_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")

#endregion

#region IP information
    def geolocation_ip(self, ip):
        url = f"https://ipwhois.app/json/{ip}"
        respon = get(url, headers=self.headers)
        if respon.status_code == 200:
            result = respon.json() 
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP : ", result.get("ip"))
            print(f" {Fore.LIGHTWHITE_EX}├──Country :{Fore.LIGHTRED_EX} ", result.get("country"))
            print(f" {Fore.LIGHTWHITE_EX}├──Region :{Fore.LIGHTRED_EX} ", result.get("region"))
            print(f" {Fore.LIGHTWHITE_EX}├──City :{Fore.LIGHTRED_EX} ", result.get("city"))
            print(f" {Fore.LIGHTWHITE_EX}├──Location : {Fore.LIGHTRED_EX}", f"{result.get('latitude')}, {result.get('longitude')}")
            print(f" {Fore.LIGHTWHITE_EX}├──ISP : {Fore.LIGHTRED_EX}", result.get("isp"))
            print(f" {Fore.LIGHTWHITE_EX}└──ASN : {Fore.LIGHTRED_EX}", result.get("asn"))
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Unable to fetch data for IP: {ip}")

    def hudsonrock_api_ip(self, text):
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-ip?ip={text}"
        response = get(url, headers=self.headers)
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
                print(f" {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTRED_EX} ", computer_name)
                print(f" {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTRED_EX} ", operating_system)
                print(f" {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTRED_EX} ", ip)
                print(f" {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTRED_EX} ", malware_path)
                print(f" {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTRED_EX} ", date_compromised)
                print(f" {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTRED_EX} ", antiviruses)
                print(f" {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTRED_EX} ", ', '.join(top_logins))
                print(f" {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTRED_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")

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

#region Bitcoin Information

    def get_bitcoin_info(self, bitcoin):
        url = f"https://blockchain.info/rawaddr/{bitcoin}"
        
        try:
            response = get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} ERROR : {response.status_code}")
                return
            
            data = response.json()

            total_balance = data.get('final_balance', 0) / 1e8
            total_transactions = data.get('n_tx', 0)
            total_received = data.get('total_received', 0) / 1e8 
            total_sent = data.get('total_sent', 0) / 1e8 

            first_tx_time = 'None'
            if data.get('txs', []):
                first_tx_time = data['txs'][0].get('time', 'None')

            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitcoin :{Fore.LIGHTRED_EX} {bitcoin}")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Balance :{Fore.LIGHTRED_EX} {total_balance} BTC")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Transactions : {Fore.LIGHTRED_EX}{total_transactions}")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Received : {Fore.LIGHTRED_EX}{total_received} BTC")
            print(f" {Fore.LIGHTWHITE_EX}├──Total Sent :{Fore.LIGHTRED_EX} {total_sent} BTC")
            print(f" {Fore.LIGHTWHITE_EX}└──First Transaction (timestamp) :{Fore.LIGHTRED_EX} {first_tx_time}")
            
        except Exception as e:
            pass

#endregion

#region Google Dorking

    def doxbin_search(self, text):
        query = f'"{text}" site:doxbin.org'
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
                if 'doxbin.org' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
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


    def instagram_search(self, text):
        query = f"{text} site:instagram.com"
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
                if 'instagram.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def twitter_search(self, text):
        query = f"{text} site:x.com"
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
                if 'x.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def youtube_search(self, text):
        query = f"{text} site:youtube.com"
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
                if 'youtube.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def facebook_search(self, text):
        query = f"{text} site:facebook.com"
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
                if 'facebook.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def reddit_search(self, text):
        query = f"{text} site:reddit.com"
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

    def snapchat_search(self, text):
        query = f"{text} site:snapchat.com"
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
                if 'snapchat.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def github_search(self, text):
        query = f"{text} site:github.com"
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
                if 'github.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
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


    def pagejaunes_search(self, text):
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
#endregion


#region Cameras

    def check_cameras(self):
        for country_code, path in self.countries.items():
            if os.path.exists(path):
                print()
                decrypted_content = self.decrypt_file(path)
                for line in decrypted_content.split("\n"):
                    url = line.strip()
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} (Camera {country_code}) :{Fore.LIGHTRED_EX} {url}")
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} The file for {country_code} does not exist.")

#endregion

#region PyInstaller

    def get_pe_info(self, file):
        file_path = file
        try:
            pe = PE(file_path)
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                {Fore.LIGHTRED_EX}  General information {Fore.LIGHTWHITE_EX}                ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} File Name : {path.basename(file_path)}")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} File size : {path.getsize(file_path)} octets")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Entrypoint : 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:X}")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ImageBase : 0x{pe.OPTIONAL_HEADER.ImageBase:X}")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Machine : {hex(pe.FILE_HEADER.Machine)}")
            timestamp = pe.FILE_HEADER.TimeDateStamp
            if timestamp > 0:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} TimeDateStamp : {datetime.fromtimestamp(timestamp, UTC)}")
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                    {Fore.LIGHTRED_EX}    Selections {Fore.LIGHTWHITE_EX}                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            for section in pe.sections:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {section.Name.decode().strip()} - VA: {hex(section.VirtualAddress)}, Size: {section.Misc_VirtualSize}, Entropie: {section.get_entropy()}")
            
            
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTRED_EX}       DLL   {Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {entry.dll.decode()} : {[imp.name.decode() if imp.name else 'Ordinal' for imp in entry.imports]}")
            
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTRED_EX}     Version {Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            with open(file_path, "rb") as f:
                content = f.read()
                match = search(rb'python(\d{2,3})', content, IGNORECASE)
                if match:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Version Python : Python{match.group(1).decode()}")
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTRED_EX}   HASH {Fore.LIGHTWHITE_EX}                        ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            with open(file_path, "rb") as f:
                file_data = f.read()
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} MD5 : {md5(file_data).hexdigest()}")
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SHA-1 : {sha1(file_data).hexdigest()}")
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SHA-256 : {sha256(file_data).hexdigest()}")
            

            pe.close()
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {e}")

#endregion

#region Main
def title():
    system('clear || cls')
    print(
        f'''
{Fore.LIGHTGREEN_EX}██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗███████╗██████╗ 
{Fore.LIGHTWHITE_EX}██║  ██║██╔══██╗██║    ██║██║ ██╔╝██╔════╝██╔══██╗
{Fore.LIGHTCYAN_EX}███████║███████║██║ █╗ ██║█████╔╝ █████╗  ██████╔╝
{Fore.LIGHTWHITE_EX}██╔══██║██╔══██║██║███╗██║██╔═██╗ ██╔══╝  ██╔══██╗
{Fore.LIGHTGREEN_EX}██║  ██║██║  ██║╚███╔███╔╝██║  ██╗███████╗██║  ██║
{Fore.LIGHTWHITE_EX}╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Fore.LIGHTGREEN_EX}1.{Fore.LIGHTWHITE_EX} Email Information
{Fore.LIGHTCYAN_EX}2.{Fore.LIGHTWHITE_EX} Phone Information
{Fore.LIGHTGREEN_EX}3.{Fore.LIGHTWHITE_EX} Person Information
{Fore.LIGHTCYAN_EX}4.{Fore.LIGHTWHITE_EX} IP Information
{Fore.LIGHTGREEN_EX}5.{Fore.LIGHTWHITE_EX} MAC Information
{Fore.LIGHTCYAN_EX}6.{Fore.LIGHTWHITE_EX} Bitcoin Information
{Fore.LIGHTGREEN_EX}7.{Fore.LIGHTWHITE_EX} Cameras Information
{Fore.LIGHTCYAN_EX}8.{Fore.LIGHTWHITE_EX} PyInstaller Information
        '''
    )

def main():
    while True:
        haw = Hawker()
        title()
        command = input(f'{Fore.LIGHTGREEN_EX}H{Fore.LIGHTWHITE_EX}A{Fore.LIGHTCYAN_EX}W{Fore.LIGHTWHITE_EX}K{Fore.LIGHTGREEN_EX}E{Fore.LIGHTWHITE_EX}R{Fore.LIGHTCYAN_EX}>{Fore.LIGHTWHITE_EX} ')

        if command == "01" or command == "1":
            email = input(f"{Fore.RED}•{Fore.LIGHTWHITE_EX} Email {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ")
            print(
                f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                    {Fore.LIGHTRED_EX}   Data Breach {Fore.LIGHTWHITE_EX}                   ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.search_database(email)
            print(
                f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                {Fore.LIGHTRED_EX}    Social Networks  {Fore.LIGHTWHITE_EX}                 ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.check_github_email(email)
            haw.picsart(email)
            haw.pornhub(email)
            haw.check_spotify_email(email)
            haw.check_twitter_email(email)
            haw.check_chess_email(email)
            haw.check_duolingo_email(email)
            haw.check_gravatar_email(email)
            haw.check_pinterest_email(email)
            haw.bitmoji(email)
            haw.mewe(email)
            haw.firefox(email)
            haw.xnxx(email)
            haw.xvideos(email)
            haw.Patreon(email)

            doxbin_results = haw.doxbin_search(email)
            if doxbin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX} DOXBIN{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in doxbin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(email)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} PASTEBIN {Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            print(
                f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                  {Fore.LIGHTRED_EX}    HUDSONROCK  {Fore.LIGHTWHITE_EX}                    ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_api_email(email)

            print(
                f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} WIKI LEAKS {Fore.LIGHTWHITE_EX}                    ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.wikileaks_search(email)


            reddit_results = haw.reddit_search(email)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                       {Fore.LIGHTRED_EX}Reddit.com{Fore.LIGHTWHITE_EX}                     ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            snapchat_results = haw.snapchat_search(email)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                     {Fore.LIGHTRED_EX}Snapchat.com{Fore.LIGHTWHITE_EX}                     ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(email)
            if reddit_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                     {Fore.LIGHTRED_EX}  Github.com  {Fore.LIGHTWHITE_EX}                   ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(email)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                  {Fore.LIGHTRED_EX}  Instagram.com   {Fore.LIGHTWHITE_EX}                  ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(email)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX}  X.com{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            youtube_results = haw.youtube_search(email)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                    {Fore.LIGHTRED_EX}  Youtube.com   {Fore.LIGHTWHITE_EX}                  ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(email)
            if facebook_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                    {Fore.LIGHTRED_EX}  FaceBook.com{Fore.LIGHTWHITE_EX}                    ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "02" or command == "2":
            phone = input(f"{Fore.RED}•{Fore.LIGHTWHITE_EX} Phone {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ")

            doxbin_results = haw.doxbin_search(phone)
            if doxbin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX} DOXBIN{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in doxbin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(phone)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} PASTEBIN {Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")


            data = haw.get_phone_info(phone)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
╔══════════════════════════════════════════════════════╗
║                {Fore.LIGHTRED_EX}  Phone Information{Fore.LIGHTWHITE_EX}                   ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            if data:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number:{Fore.LIGHTRED_EX}", data.get('query'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Status:{Fore.LIGHTRED_EX}", data.get('status'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Type:{Fore.LIGHTRED_EX}", data.get('numberType'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid:{Fore.LIGHTRED_EX}", data.get('numberValid'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid for Region:{Fore.LIGHTRED_EX}", data.get('numberValidForRegion'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country Code:{Fore.LIGHTRED_EX}", data.get('numberCountryCode'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Area Code:{Fore.LIGHTRED_EX}", data.get('numberAreaCode'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} E.164 Format:{Fore.LIGHTRED_EX}", data.get('formatE164'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} National Format:{Fore.LIGHTRED_EX}", data.get('formatNational'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} International Format:{Fore.LIGHTRED_EX}", data.get('formatInternational'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Continent:{Fore.LIGHTRED_EX}", data.get('continent'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country:{Fore.LIGHTRED_EX}", data.get('countryName'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Region:{Fore.LIGHTRED_EX}", data.get('regionName'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} City:{Fore.LIGHTRED_EX}", data.get('city'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Latitude:{Fore.LIGHTRED_EX}", data.get('lat'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Longitude:{Fore.LIGHTRED_EX}", data.get('lon'))
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Timezone:{Fore.LIGHTRED_EX}", data.get('timezone'))
            else:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error retrieving data.")


            reddit_results = haw.reddit_search(phone)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                       {Fore.LIGHTRED_EX}Reddit.com{Fore.LIGHTWHITE_EX}                     ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            snapchat_results = haw.snapchat_search(phone)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                     {Fore.LIGHTRED_EX}Snapchat.com{Fore.LIGHTWHITE_EX}                     ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(phone)
            if reddit_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                     {Fore.LIGHTRED_EX}  Github.com  {Fore.LIGHTWHITE_EX}                   ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(phone)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                  {Fore.LIGHTRED_EX}  Instagram.com   {Fore.LIGHTWHITE_EX}                  ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(phone)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX}  X.com{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            youtube_results = haw.youtube_search(phone)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                    {Fore.LIGHTRED_EX}  Youtube.com   {Fore.LIGHTWHITE_EX}                  ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(phone)
            if facebook_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                    {Fore.LIGHTRED_EX}  FaceBook.com{Fore.LIGHTWHITE_EX}                    ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")

        elif command == "03" or command == "3":
            fullname = input(f'{Fore.RED}•{Fore.LIGHTWHITE_EX} Full Name {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ')

            doxbin_results = haw.doxbin_search(fullname)
            if doxbin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX} DOXBIN{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in doxbin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(fullname)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} PASTEBIN {Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")



            whitepages_results = haw.whitepages_search(fullname)
            if whitepages_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX}  White Pages {Fore.LIGHTWHITE_EX}                  ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in whitepages_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pagesjaunes_results = haw.pagejaunes_search(fullname)
            if pagesjaunes_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                    {Fore.LIGHTRED_EX}  PagesJaunes {Fore.LIGHTWHITE_EX}                    ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pagesjaunes_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")

        elif command == "04" or command == "4":
            ip = input(f'{Fore.RED}•{Fore.LIGHTWHITE_EX} IP {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ')

            doxbin_results = haw.doxbin_search(ip)
            if doxbin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX} DOXBIN{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in doxbin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(ip)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} PASTEBIN {Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            print(
                f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                   {Fore.LIGHTRED_EX}  IP Information{Fore.LIGHTWHITE_EX}                   ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.geolocation_ip(ip)
            print(
                f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                  {Fore.LIGHTRED_EX}    HUDSONROCK{Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_api_ip(ip)



            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "05" or command == "5":
            mac = input(f'{Fore.RED}•{Fore.LIGHTWHITE_EX} MAC Address {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ')
            print(
                    f'''  {Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                 {Fore.LIGHTRED_EX}   MAC Information {Fore.LIGHTWHITE_EX}                  ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
            result = haw.mac_address_lookup(mac)
            
            if "error" in result:
                print(f"{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {result['error']}")
            else:
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


            doxbin_results = haw.doxbin_search(mac)
            if doxbin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX} DOXBIN{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in doxbin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(mac)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} PASTEBIN {Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")


            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")


        elif command == "06" or command == "6":
            bitcoin = input(f"{Fore.RED}•{Fore.LIGHTWHITE_EX} Bitcoin {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
╔══════════════════════════════════════════════════════╗
║               {Fore.LIGHTRED_EX}   Bitcoin Information {Fore.LIGHTWHITE_EX}                ║
╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.get_bitcoin_info(bitcoin)


            doxbin_results = haw.doxbin_search(bitcoin)
            if doxbin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                        {Fore.LIGHTRED_EX} DOXBIN{Fore.LIGHTWHITE_EX}                       ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in doxbin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(bitcoin)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
╔══════════════════════════════════════════════════════╗
║                      {Fore.LIGHTRED_EX} PASTEBIN {Fore.LIGHTWHITE_EX}                      ║
╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} PasteBin {Fore.LIGHTCYAN_EX}:{Fore.LIGHTWHITE_EX} {link}")
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "07" or command == "7":
            haw.check_cameras()
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
        elif command == "08" or command == "8":
            file = input(f"{Fore.RED}•{Fore.LIGHTWHITE_EX} File {Fore.LIGHTRED_EX}:{Fore.LIGHTWHITE_EX} ")
            haw.get_pe_info(file)
            input(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}>{Fore.LIGHTWHITE_EX}] Type 'enter' to continue. . .")
#endregion
if __name__ == "__main__":
    main()

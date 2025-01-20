from colorama                                                 import Fore, init
from os                                                       import system
from requests                                                 import get, post, Session, RequestException, exceptions
from re                                                       import compile
from hashlib                                                  import md5
from bs4                                                      import BeautifulSoup
from random                                                   import choice
from urllib.parse                                             import urlencode, urljoin, quote
from time                                                     import sleep

init()

class Hawker:
    def __init__(self):
        self.headers = {
            "User-Agent": choice([
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            ]),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com",
            "Origin": "https://www.google.com"
        }

    def doxbin_search(self, text):
        query = f"{text} site:doxbin.org"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }
        url_with_params = url + urlencode(params)
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'doxbin.org' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'doxbin.org' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None


    def pastebin_search(self, text):
        query = f"{text} site:pastebin.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }
        url_with_params = url + urlencode(params)
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'pastebin.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'pastebin.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            return links
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None


    def check_chess_email(self, email):
        url = f"https://www.chess.com/callback/email/available?email={email}"
        
        try:
            response = get(url, headers=self.headers)
            data = response.json()
        
            if data.get('isEmailAvailable') == True:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Chess.com account") 
            elif data.get('isEmailAvailable') == False:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com Account Found") 
            else:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com account") 
        except:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Chess.com account")

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
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Duolingo account")
                else:
                    valid = response.json()['users'][0]['username']
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Duolingo Account Found")

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
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} GitHub Profile: https://github.com/{user['login']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──ID:{Fore.LIGHTMAGENTA_EX} {user['id']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Login:{Fore.LIGHTMAGENTA_EX} {user['login']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Avatar URL:{Fore.LIGHTMAGENTA_EX} {user['avatar_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Type:{Fore.LIGHTMAGENTA_EX} {user['type']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──URL:{Fore.LIGHTMAGENTA_EX} {user['url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Repos URL:{Fore.LIGHTMAGENTA_EX} {user['repos_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Gists URL:{Fore.LIGHTMAGENTA_EX} {user['gists_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Following URL:{Fore.LIGHTMAGENTA_EX} {user['following_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Followers URL:{Fore.LIGHTMAGENTA_EX} {user['followers_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Events URL:{Fore.LIGHTMAGENTA_EX} {user['events_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}└──Received Events URL:{Fore.LIGHTMAGENTA_EX} {user['received_events_url']}")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No GitHub account found for this email.")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {response.status_code}")
        except Exception as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} An error occurred: {e}")

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
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Gravatar Account Found")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Gravatar Profile:{Fore.LIGHTMAGENTA_EX} https://gravatar.com/{email_hash}")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Display Name:{Fore.LIGHTMAGENTA_EX} {display_name}")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Preferred Username:{Fore.LIGHTMAGENTA_EX} {preferred_username}")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Hash:{Fore.LIGHTMAGENTA_EX} {email_hash}")
                    print(f"     {Fore.LIGHTWHITE_EX}└──Profile Photo:{Fore.LIGHTMAGENTA_EX} {photo_url}")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Gravatar account found.")
            elif response.status_code == 404:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Gravatar account associated with this email.")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {response.status_code}")
        except Exception as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} An error occurred: {e}")

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
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pinterest Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pinterest account")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pinterest account")

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
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pornhub account")
                elif response_json.get('email') == "create_account_failed":
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pornhub Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pornhub account")

        except Exception as e:
            pass

    def check_spotify_email(self, target: str):
        url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
        
        try:
            response = get(url, headers=self.headers)

            if response.status_code == 200:
                responseData = response.json()
            
                if responseData.get('status') == 20:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Spotify Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Spotify account")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Spotify account")

        except Exception as e:
            pass

    def check_twitter_email(self, email):
        url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
        
        try:
            response = get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if not data["valid"]:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Twitter Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Twitter account")
        except Exception as e:
            pass

    def wordpress_email(self, email):
        response = get(f'https://public-api.wordpress.com/rest/v1.1/users/{email}/auth-options', headers=self.headers)

        if '"email_verified":true' in response.text:
            print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Wordpress Account Found')
        else:
            print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Wordpress account')

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
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Picsart Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Picsart Account")

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
                print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitmoji Account Found')
            else:
                print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Bitmoji Account')

        except Exception as e:
            pass

    def hudsonrock_api(self, text):
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
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} STEALERS: ")
                print(f"     {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTMAGENTA_EX} ", computer_name)
                print(f"     {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTMAGENTA_EX} ", operating_system)
                print(f"     {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTMAGENTA_EX} ", ip)
                print(f"     {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTMAGENTA_EX} ", malware_path)
                print(f"     {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTMAGENTA_EX} ", date_compromised)
                print(f"     {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTMAGENTA_EX} ", antiviruses)
                print(f"     {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTMAGENTA_EX} ", ', '.join(top_logins))
                print(f"     {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTMAGENTA_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")

    def wikileaks_search(self, text):
        URL = f'https://search.wikileaks.org/?query={text}&exact_phrase=&include_external_sources=True&order_by=newest_document_date&page=1'
        response = get(URL, headers=self.headers)
        
        if response.status_code != 200:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error retrieving the page.")
            return
        
        sleep(1)

        soup = BeautifulSoup(response.content, "lxml")
        divtag_var = soup.find_all('div', {'class': 'result'})
        if not divtag_var:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No results found for the search.")
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
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date:{Fore.LIGHTMAGENTA_EX} {date_var}')
                if sendr_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Sender:{Fore.LIGHTMAGENTA_EX} {sendr_var}')
                if subj_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Subject:{Fore.LIGHTMAGENTA_EX} {subj_var}')
                if url_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} URL:{Fore.LIGHTMAGENTA_EX} {url_var}')
                if leak_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Leak:{Fore.LIGHTMAGENTA_EX} {leak_var}')
                print('\n')

    def instagram_search(self, text):
        query = f"{text} site:instagram.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'instagram.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'instagram.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def twitter_search(self, text):
        query = f"{text} site:x.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'x.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'x.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def youtube_search(self, text):
        query = f"{text} site:youtube.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'youtube.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'youtube.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def facebook_search(self, text):
        query = f"{text} site:facebook.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'facebook.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'facebook.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def reddit_search(self, text):
        query = f"{text} site:reddit.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'reddit.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'reddit.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def snapchat_search(self, text):
        query = f"{text} site:snapchat.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'snapchat.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'snapchat.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def github_search(self, text):
        query = f"{text} site:github.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'github.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'github.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def get_phone_info(self, phone_number):
        url = f"http://phone-number-api.com/json/?number={phone_number}"
        response = get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def google_dorking_name(self, text, file_type):
        query = f"{text} filetype:{file_type}"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if link.endswith(file_type):
                        links.append(link)
                elif href.endswith(file_type):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def pagesjaunes_search(self, text):
        query = f"{text} site:pagesjaunes.fr"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'pagesjaunes.fr' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'pagesjaunes.fr' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None
        
    def whitepages_search(self, text):
        query = f"{text} site:whitepages.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'whitepages.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'whitepages.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def mastodon_social(self, fullname):
        encoded_name = quote(fullname)
        url = f"https://mastodon.social/api/v2/search?q={encoded_name}&type=accounts"

        response = get(url, headers=self.headers)
        data = response.json()

        if 'accounts' in data:
            for account in data['accounts']:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ID:{Fore.LIGHTMAGENTA_EX} {account['id']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Username:{Fore.LIGHTMAGENTA_EX} {account['username']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Account:{Fore.LIGHTMAGENTA_EX} {account['acct']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Display Name:{Fore.LIGHTMAGENTA_EX} {account['display_name']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Locked:{Fore.LIGHTMAGENTA_EX} {account['locked']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bot:{Fore.LIGHTMAGENTA_EX} {account['bot']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Created At:{Fore.LIGHTMAGENTA_EX} {account['created_at']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Note:{Fore.LIGHTMAGENTA_EX} {account['note']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Profile URL:{Fore.LIGHTMAGENTA_EX} {account['url']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Avatar URL:{Fore.LIGHTMAGENTA_EX} {account['avatar']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Header URL:{Fore.LIGHTMAGENTA_EX} {account['header']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Followers:{Fore.LIGHTMAGENTA_EX} {account['followers_count']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Following:{Fore.LIGHTMAGENTA_EX} {account['following_count']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Statuses:{Fore.LIGHTMAGENTA_EX} {account['statuses_count']}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Last Status:{Fore.LIGHTMAGENTA_EX} {account['last_status_at']}\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No found...")

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

    def geolocation_ip(self, text):
        url = f"https://ipwhois.app/json/{text}"
        respon = get(url, headers=self.headers)
        if respon.status_code == 200:
            result = respon.json() 
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP : ", result.get("ip"))
            print(f"     {Fore.LIGHTWHITE_EX}├──Country :{Fore.LIGHTMAGENTA_EX} ", result.get("country"))
            print(f"     {Fore.LIGHTWHITE_EX}├──Region :{Fore.LIGHTMAGENTA_EX} ", result.get("region"))
            print(f"     {Fore.LIGHTWHITE_EX}├──City :{Fore.LIGHTMAGENTA_EX} ", result.get("city"))
            print(f"     {Fore.LIGHTWHITE_EX}├──Location : {Fore.LIGHTMAGENTA_EX}", f"{result.get('latitude')}, {result.get('longitude')}")
            print(f"     {Fore.LIGHTWHITE_EX}├──ISP : {Fore.LIGHTMAGENTA_EX}", result.get("isp"))
            print(f"     {Fore.LIGHTWHITE_EX}├──Organization :{Fore.LIGHTMAGENTA_EX} ", result.get("org"))
            print(f"     {Fore.LIGHTWHITE_EX}└──ASN : {Fore.LIGHTMAGENTA_EX}", result.get("asn"))
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Unable to fetch data for IP: {ip}")

    def hudsonrock_ip_api(self, text):
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
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} STEALERS: ")
                print(f"     {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTMAGENTA_EX} ", computer_name)
                print(f"     {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTMAGENTA_EX} ", operating_system)
                print(f"     {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTMAGENTA_EX} ", ip)
                print(f"     {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTMAGENTA_EX} ", malware_path)
                print(f"     {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTMAGENTA_EX} ", date_compromised)
                print(f"     {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTMAGENTA_EX} ", antiviruses)
                print(f"     {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTMAGENTA_EX} ", ', '.join(top_logins))
                print(f"     {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTMAGENTA_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")

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

            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitcoin :{Fore.LIGHTMAGENTA_EX} {bitcoin}")
            print(f"     {Fore.LIGHTWHITE_EX}├──Total Balance :{Fore.LIGHTMAGENTA_EX} {total_balance} BTC")
            print(f"     {Fore.LIGHTWHITE_EX}├──Total Transactions : {Fore.LIGHTMAGENTA_EX}{total_transactions}")
            print(f"     {Fore.LIGHTWHITE_EX}├──Total Received : {Fore.LIGHTMAGENTA_EX}{total_received} BTC")
            print(f"     {Fore.LIGHTWHITE_EX}├──Total Sent :{Fore.LIGHTMAGENTA_EX} {total_sent} BTC")
            print(f"     {Fore.LIGHTWHITE_EX}└──First Transaction (timestamp) :{Fore.LIGHTMAGENTA_EX} {first_tx_time}")
            
        except Exception as e:
            pass

    def username_search(self, username):
        urls = [
            f'https://www.youtube.com/@{username}',
            f'https://github.com/{username}',
            f'https://doxbin.org/user/{username}',
            f'https://open.spotify.com/user/{username}',
            f'https://35photo.pro/@{username}',
            f'https://www.chess.com/member/{username}',
            f'https://www.flickr.com/photos/{username}',
            f'https://pastebin.com/u/{username}',
            f'https://www.eyeem.com/u/{username}',
            f'https://mastodon.social/@{username}',
            f'https://steemit.com/@{username}',
            f'https://soundcloud.com/{username}',
            f'https://www.gog.com/u/{username}',
            f'https://rblx.trade/p/{username}'
        ]
        for url in urls:
            response = get(url, allow_redirects=False)
            if response.status_code == 200:
                print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {url}{Fore.LIGHTMAGENTA_EX} | {Fore.LIGHTGREEN_EX}{response.status_code}')
            elif response.status_code == 404:
                print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} {url}{Fore.LIGHTMAGENTA_EX} | {Fore.LIGHTRED_EX}{response.status_code}')
            elif response.status_code == 403:
                print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} {url}{Fore.LIGHTMAGENTA_EX} | {Fore.LIGHTYELLOW_EX}{response.status_code}')
            elif response.status_code == 302:
                print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} {url}{Fore.LIGHTMAGENTA_EX} | {Fore.LIGHTWHITE_EX}{response.status_code}')
            sleep(0.05)

    def hudsonrock_username_api(self, text):
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={text}"
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
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} STEALERS: ")
                print(f"     {Fore.LIGHTWHITE_EX}├──Computer Name:{Fore.LIGHTMAGENTA_EX} ", computer_name)
                print(f"     {Fore.LIGHTWHITE_EX}├──Operating System:{Fore.LIGHTMAGENTA_EX} ", operating_system)
                print(f"     {Fore.LIGHTWHITE_EX}├──IP:{Fore.LIGHTMAGENTA_EX} ", ip)
                print(f"     {Fore.LIGHTWHITE_EX}├──Malware Path:{Fore.LIGHTMAGENTA_EX} ", malware_path)
                print(f"     {Fore.LIGHTWHITE_EX}├──Date Compromised:{Fore.LIGHTMAGENTA_EX} ", date_compromised)
                print(f"     {Fore.LIGHTWHITE_EX}├──AntiViruses:{Fore.LIGHTMAGENTA_EX} ", antiviruses)
                print(f"     {Fore.LIGHTWHITE_EX}├──Top Logins:{Fore.LIGHTMAGENTA_EX} ", ', '.join(top_logins))
                print(f"     {Fore.LIGHTWHITE_EX}└──Passwords:{Fore.LIGHTMAGENTA_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")

    def CompanyClientLogins(self, domain):
        url = f'https://chiasmodon.com/v2/CompanyClientLogins?q={domain}&key=&page=1 '
        response = get(url, headers=self.headers)

        if response.status_code == 200:
            print(f"{response.text}".replace('username', f'{Fore.LIGHTMAGENTA_EX}username{Fore.LIGHTWHITE_EX}').replace('password', f'{Fore.LIGHTGREEN_EX}password{Fore.LIGHTWHITE_EX}').replace('email', f'{Fore.LIGHTCYAN_EX}email{Fore.LIGHTWHITE_EX}').replace('country', f'{Fore.LIGHTCYAN_EX}country{Fore.LIGHTWHITE_EX}').replace('date', f'{Fore.LIGHTCYAN_EX}date{Fore.LIGHTWHITE_EX}').replace('"', f'{Fore.LIGHTYELLOW_EX}"{Fore.LIGHTWHITE_EX}'))

    def CompanyEmployeLogins(self, domain):
        url = f'https://chiasmodon.com/v2/CompanyEmployeLogins?q={domain}&key=&page=1 '
        response = get(url, headers=self.headers)

        if response.status_code == 200:
            print(f"{response.text}".replace('username', f'{Fore.LIGHTMAGENTA_EX}username{Fore.LIGHTWHITE_EX}').replace('password', f'{Fore.LIGHTGREEN_EX}password{Fore.LIGHTWHITE_EX}').replace('email', f'{Fore.LIGHTCYAN_EX}email{Fore.LIGHTWHITE_EX}').replace('country', f'{Fore.LIGHTCYAN_EX}country{Fore.LIGHTWHITE_EX}').replace('date', f'{Fore.LIGHTCYAN_EX}date{Fore.LIGHTWHITE_EX}').replace('"', f'{Fore.LIGHTYELLOW_EX}"{Fore.LIGHTWHITE_EX}'))
    
    def CompanyEmails(self, domain):
        url = f'https://chiasmodon.com/v2/CompanyEmails?q={domain}&key=&page=1 '
        response = get(url, headers=self.headers)

        if response.status_code == 200:
            print(f"{response.text}".replace('"', f'{Fore.LIGHTMAGENTA_EX}"{Fore.LIGHTWHITE_EX}'))

    def subdomain(self, domain):
        path = [
            "signup", "login", "logout", "database", "secret", "app", "sms", "ipv4", "search", 
            "disclaimer", "guest", "book", "buynow", "live", "artists", "demo", "ip", "internet", 
            "malware", "hide", "register", "account", "join", "enroll", "disconnect", "legal", 
            "bot", "history", "help", "username", "login.php", "signup.php", "userinfo.php", "tags", 
            "hits", "porn", "pornstar", "best", "forum", "tos", "privacy", "notice", "file", "menu", 
            "support", "contact", "email", "login.asp", "gay", "categories", "exit", "gifs", "gif", 
            "db", "datastore", "confidential", "private", "hidden", "secure", "password", "application", 
            "software", "program", "text", "message", "web", "online", "network", "cyberspace", "net", 
            "information", "dataset", "records", "details", "statistics", "repository", "archive", 
            "utility", "admin", "owner", "member", "home", "settings", "chat", "friends", "profile", 
            "store", "security", "2fa", "notify", "api", "test", "ssh", "uploader", "administrator", 
            "marketing", "flag", "user", "player", "main", "badge", "feedback", "version", "ascii", 
            "hacking", "pentester", "learn", "dashboard", "workplace", "free", "developer", "room", 
            "rooms", "manage", "view", "share", "proxy", "inject", "sql", "osint", "locate", "location", 
            "avatar", "phone", "social", "token", "id", "delete", "remove", "cat", "anonymous", "emoji", 
            "leave", "left", "shell", "spy", "signin", "market", "create", "video", "rec", "edit", "run", 
            "blog", "group", "about", "tg", "add", "paste", "extensions", "docs", "teams", "discord", 
            "telegram", "faq", "Upgrades", "hoa", "rules", "themes", "item", "buy", "welcome", "en", 
            "fr", "index", "inventory", "users", "accessories", "trades", "premium", "giftcards", "playlist", 
            "feed", "subscriptions", "update", "download", "stars", "project", "packages", "products", 
            "sitemap", "archives", "events", "event", "templates", "services", "icons", "resources", "info", 
            "partners", "graphics", "research", "module", "modules", "index.php", "slogin.php", "socialnetworks", 
            "rss", "img", "default", "keygen", "article", "classroom", "client", "clientes", "clients", "cloud", 
            "cloudflare-resolve-to", "club", "cms", "cn", "co", "community", "ads", "acceptatie", "access", 
            "accounting", "agenda", "alpha", "sex", "ad", "adm", "webmail", "mysql", "autodiscover", "autoconfig", 
            "mobile", "go", "start", "files", "terminal", "linux", "downloads", "win", "windows", "stat", "wiki", 
            "images", "image", "calendar", "stage", "gateway", "unix", "nginx", "wss", "miss", "staging-chat", 
            "release-chat-service", "h2", "paper", "russian", "gf", "site2", "wd", "mls", "printer", "registrar", 
            "ff", "dell", "va", "vl", "avalon", "bugtracker", "offline", "ppc", "ppp", "r25", "e2", "psql", 
            "releasephp", "submit", "backup3", "tel", "dns0", "staging-chat-service", "postfixadmin", "ck", 
            "s20", "sauron", "econ", "liste", "save", "perlbal-release", "lan", "graphics2", "dev-chat", 
            "ana-dev", "shadow", "savvis-dev-commondata", "holiday", "reader", "exmail", "hosting1", "solr", 
            "database2", "name", "ads1", "3img", "coregw1", "che", "mx7", "aries", "devwowza", "np", "n1", "zsb", 
            "mod", "technology", "vod5", "host6", "parents", "imgup-lb", "portaltest", "jwgl", "setup", "reservation", 
            "img8", "enquetes", "ns34", "classified", "mpa", "leads", "urchin", "nav", "ces", "mike", "casper", "99", 
            "tula", "photos4", "microsoft", "thumb", "temp2", "sandd-dev-commondata", "sci", "fs2", "sac", "drweb", 
            "elib", "mir", "asa", "tool", "wh", "seguro", "parts", "tcs", "teknobyen-gw2", "bid", "transparencia", 
            "cic", "vi", "rec", "gifts", "hyperion", "communication", "imap2", "tftp", "moe", "pollux", "tuanwei", 
            "pop1", "mapa", "photos5", "praca", "kiwi", "scs", "cricket", "line", "condor", "w6", "wb", "0", "fz", 
            "geobanner", "vr", "oas", "tts", "http", "gift", "meta", "splash", "media3", "tf", "homes", "grad", "uni", 
            "mds", "5", "mobility", "cy", "anunturi", "ceres", "sx", "sj", "29", "altair", "tim", "singapore", "count", 
            "msa", "rw", "dn", "fin", "sbe", "iis", "estadisticas", "stolav-gw4", "chaos", "vancouver", "eis", 
            "database1", "neptun", "openfire", "find", "sip1", "std", "rpc", "leon", "outgoing", "gauss", "notify", 
            "destiny", "emc", "remote2", "mv", "core2", "nf", "grace", "checkrelay", "oldwebmail", "deal", "k2", 
            "seattle", "s18", "toolbar", "turing", "allegro", "s30", "requests", "request", "ig", "ds", "skin", "snap", 
            "cart", "guestbook", "careers", "product", "testing", "date", "time", "timeline", "vscode", "code", "copyright", 
            "copy"
        ]
        for paths in path:
            url = f'https://{domain}/{paths}'
            response = get(
                url,
                headers=self.headers
            )
            if response.status_code == 200:
                print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {paths}/')

#region TITLE
def title():
    system('cls || clear')
    print(
        f"""{Fore.MAGENTA}
                    ╦ ╦╔═╗╦ ╦╦╔═╔═╗╦═╗
                    ╠═╣╠═╣║║║╠╩╗║╣ ╠╦╝
                   {Fore.LIGHTMAGENTA_EX} ╩ ╩╩ ╩╚╩╝╩ ╩╚═╝╩╚═
        ╔════════════════════════════════════════╗
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 01{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} Email Information{Fore.LIGHTWHITE_EX} - - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 02{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} Phone Information{Fore.LIGHTWHITE_EX} - - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 03{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} Person Information{Fore.LIGHTWHITE_EX}  - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 04{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} MAC Information{Fore.LIGHTWHITE_EX} - - - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 05{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} IP Information{Fore.LIGHTWHITE_EX}  - - - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 06{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} Bitcoin Information{Fore.LIGHTWHITE_EX} - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 07{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} IPv6 Information  {Fore.LIGHTWHITE_EX}- - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 08{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} Username Search{Fore.LIGHTWHITE_EX} - - - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ║{Fore.LIGHTWHITE_EX}-{Fore.LIGHTYELLOW_EX} 09{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} Website Information{Fore.LIGHTWHITE_EX} - - - - - - -{Fore.LIGHTMAGENTA_EX}║
        ╚════════════════════════════════════════╝
        """
    )
#endpoint

#region Main
try:
    while True:
        haw = Hawker()
        title()
        command = input(f'  {Fore.MAGENTA}[{Fore.LIGHTMAGENTA_EX}root{Fore.LIGHTWHITE_EX}@{Fore.LIGHTMAGENTA_EX}Hawker{Fore.LIGHTWHITE_EX} ~{Fore.MAGENTA}]#{Fore.LIGHTGREEN_EX} ')

        if command == "01" or command == "1":
            email = input(f'    {Fore.LIGHTCYAN_EX}Email{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            search_results = haw.doxbin_search(email)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX} DoxBin.org {Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(email)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX}     Pastebin{Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║   {Fore.LIGHTMAGENTA_EX}Result of Social Networking Sites Linked to Email{Fore.LIGHTWHITE_EX}  ║
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
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX} Hudsonrock API {Fore.LIGHTWHITE_EX}                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_api(email)
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX}  WikiLeaks   {Fore.LIGHTWHITE_EX}                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.wikileaks_search(email)


            reddit_results = haw.reddit_search(email)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                       {Fore.LIGHTMAGENTA_EX}Reddit.com{Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            snapchat_results = haw.snapchat_search(email)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX}Snapchat.com{Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(email)
            if reddit_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX}  Github.com  {Fore.LIGHTWHITE_EX}                   ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(email)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                  {Fore.LIGHTMAGENTA_EX}  Instagram.com   {Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(email)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                        {Fore.LIGHTMAGENTA_EX}  X.com{Fore.LIGHTWHITE_EX}                       ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            youtube_results = haw.youtube_search(email)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                    {Fore.LIGHTMAGENTA_EX}  Youtube.com   {Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(email)
            if facebook_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                    {Fore.LIGHTMAGENTA_EX}  FaceBook.com{Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "02" or command == "2":
            phone = input(f'    {Fore.LIGHTCYAN_EX}Phone{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            data = haw.get_phone_info(phone)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                {Fore.LIGHTMAGENTA_EX}  Phone Information{Fore.LIGHTWHITE_EX}                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            if data:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number:{Fore.LIGHTMAGENTA_EX}", data.get('query'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Status:{Fore.LIGHTMAGENTA_EX}", data.get('status'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Type:{Fore.LIGHTMAGENTA_EX}", data.get('numberType'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid:{Fore.LIGHTMAGENTA_EX}", data.get('numberValid'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid for Region:{Fore.LIGHTMAGENTA_EX}", data.get('numberValidForRegion'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country Code:{Fore.LIGHTMAGENTA_EX}", data.get('numberCountryCode'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Area Code:{Fore.LIGHTMAGENTA_EX}", data.get('numberAreaCode'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} E.164 Format:{Fore.LIGHTMAGENTA_EX}", data.get('formatE164'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} National Format:{Fore.LIGHTMAGENTA_EX}", data.get('formatNational'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} International Format:{Fore.LIGHTMAGENTA_EX}", data.get('formatInternational'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Continent:{Fore.LIGHTMAGENTA_EX}", data.get('continent'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country:{Fore.LIGHTMAGENTA_EX}", data.get('countryName'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Region:{Fore.LIGHTMAGENTA_EX}", data.get('regionName'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} City:{Fore.LIGHTMAGENTA_EX}", data.get('city'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Latitude:{Fore.LIGHTMAGENTA_EX}", data.get('lat'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Longitude:{Fore.LIGHTMAGENTA_EX}", data.get('lon'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Timezone:{Fore.LIGHTMAGENTA_EX}", data.get('timezone'))
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error retrieving data.")

            search_results = haw.doxbin_search(phone)
            if search_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX} DoxBin.org {Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(phone)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX}     Pastebin{Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            reddit_results = haw.reddit_search(phone)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                       {Fore.LIGHTMAGENTA_EX}Reddit.com{Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            snapchat_results = haw.snapchat_search(phone)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX}Snapchat.com{Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(phone)
            if reddit_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX}  Github.com  {Fore.LIGHTWHITE_EX}                   ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(phone)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                  {Fore.LIGHTMAGENTA_EX}  Instagram.com   {Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(phone)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                        {Fore.LIGHTMAGENTA_EX}  X.com{Fore.LIGHTWHITE_EX}                       ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            youtube_results = haw.youtube_search(phone)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                    {Fore.LIGHTMAGENTA_EX}  Youtube.com   {Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(phone)
            if facebook_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                    {Fore.LIGHTMAGENTA_EX}  FaceBook.com{Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "03" or command == "3":
            fullname = input(f'    {Fore.LIGHTCYAN_EX}Full Name{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            search_results = haw.doxbin_search(fullname)
            if search_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX} DoxBin.org {Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(fullname)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX}     Pastebin{Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")



            white_results = haw.whitepages_search(fullname)
            if white_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                {Fore.LIGHTMAGENTA_EX}     White Pages  {Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in white_results:
                    if 'whitepages.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            pagejaunes_results = haw.pagesjaunes_search(fullname)
            if pagejaunes_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX}PageJaunes {Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pagejaunes_results:
                    if 'pagesjaunes.fr' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            print(
                    f'''  {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                {Fore.LIGHTMAGENTA_EX}Google Dorking Files{Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            file_types = ["pdf", "xlsx", "docx", "txt", "xls", "doc", "ppt", "rft", "odt", "csv"]
            for file_type in file_types:
                search_results = haw.google_dorking_name(fullname, file_type)
        
                if search_results:
                    for link in search_results:
                        print(f"    {Fore.LIGHTGREEN_EX}[+] {Fore.LIGHTMAGENTA_EX} {file_type.upper()} {Fore.LIGHTWHITE_EX}{link}")

            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                 {Fore.LIGHTMAGENTA_EX}    Mastodon Social {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.mastodon_social(fullname)

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "04" or command == "4":
            mac = input(f'    {Fore.LIGHTCYAN_EX}MAC Address{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')
            print(
                    f'''  {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                 {Fore.LIGHTMAGENTA_EX}   MAC Information {Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
            result = haw.mac_address_lookup(mac)
            
            if "error" in result:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error: {result['error']}")
            else:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} MAC Prefix: {result.get('macPrefix', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Company: {result.get('company', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Address: {result.get('address', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country: {result.get('country', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} MAC Block Start: {result.get('blockStart', 'N/A')} - {result.get('blockEnd', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Block Size: {result.get('blockSize', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Block Type: {result.get('blockType', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Updated on: {result.get('updated', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Is Random: {result.get('isRand', 'N/A')}")
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Is Private: {result.get('isPrivate', 'N/A')}")

            search_results = haw.doxbin_search(mac)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX}    DoxBin.org {Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(mac)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX}  Pastebin{Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")


        elif command == "05" or command == "5":
            ip = input(f'    {Fore.LIGHTCYAN_EX}IP{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            search_results = haw.doxbin_search(ip)
            if search_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX} DoxBin.org{Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(ip)
            if pastebin_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX}  Pastebin{Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX} IP Information   {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.geolocation_ip(ip)
            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                {Fore.LIGHTMAGENTA_EX}     Hudsonrock API  {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_ip_api(ip)
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")

        elif command == "06" or command == "6":
            bitcoin = input(f'    {Fore.LIGHTCYAN_EX}Bitcoin Address{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║               {Fore.LIGHTMAGENTA_EX}   Bitcoin Information {Fore.LIGHTWHITE_EX}                ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.get_bitcoin_info(bitcoin)


            search_results = haw.doxbin_search(bitcoin)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX}  DoxBin.org   {Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(bitcoin)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX}  Pastebin  {Fore.LIGHTWHITE_EX}                    ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")

        elif command == "07" or command == "7":
            ipv6 = input(f'    {Fore.LIGHTCYAN_EX}IPv6{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            search_results = haw.doxbin_search(ipv6)
            if search_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX} DoxBin.org{Fore.LIGHTWHITE_EX}                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(ipv6)
            if pastebin_results:
                print(
                    f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                      {Fore.LIGHTMAGENTA_EX}  Pastebin{Fore.LIGHTWHITE_EX}                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX} IP Information   {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.geolocation_ip(ipv6)

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "08" or command == "8":
            username = input(f'    {Fore.LIGHTCYAN_EX}Username{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')
            print(
                f'''{Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX} Social Network {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )

            haw.username_search(username)

            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                {Fore.LIGHTMAGENTA_EX}     Hudsonrock API  {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_username_api(username)

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "09" or command == "9":
            domain = input(f'    {Fore.LIGHTCYAN_EX}Domain{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')
            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                    {Fore.LIGHTMAGENTA_EX}   Client Logins  {Fore.LIGHTWHITE_EX}                ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.CompanyClientLogins(domain)
            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                   {Fore.LIGHTMAGENTA_EX} Employe Logins   {Fore.LIGHTWHITE_EX}                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.CompanyEmployeLogins(domain)
            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                     {Fore.LIGHTMAGENTA_EX} Company Emails{Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.CompanyEmails(domain)
            print(
                f''' {Fore.LIGHTWHITE_EX}
    ╔══════════════════════════════════════════════════════╗
    ║                  {Fore.LIGHTMAGENTA_EX}  Subdomain Finder{Fore.LIGHTWHITE_EX}                  ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )   
            haw.subdomain(domain)
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")

except Exception as e:
    print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Program Failed: ', e) 
#endpoint

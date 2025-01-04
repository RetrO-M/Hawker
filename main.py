from colorama                                                 import Fore, init
from os                                                       import system
from requests                                                 import get, Session, RequestException, exceptions
from re                                                       import compile
from hashlib                                                  import md5
from bs4                                                      import BeautifulSoup
from random                                                   import choice
from urllib.parse                                             import urlencode, urljoin
from time                                                     import sleep

init()

class Hawker:
    def __init__(self):
        self.headers = {
            "User-Agent": choice([
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.62",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com",
            "Origin": "https://www.google.com"
        }

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
                        print(f"     {Fore.LIGHTWHITE_EX}├──ID:{Fore.LIGHTGREEN_EX} {user['id']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Login:{Fore.LIGHTGREEN_EX} {user['login']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Avatar URL:{Fore.LIGHTGREEN_EX} {user['avatar_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Type:{Fore.LIGHTGREEN_EX} {user['type']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──URL:{Fore.LIGHTGREEN_EX} {user['url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Repos URL:{Fore.LIGHTGREEN_EX} {user['repos_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Gists URL:{Fore.LIGHTGREEN_EX} {user['gists_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Following URL:{Fore.LIGHTGREEN_EX} {user['following_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Followers URL:{Fore.LIGHTGREEN_EX} {user['followers_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}├──Events URL:{Fore.LIGHTGREEN_EX} {user['events_url']}")
                        print(f"     {Fore.LIGHTWHITE_EX}└──Received Events URL:{Fore.LIGHTGREEN_EX} {user['received_events_url']}")
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
                    print(f"     {Fore.LIGHTWHITE_EX}├──Gravatar Profile:{Fore.LIGHTGREEN_EX} https://gravatar.com/{email_hash}")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Display Name:{Fore.LIGHTGREEN_EX} {display_name}")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Preferred Username:{Fore.LIGHTGREEN_EX} {preferred_username}")
                    print(f"     {Fore.LIGHTWHITE_EX}├──Hash:{Fore.LIGHTGREEN_EX} {email_hash}")
                    print(f"     {Fore.LIGHTWHITE_EX}└──Profile Photo:{Fore.LIGHTGREEN_EX} {photo_url}")
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
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date:{Fore.LIGHTGREEN_EX} {date_var}')
                if sendr_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Sender:{Fore.LIGHTGREEN_EX} {sendr_var}')
                if subj_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Subject:{Fore.LIGHTGREEN_EX} {subj_var}')
                if url_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} URL:{Fore.LIGHTGREEN_EX} {url_var}')
                if leak_var:
                    print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Leak:{Fore.LIGHTGREEN_EX} {leak_var}')
                print('\n')


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
                print(f"     {Fore.LIGHTWHITE_EX}├──Computer Name{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", computer_name)
                print(f"     {Fore.LIGHTWHITE_EX}├──Operating System{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", operating_system)
                print(f"     {Fore.LIGHTWHITE_EX}├──IP{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ip)
                print(f"     {Fore.LIGHTWHITE_EX}├──Malware Path{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", malware_path)
                print(f"     {Fore.LIGHTWHITE_EX}├──Date Compromised{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", date_compromised)
                print(f"     {Fore.LIGHTWHITE_EX}├──AntiViruses{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", antiviruses)
                print(f"     {Fore.LIGHTWHITE_EX}├──Top Logins{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_logins))
                print(f"     {Fore.LIGHTWHITE_EX}└──Passwords{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")


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


    def geolocation_ip(self, ip):
        url = f"https://ipwhois.app/json/{ip}"
        respon = get(url, headers=self.headers)
        if respon.status_code == 200:
            result = respon.json() 
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP : ", result.get("ip"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country : ", result.get("country"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Region : ", result.get("region"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} City : ", result.get("city"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Location : ", f"{result.get('latitude')}, {result.get('longitude')}")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ISP : ", result.get("isp"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Organization : ", result.get("org"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ASN : ", result.get("asn"))
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
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Computer Name{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", computer_name)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Operating System{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", operating_system)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ip)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Malware Path{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", malware_path)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date Compromised{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", date_compromised)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} AntiViruses{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", antiviruses)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Top Logins{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_logins))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Passwords{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_passwords), "\n")
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

            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitcoin : {bitcoin}")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Balance : {total_balance} BTC")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Transactions : {total_transactions}")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Received : {total_received} BTC")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Sent : {total_sent} BTC")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} First Transaction (timestamp) : {first_tx_time}")
            
        except Exception as e:
            pass


#region TITLE
def title():
    system('cls || clear')
    print(
        f"""{Fore.LIGHTWHITE_EX}
                          ▓▓████████████████                    
                    ▒▒██▓▓              ▒▒██████░░              
                ▓▓██░░    {Fore.LIGHTCYAN_EX}▓▓██████████████{Fore.LIGHTWHITE_EX}    ██████            
            ██▒▒  ░░██{Fore.LIGHTCYAN_EX}████████████████████{Fore.LIGHTWHITE_EX}████    ██████        
          ██  ▒▒██░░  {Fore.LIGHTCYAN_EX}████████████████████{Fore.LIGHTWHITE_EX}░░▒▒██▒▒  ▓▓████      
        ██  ██        {Fore.LIGHTCYAN_EX}████████    ██████████ {Fore.LIGHTWHITE_EX}   ████  ▒▒████░░  
      ▒▒        {Fore.LIGHTCYAN_EX}    ████████        ████████  {Fore.LIGHTWHITE_EX}    ████    ██████
    ░░░░            {Fore.LIGHTCYAN_EX}██    ██        ████████ {Fore.LIGHTWHITE_EX}       ████  ░░████
    ░░            {Fore.LIGHTCYAN_EX}  ██    ██        ████████ {Fore.LIGHTWHITE_EX}         ████    ██
                  {Fore.LIGHTCYAN_EX}    ▒▒████████████████████  {Fore.LIGHTWHITE_EX}        ██████    
                   {Fore.LIGHTCYAN_EX}   ████████████████████  {Fore.LIGHTWHITE_EX}        ░░██████    
      ░░               {Fore.LIGHTCYAN_EX} ████████████████    {Fore.LIGHTWHITE_EX}      ░░██▒▒████    
          ░░            {Fore.LIGHTCYAN_EX}  ▒▒████████▒▒ {Fore.LIGHTWHITE_EX}         ████            
            ▒▒▒▒░░                          ▒▒██                
                  ░░▒▒██                ▓▓██  
    {Fore.LIGHTWHITE_EX}•{Fore.LIGHTMAGENTA_EX} Author : https://github.com/RetrO-M
    {Fore.LIGHTWHITE_EX}╔════╦──────────────────────────────┐
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTMAGENTA_EX}01 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}Email Information            {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTMAGENTA_EX}02 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}Phone Information            {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTMAGENTA_EX}03 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}Perso Information            {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTMAGENTA_EX}04 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}MAC Information              {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTMAGENTA_EX}05 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}IP Information               {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTMAGENTA_EX}06 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}Bitcoin Information          {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTRED_EX}07 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}IPv6 Information             {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╠════╬──────────────────────────────┤
    {Fore.LIGHTWHITE_EX}║ {Fore.LIGHTRED_EX}08 {Fore.LIGHTWHITE_EX}│ {Fore.LIGHTCYAN_EX}Website Information          {Fore.LIGHTWHITE_EX}│
    {Fore.LIGHTWHITE_EX}╚════╩──────────────────────────────┘
        """
    )
#endpoint

#region Main
try:
    while True:
        haw = Hawker()
        title()
        print(f'    {Fore.LIGHTWHITE_EX}┌─{Fore.LIGHTCYAN_EX}══{Fore.LIGHTWHITE_EX}──[{Fore.LIGHTCYAN_EX}HAWKER{Fore.LIGHTWHITE_EX}]')
        command = input(f'{Fore.LIGHTWHITE_EX}    └─────>  ')

        if command == "01" or command == "1":
            email = input(f'    {Fore.LIGHTCYAN_EX}Email{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            search_results = haw.doxbin_search(email)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
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
    ║                        Pastebin                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║   Result of Social Networking Sites Linked to Email  ║
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
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       WikiLeaks                      ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.wikileaks_search(email)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     Hudsonrock API                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_api(email)


            reddit_results = haw.reddit_search(email)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Reddit.com                     ║
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
        ║                     Snapchat.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(email)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Github.com                     ║
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
        ║                    Instagram.com                     ║
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
        ║                          X.com                       ║
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
        ║                      Youtube.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(email)
            if facebook_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      FaceBook.com                    ║
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
    ║                  Phone Information                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            if data:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number:", data.get('query'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Status:", data.get('status'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Type:", data.get('numberType'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid:", data.get('numberValid'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Number Valid for Region:", data.get('numberValidForRegion'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country Code:", data.get('numberCountryCode'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Area Code:", data.get('numberAreaCode'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} E.164 Format:", data.get('formatE164'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} National Format:", data.get('formatNational'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} International Format:", data.get('formatInternational'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Continent:", data.get('continent'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country:", data.get('countryName'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Region:", data.get('regionName'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} City:", data.get('city'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Latitude:", data.get('lat'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Longitude:", data.get('lon'))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Timezone:", data.get('timezone'))
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error retrieving data.")

            search_results = haw.doxbin_search(phone)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
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
    ║                        Pastebin                      ║
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
        ║                       Reddit.com                     ║
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
        ║                     Snapchat.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(phone)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Github.com                     ║
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
        ║                    Instagram.com                     ║
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
        ║                          X.com                       ║
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
        ║                      Youtube.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(phone)
            if facebook_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      FaceBook.com                    ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "03" or command == "3":
            fullname = input(f'    {Fore.LIGHTCYAN_EX}Full Name{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')

            white_results = haw.whitepages_search(fullname)
            if white_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     White Pages                      ║
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
    ║                      PageJaunes                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pagejaunes_results:
                    if 'pagesjaunes.fr' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                Google Dorking Files                  ║
        ╚══════════════════════════════════════════════════════╝
                '''
            )
            file_types = ["pdf", "xlsx", "docx", "txt", "xls", "doc", "ppt", "rft", "odt", "csv"]
            for file_type in file_types:
                search_results = haw.google_dorking_name(fullname, file_type)
        
                if search_results:
                    for link in search_results:
                        print(f"    {Fore.LIGHTGREEN_EX}[+] {Fore.LIGHTMAGENTA_EX} {file_type.upper()} {Fore.LIGHTWHITE_EX}{link}")


            search_results = haw.doxbin_search(fullname)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
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
    ║                        Pastebin                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            reddit_results = haw.reddit_search(fullname)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Reddit.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            snapchat_results = haw.snapchat_search(fullname)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                     Snapchat.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            github_results = haw.github_search(fullname)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Github.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(fullname)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                    Instagram.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(fullname)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                          X.com                       ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            youtube_results = haw.youtube_search(fullname)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      Youtube.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(fullname)
            if facebook_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      FaceBook.com                    ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "04" or command == "4":
            mac = input(f'    {Fore.LIGHTCYAN_EX}MAC Address{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTWHITE_EX} ')
            print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                    MAC Information                   ║
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
    ║                       DoxBin.org                     ║
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
    ║                        Pastebin                      ║
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
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            pastebin_results = haw.pastebin_search(ip)
            if pastebin_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                        Pastebin                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                    IP Information                    ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.geolocation_ip(ip)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     Hudsonrock API                   ║
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
    ║                  Bitcoin Information                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.get_bitcoin_info(bitcoin)


            search_results = haw.doxbin_search(bitcoin)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
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
    ║                        Pastebin                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in pastebin_results:
                    if 'pastebin.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "07" or command == "7":
            print(f'    Coming Soon, good luck with your investigation')
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
        elif command == "08" or command == "8":
            print(f'    Coming Soon, good luck with your investigation')
            input(f"    {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTWHITE_EX}>{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTWHITE_EX} Type 'enter' to continue. . .")
except Exception as e:
    print(f'{Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Program Failed: ', e) 
#endpoint

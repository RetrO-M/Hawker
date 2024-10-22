from colorama import Fore, init
from fake_useragent import UserAgent
import sys, os, requests, hashlib, re, random, ssl, socket
from urllib.parse import urlparse, urljoin, quote, urlencode
from bs4 import BeautifulSoup
from typing import List, Dict

init()

class log:
    wait = f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTCYAN_EX} * {Fore.LIGHTWHITE_EX}]"
    success = f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX} ✓ {Fore.LIGHTWHITE_EX}]"
    warning = f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX} ! {Fore.LIGHTWHITE_EX}]"
    error = f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX} X {Fore.LIGHTWHITE_EX}]"

def get_user_agent():
    ua = UserAgent()
    return ua.random

def domain_ex(url):
    domain = urlparse(url).netloc
    return domain

headers = {
    "Content-Type": "application/json",
    "User-Agent": get_user_agent(),
    "Accept-Language": random.choice(["en-US,en;q=0.9", "fr-FR,fr;q=0.9", "es-ES,es;q=0.9", "de-DE,de;q=0.9"]),
}

MALICIOUS_KEYWORDS = [
    'porno', 'porn', 'gore', 'viol', 'murder', 'blood', 'drugs', 'crime', 'violence',
    'suicide', 'hack', 'scam', 'malware', 'phishing', 'child abuse', 'exploit', 
    'torture', 'assassination', 'bullying', 'doxing', 'fraud', 'hacking', 
    'extortion', 'terrorism', 'ISIS', 'human trafficking', 'pedophile', 'abduction', 
    'black market', 'weapon', 'smuggling', 'arson', 'robbery', 'gang', 'hitman', 
    'assault', 'cyberbully', 'drug trafficking', 'weapon trafficking', 
    'death', 'decapitation', 'snuff', 'necrophilia', 'rape', 'stalking', 
    'incest', 'abuse', 'treat', 'exploitation', 'violence against women', 
    'violence against children', 'self-harm', 'self-injury', 'brutality', 
    'sadism', 'masochism', 'torturer', 'vandalism', 'corruption', 'slander', 
    'defamation', 'terrorist', 'discrimination', 'hate speech', 'radicalization', 
    'cult', 'militia', 'secession', 'sabotage', 'hostage', 'death threats', 
    'extremism', 'lynching', 'lynch mob', 'molestation', 'suffocation', 
    'homicide', 'kidnapping', 'cannibalism', 'clan', 'anarchy', 'destruction', 
    'hostility', 'oppression', 'insurgency', 'uprising', 'war crimes', 
    'crimes against humanity', 'genocide', 'ethnic cleansing', 'hate group', 
    'illegal', 'unlawful', 'felony', 'misconduct', 'wrongdoing', 'offense', 
    'trespass', 'conspiracy', 'perjury', 'embezzlement', 'money laundering', 
    'bribery', 'identity theft', 'financial fraud', 'cybercrime', 
    'dark web', 'deep web', 'scam site', 'phishing site', 'botnet', 
    'spam', 'spyware', 'trojan', 'ransomware', 'adware', 'keylogger', 
    'breach', 'leak', 'hacktivism', 'underground', 'piracy', 'crack', 
    'torrent', 'warez', 'zero-day', 'vulnerability', 'exploit kit', 
    'access', 'infiltrate', 'penetrate', 'malicious', 'trojan horse', 
    'rogue', 'payload', 'backdoor', 'vulnerability', 'exploit', 
    'social engineering', 'spear phishing', 'whaling', 'scareware', 
    'clickjacking', 'SQL injection', 'cross-site scripting', 'XSS', 
    'DNS spoofing', 'man-in-the-middle', 'DNS hijacking', 'session hijacking', 
    'IP spoofing', 'packet sniffing', 'credential stuffing', 'click fraud', 
    'ad fraud', 'affiliate fraud', 'traffic pumping', 'data mining', 
    'data breach', 'insider threat', 'sensitive data', 'confidential', 
    'classified', 'restricted', 'privacy violation', 'data protection', 
    'GDPR', 'CCPA', 'HIPAA', 'FERPA', 'identity', 'sensitive information', 
    'personal information', 'PPI', 'PII', 'social security', 'credit card', 
    'banking', 'financial', 'account', 'transaction', 'transfer', 
    'payment', 'debit', 'credit', 'currency', 'investment', 'stock', 
    'trading', 'broker', 'fraudulent', 'illicit', 'dangerous', 
    'hazardous', 'risk', 'threat', 'unethical', 'immoral', 'criminal', 
    'malice', 'wicked', 'evil', 'treachery', 'betrayal', 'treason', 
    'insider', 'covert', 'deception', 'con', 'fleece', 'scrounge', 
    'grift', 'graft', 'swindle', 'cheat', 'fraudster', 'scammer', 
    'con artist', 'criminal network', 'syndicate', 'mafia', 'cartel',
    'bestgore', 'sex', 'dox', 'X Videos', 'pornstar', 'dick', 'webcam girl',
    'cam girl', 'dark net', 'darknet', 'darkweb', 'dark web', 'deepweb', 'deep web',
    '4chan', 'ddos', 'kaotic', 'crazyshit', 'rotten', 'sex girl', 'gay', 'playboy', 'play boy', 'cannibal',
    'g0re', 'execution', 'drowing', 'funny death', 'live sex', 'fight', 'sextoys'
    'attack', 'killer', 'cam sex', 'XXX', 'cum', 'shock'
]

ports = [
    20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 6379, 8080, 554, 
    9050, 1521, 1433, 3389, 70, 1080, 68, 7, 88, 2049, 5900, 10000, 514, 69, 
    25565, 1723, 6667, 1352, 500, 79, 213, 23399, 4321, 513, 512, 135, 445
]

def check_adobe_email(email: str):
    data = {
        "username": email,
        "usernameType": "EMAIL"
    }
    try:
        r = requests.post("https://auth.services.adobe.com/signin/v2/users/accounts", headers=headers, json=data)
        response = r.json()

        if response and 'authenticationMethods' in response[0]:
            print(log.success + f" Adobe Account Found")
        else:
            print(log.error + f" No Adobe account")
    except Exception as e:
        pass

def check_chess_email(email):
    url = f"https://www.chess.com/callback/email/available?email={email}"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get('isEmailAvailable') == True:
            print(log.error + f" No Chess.com account") 
        elif data.get('isEmailAvailable') == False:
            print(log.success + f" Chess.com Account Found") 
        else:
            print(log.error + f" Chess.com account") 
    except:
        print(log.error + f" No Chess.com account")

def check_duolingo_email(target: str):
    url = "https://www.duolingo.com/2017-06-30/users"

    params = {
        'email': target
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            text_response = response.text

            if '{"users":[]}' in text_response:
                print(log.error + f" No Duolingo account")
            else:
                valid = response.json()['users'][0]['username']
                print(log.success + f" Duolingo Account Found")

    except Exception as e:
        pass

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

            response = requests.get(api_url, params=params, headers=headers)
            try:
                data = response.json()
                if 'user' in data:
                    print(log.success + f" https://www.flickr.com/people/{data['user']['nsid']}/")
                    flickr_found = True
                    break
            except:
                continue

    if not flickr_found:
        print(log.error + f" No Flickr account")

def check_github_email(email):
    url = f"https://api.github.com/search/users?q={email}+in:email"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result["total_count"] > 0:
                print(log.success + f" https://github.com/{result['items'][0]['login']}")
            else:
                print(log.error + f" No GitHub account")
    except Exception as e:
        pass

def check_gravatar_email(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://en.gravatar.com/{email_hash}.json"
    
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            display_name = data['entry'][0].get('displayName', 'Unknown')
            print(log.success + f" https://gravatar.com/{display_name}")
        elif response.status_code == 404:
            print(log.error + f" No Gravatar account")
    except Exception as e:
        pass

def check_pinterest_email(email):
    params = {
        "source_url": "/",
        "data": '{"options": {"email": "' + email + '"}, "context": {}}'
    }
    
    try:
        response = requests.get("https://www.pinterest.fr/resource/EmailExistsResource/get/", params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data["resource_response"]["data"]:
                print(log.success +f" Pinterest Account Found")
            else:
                print(log.error + f" No Pinterest account")
        else:
            print(log.error + f"No Pinterest account")

    except Exception as e:
        pass

def pornhub(target: str):
    try:
        with requests.Session() as session:
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
                print(log.error + f" No Pornhub account")
            elif response_json.get('email') == "create_account_failed":
                print(log.success + f" Pornhub Account Found")
            else:
                print(log.error + f"No Pornhub account")

    except Exception as e:
        pass

def check_spotify_email(target: str):
    url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
    
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            responseData = response.json()
            
            if responseData.get('status') == 20:
                print(log.success + f" Spotify Account Found")
            else:
                print(log.error + f" No Spotify account")
        else:
            print(log.error + f" No Spotify account")

    except Exception as e:
        pass

def check_twitter_email(email):
    url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data["valid"]:
                print(log.success + f" Twitter Account Found")
            else:
                print(log.error + f" No Twitter account")
    except requests.exceptions.JSONDecodeError:
        pass
    except Exception as e:
        pass

def wordpress_email(email):
    response = requests.get(f'https://public-api.wordpress.com/rest/v1.1/users/{email}/auth-options', headers=headers)

    if '"email_verified":true' in response.text:
        print(log.success + f' Wordpress Account Found')
    else:
        print(log.error + f' No Wordpress account')

def get_email_info(email):
    url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={email}"
    try:
        response = requests.get(url, headers=headers)
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

                print(log.success + f" Computer Name : ", computer_name)
                print(log.success + f" Operating System : ", operating_system)
                print(log.success + f" IP : ", ip)
                print(log.success + f" Malware Path : ", malware_path)
                print(log.success + f" Date Compromised : ", date_compromised)
                print(log.success + f" AntiViruses : ", antiviruses)
        else:
            print(log.error + " No data found...")

    except requests.RequestException as e:
        pass

def check_pastebin_dumps(email):
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{email}", headers=headers)
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                print(log.wait + f' PasteBin Dumps')
                for result in data:
                    print(log.success + f" https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(log.error + f" ERROR Json")

def check_http_methods(url):
    methods_to_check = [
        'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT', 'TRACE'
    ]
    
    print(log.wait + f" Checking HTTP methods for {url}:")
    for method in methods_to_check:
        try:
            response = requests.request(method, url, headers=headers)
            print(log.success + f" {method} : {response.status_code}")
        except requests.RequestException as e:
            print(log.error + f" {method} : {e}")

def check_email_website(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pattern = r'[\w\.-]+@[\w\.-]+'
            emails = set(re.findall(pattern, response.text))
            return list(emails)
        else:
            print(log.error + f" Error {response.status_code} Requests")
    except requests.exceptions.RequestException as e:
        print(log.error + f" ERROR: {e}")

def website_information(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        ip_address = socket.gethostbyname(domain)
        print(log.success + f" IP : {ip_address}")

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "None"
        print(log.success + f" Title : {title}")

        geo_request = requests.get(f"https://ipinfo.io/{ip_address}/json")
        geo_info = geo_request.json()
        
        city = geo_info.get("city", "None")
        region = geo_info.get("region", "None")
        country = geo_info.get("country", "None")
        location = geo_info.get("loc", "None")
        
        print(log.success + f" INFO : {city} | {region} | {country}")
        print(log.success + f" LOCATION : {location}")
        
    except Exception as e:
        pass

def website_information_usrs(url):
    domain = domain_ex(url)
    api_url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain?domain={domain}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        stealers_data = response.json().get('stealerFamilies', {})
        if stealers_data:
            redline = stealers_data.get('RedLine', 0)
            lumma = stealers_data.get('Lumma', 0)
            generic_stealer = stealers_data.get('Generic Stealer', 0)
            raccoon = stealers_data.get('Raccoon', 0)
            stealc = stealers_data.get('StealC', 0)
            vidar = stealers_data.get('Vidar', 0)
            azorult = stealers_data.get('Azorult', 0)
            unknown = stealers_data.get('UNKNOWN', 0)
            mystic = stealers_data.get('Mystic', 0)
            cryptbot = stealers_data.get('CRYPTBOT', 0)
            darkcrystal = stealers_data.get('DarkCrystal', 0)
            ficker = stealers_data.get('Ficker', 0)
            taurus = stealers_data.get('Taurus', 0)
            predator = stealers_data.get('Predator', 0)
            kpot = stealers_data.get('KPOT', 0)
            atomic = stealers_data.get('Atomic', 0)
            print(log.wait + f' Stealer Families')
            print(log.success + f" RedLine : {Fore.LIGHTGREEN_EX}{redline}")
            print(log.success + f" Lumma : {Fore.LIGHTGREEN_EX}{lumma}")
            print(log.success + f" Generic Stealer : {Fore.LIGHTGREEN_EX}{generic_stealer}")
            print(log.success + f" Raccoon : {Fore.LIGHTGREEN_EX}{raccoon}")
            print(log.success + f" StealC : {Fore.LIGHTGREEN_EX}{stealc}")
            print(log.success + f" Vidar : {Fore.LIGHTGREEN_EX}{vidar}")
            print(log.success + f" Azorult : {Fore.LIGHTGREEN_EX}{azorult}")
            print(log.success + f" UNKNOWN : {Fore.LIGHTGREEN_EX}{unknown}")
            print(log.success + f" Mystic : {Fore.LIGHTGREEN_EX}{mystic}")
            print(log.success + f" CRYPTBOT : {Fore.LIGHTGREEN_EX}{cryptbot}")
            print(log.success + f" DarkCrystal : {Fore.LIGHTGREEN_EX}{darkcrystal}")
            print(log.success + f" Ficker : {Fore.LIGHTGREEN_EX}{ficker}")
            print(log.success + f" Taurus : {Fore.LIGHTGREEN_EX}{taurus}")
            print(log.success + f" Predator : {Fore.LIGHTGREEN_EX}{predator}")
            print(log.success + f" KPOT : {Fore.LIGHTGREEN_EX}{kpot}")
            print(log.success + f" Atomic : {Fore.LIGHTGREEN_EX}{atomic}")
        else:
            print(log.error + f" No stealer data found...")
    
    except requests.RequestException as e:
        pass

def get_subdomains(domain):
    subdomains = [
        'www', 'mail', 'ads', 'admin', 'ftp', 'webmail', 
        'secure', 'login', 'api', 'dev', 'test', 'dashboard', 'contents', 'x', 'cdn', 'beta', 'fr', 'en',
        'search', 'videos', 'blog', 'cdn2', 'cdn1', "de", "es", "signup", "signin"
    ]
    
    found_subdomains = []

    for sub in subdomains:
        full_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            found_subdomains.append((full_domain, ip))
        except socket.gaierror:
            continue

    return found_subdomains

def get_ssl_info(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443

    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssl_info = ssock.getpeercert()

    return ssl_info

def get_http_headers(url):
    response = requests.get(url, headers=headers)
    return response.headers

def calculate_hash(data):
    return {
        'md5': hashlib.md5(data.encode()).hexdigest(),
        'sha1': hashlib.sha1(data.encode()).hexdigest(),
        'sha256': hashlib.sha256(data.encode()).hexdigest()
    }

def get_website_info(url):
    try:
        ssl_info = get_ssl_info(url)
        headers = get_http_headers(url)
        hash_info = calculate_hash(url)

        print(log.wait + f' SSL information:')
        for key, value in ssl_info.items():
            print(log.success + f' {key} :{Fore.LIGHTCYAN_EX} {value}')

        print(log.wait + f' HTTP headers:')
        for key, value in headers.items():
            print(log.success + f' {key} :{Fore.LIGHTCYAN_EX} {value}')

        print(log.wait + f' Hash URL:')
        for key, value in hash_info.items():
            print(log.success + f' {key} :{Fore.LIGHTCYAN_EX} {value}')

    except Exception as e:
        pass

def analyze_website(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
    except requests.RequestException as e:
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text()
    print(log.wait + f' Malicious keywords found :')
    for keyword in MALICIOUS_KEYWORDS:
        if keyword in content.lower():
            print(log.success + f' Found :{Fore.LIGHTGREEN_EX} {keyword}')

def website_pastebin_dumps(url):
    domain = domain_ex(url)
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{domain}", headers=headers)
    print(log.wait + f' PasteBin Dumps:')
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                for result in data:
                    print(log.success + f" {result.get('time')}{Fore.LIGHTYELLOW_EX} -{Fore.LIGHTCYAN_EX} https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(log.error + f" Error json")

def detect_os(host: str) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((host, 80)) 
            
            request = f'GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
            sock.sendall(request.encode('utf-8'))

            response = sock.recv(1024).decode('utf-8')

            if 'Ubuntu' in response:
                return 'Ubuntu'
            elif 'Debian' in response:
                return 'debian'
            elif 'Windows' in response:
                return 'windows'
            elif 'Apache' in response:
                return 'linux'
            elif 'nginx' in response:
                return 'linux'
            elif 'Python' in response:
                return 'python'
            elif 'Server' in response:
                return 'Unknown'
            else:
                return 'Unknown'

    except socket.error as e:
        return 'Unknown'

def geolocation_ip(ip):
    url = "https://ipinfo.io/"+ip+"/json"
    respon = requests.get(url, headers=headers)
    if respon.status_code == 200:
        result = respon.json()
        print(log.wait + f' IP Lookup : {ip}') 
        print(log.success + f" IP : ",result.get("ip"))
        print(log.success + f" Country : ",result.get("country"))
        print(log.success + f" City : ",result.get("city"))
        print(log.success + f" Location : ",result.get("loc"))
        print(log.success + f" Hostname : ",result.get("hostname"))

def get_info(ip):
    url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-ip?ip={ip}"
    try:
        response = requests.get(url, headers=headers)
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
                print(log.success + f" Computer Name : ", computer_name)
                print(log.success + f" Operating System : ", operating_system)
                print(log.success + f" IP : ", ip)
                print(log.success + f" Malware Path : ", malware_path)
                print(log.success + f" Date Compromised : ", date_compromised)
                print(log.success + f" AntiViruses : ", antiviruses)
        else:
            print(log.error + " No data found...")

    except requests.RequestException as e:
        pass

def ip_pastebin_dumps(ip):
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{ip}", headers=headers)
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                print(log.wait + f' PasteBin Dumps:')
                for result in data:
                    print(log.success + f" {result.get('time')}{Fore.LIGHTYELLOW_EX} -{Fore.LIGHTCYAN_EX} https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(log.error + f" Error json")

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False

def get_service_name(port: int) -> str:
    services = {
        20: 'ftp-data',
        21: 'ftp',
        22: 'ssh',
        23: 'telnet',
        25: 'smtp',
        53: 'dns',
        80: 'http',
        110: 'pop3',
        143: 'imap',
        443: 'https',
        3306: 'mysql',
        5432: 'postgres',
        6379: 'redis',
        8080: 'http-proxy',
        554: 'rtsp',
        9050: 'tor-socks',
        1521: "oracle Database",
        1433: "microsoft-sql-server",
        5432: "postgre-sql",
        3389: "rdp",
        70: "gopher",
        1080: "socks5",
        110: "POP3",
        68: "dhcp",
        7: "echo",
        88: "kerberos",
        2049: "nfs",
        5900: "vnc",
        10000: "webdmin",
        514: "syslog",
        69: "tftp",
        25565: "minecraft-server",
        1433: "ms-sql",
        1723: "vpn-pptp",
        6667: "irc",
        1352: "lnd",
        500: "ipsec",
        79: "finger",
        213: "ipx",
        514: "shell",
        23399: "skype",
        4321: "rwhois",
        513: "login",
        512: "exec",
        135: "epmap",
        445: "microsoft-ds"
    }
    return services.get(port, 'unknown')

def get_open_ports(host: str, ports: List[int]) -> Dict[int, str]:
    open_ports = {}
    for port in ports:
        if scan_port(host, port):
            service = get_service_name(port)
            open_ports[port] = service
    return open_ports


def print_ports_summary(host: str, ports: List[int]):
    open_ports = get_open_ports(host, ports)
    if open_ports:
        print(f" {'PORT':<10} {'STATE':<6} {'SERVICE':<10}")
        print("═" * 27)
        for port, service in open_ports.items():
            print(log.success + f" {port}/tcp  open  {service}")
    else:
        print(log.error + f" No open ports found on {host}.")

def google_dorking_phone(phone, file_type):
    query = f"{phone} filetype:{file_type}"
    url = "https://www.google.com/search?"
    params = {
        'q': query,
        'hl': 'en', 
        'num': 10    
    }

    url_with_params = url + urlencode(params)
    
    try:
        response = requests.get(url_with_params, headers=headers)
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
    
    except requests.RequestException as e:
        return None

def google_dorking_scan(phone, file_type):
    query = f"{phone} filetype:{file_type}"
    url = "https://www.google.com/search?"
    params = {
        'q': query,
        'hl': 'en', 
        'num': 10    
    }

    url_with_params = url + urlencode(params)
    
    try:
        response = requests.get(url_with_params, headers=headers)
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
    
    except requests.RequestException as e:
        return None

def search_bing(phone_number):
    encoded_query = quote(f"{phone_number} site:facebook.com")
    search_url = f"https://www.bing.com/search?q={encoded_query}"

    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"{Fore.RED}STATUS : {response.status_code}")
        return None

def parse_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    for g in soup.find_all('li', class_='b_algo'):
        title = g.find('h2')
        link = g.find('a', href=True)

        if title and link:
            actual_link = link['href']
            results.append((title.text, actual_link))

    return results

def twitter_scan(phone_number):
    encoded_query = quote(f"{phone_number} site:twitter.com")
    search_url = f"https://www.bing.com/search?q={encoded_query}"

    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"{Fore.RED}STATUS : {response.status_code}")
        return None

def parse_results2(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    for g in soup.find_all('li', class_='b_algo'):
        title = g.find('h2')
        link = g.find('a', href=True)

        if title and link:
            actual_link = link['href']
            results.append((title.text, actual_link))

    return results

def linkedin_scan(phone_number):
    encoded_query = quote(f"{phone_number} site:linkedin.com")
    search_url = f"https://www.bing.com/search?q={encoded_query}"

    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"{Fore.RED}STATUS : {response.status_code}")
        return None

def parse_results3(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    for g in soup.find_all('li', class_='b_algo'):
        title = g.find('h2')
        link = g.find('a', href=True)

        if title and link:
            actual_link = link['href']
            results.append((title.text, actual_link))

    return results

def title():
    os.system("cls || clear")
    sys.stdout.write(f'''{Fore.LIGHTWHITE_EX}
         <` ─ .          .-─^">
        ^       \     /         ^
       |         r    L         |
      └;¬.      /      ,     .⌐;7
           ~`\╗{Fore.LIGHTCYAN_EX}▒^τ╔╦╗╥r){Fore.LIGHTWHITE_EX}%≤`.─`
{Fore.LIGHTWHITE_EX} █▌      █▌{Fore.LIGHTCYAN_EX}  ╣▓╣▒▓▓▓▓▓▒╢▓▓k  {Fore.LIGHTWHITE_EX} █C     █▄     █▌ ▐█    ██  ▐█▀▀▀▀▀▀▀   ▐█▀▀▀▀█▄,
{Fore.LIGHTWHITE_EX} █▌      █▌{Fore.LIGHTCYAN_EX} ╫▓▓▓▒▓▓█▓▓▓▒▓▓╣L{Fore.LIGHTWHITE_EX}  ██    █▀█⌐   ▐█  ▐█  ▄█▀   ▐█          ▐█      █▄
 {Fore.LIGHTWHITE_EX}█▌      █▌ {Fore.LIGHTCYAN_EX} ╙╣▒▒╫▓▓▓▓▒╜▒╚" {Fore.LIGHTWHITE_EX}   █⌐  ██ ▐█   █▌  ▐█,█▀     ▐█          ▐█     ,█C
 {Fore.LIGHTWHITE_EX}██▀▀▀▀▀▀█▌  {Fore.LIGHTCYAN_EX}  ("░╫▓▓╣╜'"     {Fore.LIGHTWHITE_EX} ██ ▄█   ▀█ ▐█   ▐███      ▐█▀▀▀▀▀▀▀   ▐█▄▄▄██▀"
 {Fore.LIGHTWHITE_EX}█▌      █▌  {Fore.LIGHTCYAN_EX}    ╘▒╬▒░ ╛      {Fore.LIGHTWHITE_EX}  █▄█     ███▌   ▐█ ╙█▄    ▐█          ▐█  ▀█▄
{Fore.LIGHTWHITE_EX} █▌      █▌ {Fore.LIGHTCYAN_EX}      r░░L/         {Fore.LIGHTWHITE_EX}██"      ██    ▐█   ▀█,  ▐█          ▐█    ██
 {Fore.LIGHTWHITE_EX}▀┘      ▀▀ {Fore.LIGHTCYAN_EX}       \/          {Fore.LIGHTWHITE_EX} └▀        ▌    '▀    "▀^ "▀▀▀▀▀▀▀▀   ╙▀     ╙▀^

''')

title()
choice = input(f'{Fore.LIGHTCYAN_EX}HAWKER {Fore.LIGHTWHITE_EX}> ')

try:
    if '@' in choice:
        print(log.wait + ' Result of Social Networking Sites Linked to Email')
        check_github_email(choice)
        pornhub(choice)
        check_spotify_email(choice)
        check_twitter_email(choice)
        check_flickr_email(choice)
        check_chess_email(choice)
        check_adobe_email(choice)
        check_duolingo_email(choice)
        check_gravatar_email(choice)
        check_pinterest_email(choice)
        wordpress_email(choice)
        print()
        print(log.wait + f' Hudsonrock API')
        get_email_info(choice)
        print()
        check_pastebin_dumps(choice)
    elif choice.startswith('http://') or choice.startswith('https://'):
        url = choice
        emails = check_email_website(url)
        if emails:
            print(log.wait + f" Email addresses found on {url}:")
            for email in emails:
                print(log.success + f' Found : {email}')
        else:
            print(log.error + f" No email address found on : {url}.")
        check_http_methods(url)
        print(log.wait + f" Website Information : {url}:")
        website_information(url)
        website_information_usrs(url)
        domain = domain_ex(url)
        subdomains_with_ips = get_subdomains(domain)
        if subdomains_with_ips:
            print(log.wait + f" Subdomains and IP addresses for {domain}:")
            for subdomain, ip in subdomains_with_ips:
                os_name = detect_os(ip)
                print(f"      {Fore.LIGHTCYAN_EX}{subdomain}{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} {ip}{Fore.LIGHTWHITE_EX} -{Fore.LIGHTYELLOW_EX} {os_name}")
                ip_url = f'http://{ip}'
                resp = requests.get(ip_url, headers=headers)
                print(f'      {log.success} {ip_url} --> {Fore.LIGHTGREEN_EX} ', resp.status_code)
        else:
            print(log.error + f" No subdomains found for {domain}.")
        get_website_info(url)
        analyze_website(url) 
        website_pastebin_dumps(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            input_fields = soup.find_all('input')
            for field in input_fields:
                field_type = field.get('type')
                field_name = field.get('name')
                field_id = field.get('id')
                field_placeholder = field.get('placeholder')
                print(log.success + f" Type: {Fore.LIGHTGREEN_EX}{field_type}     {Fore.YELLOW}►{Fore.LIGHTWHITE_EX}     Name: {Fore.LIGHTGREEN_EX}{field_name}{Fore.LIGHTWHITE_EX}     {Fore.YELLOW}►{Fore.LIGHTWHITE_EX}     ID: {Fore.LIGHTGREEN_EX}{field_id}{Fore.LIGHTWHITE_EX}     {Fore.YELLOW}►{Fore.LIGHTWHITE_EX}     Placeholder: {Fore.LIGHTGREEN_EX}{field_placeholder}{Fore.LIGHTWHITE_EX}")
        else:
            print(log.error + f" Failed to retrieve the page. Status code : {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a') 
            for link in links:
                    href = link.get('href')
                    if href and not href.endswith('/'):
                        print(log.success + f' URL : FILE --> {href}')
                    else:
                        print(log.error + f' URL : FILE --> {href}')
    elif '.' in choice:
        ip = choice
        geolocation_ip(ip)
        get_info(ip)
        ip_pastebin_dumps(ip)
        print_ports_summary(ip, ports)
    elif '+' in choice:
        phone = choice
        file_types = ["pdf", "xlsx", "docx", "txt", "xls", "doc", "ppt", "rft"]
        print(log.wait + f' Google Dorking:')
        for file_type in file_types:
            search_results = google_dorking_phone(phone, file_type)
            if search_results:
                for link in search_results:
                    print(log.success + f" {file_type.upper()} :{Fore.LIGHTGREEN_EX}  {link}")
            else:
                print(log.error + f' Not Found')
        html_content = search_bing(phone)
        if html_content:
            results = parse_results(html_content)
            print(log.wait + f" Facebook search results :")
            for title, link in results:
                print(log.success + f" Title:{Fore.LIGHTRED_EX} {title}{Fore.LIGHTWHITE_EX} - Link:{Fore.LIGHTCYAN_EX} {link}")
        html_content2 = twitter_scan(phone)
        if html_content2:
            results = parse_results(html_content2)

            print(log.wait + f" Twitter search results :")
            for title, link in results:
                print(log.success + f" Title:{Fore.LIGHTRED_EX} {title}{Fore.LIGHTWHITE_EX} - Link:{Fore.LIGHTCYAN_EX} {link}")
        html_content3 = linkedin_scan(phone)
        if html_content3:
            results = parse_results(html_content3)

            print(log.wait + f" Linkedin search results :")
            for title, link in results:
                print(log.success + f" Title:{Fore.LIGHTRED_EX} {title}{Fore.LIGHTWHITE_EX} - Link:{Fore.LIGHTCYAN_EX} {link}")
    else:
        print(log.error + " Try again, Please enter an email address or URL")
except Exception as e:
    print(log.error + f" An error occurred: {str(e)}")
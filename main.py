from src.github import check_github_email 
from src.pornhub import pornhub 
from src.spotify import check_spotify_email  
from src.twitter import check_twitter_email 
from src.flickr import check_flickr_email 
from src.chess import check_chess_email 
from src.adobe import check_adobe_email 
from src.duolingo import check_duolingo_email 
from src.gravatar import check_gravatar_email 
from src.pinterest import check_pinterest_email

import re, time, requests, json, socket, ssl, hashlib
from colorama import Fore, init
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote
import phonenumbers
from phonenumbers import geocoder, PhoneNumberFormat, number_type, timezone
from urllib.parse import urlencode, urljoin
from fake_useragent import UserAgent

ua = UserAgent()
useragent = ua.random


def domain_ex(url):
    domain = urlparse(url).netloc
    return domain


init()

print(
    f"""
      {Fore.BLUE}█ █{Fore.LIGHTWHITE_EX} ▄▀█ █ █ █ █▄▀ █▀▀ █▀█
      {Fore.BLUE}█▀█{Fore.LIGHTWHITE_EX} █▀█ ▀▄▀▄▀ █ █ ██▄ █▀▄
     {Fore.LIGHTBLACK_EX} Educational Purposes Only.
          {Fore.LIGHTCYAN_EX}~ by d3m3t0r
    """
)


def get_company_info(email):
    url = f"https://portal.spycloud.com/endpoint/enriched-stats/{email}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        
        data = response.json()

        company_info = data.get('company', {})
        name = company_info.get('name', '/')

        print(f"          {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Company :", name)
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
        if re.match(email_regex, email):
            print(f"          {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Valid email format : {email}")
        else:
            print(f"          {Fore.RED}[-]{Fore.LIGHTWHITE_EX} Invalid email format : {email}")


    except requests.RequestException as e:
        pass

def emailrep(email):
    try:
        r = requests.get(f'https://emailrep.io/{email}')
        r.raise_for_status() 

        data = r.json()
        details = data.get('details', {})

        disposable = details.get('disposable', False)
        data_breach = details.get('data_breach', False)
        spam = details.get('spam', False)
        spoofable = details.get('spoofable', False)

        disposable_status = "Email Disposable" if disposable else "No Disposable Email"
        data_breach_status = "Leaks online found" if data_breach else "No leaks found"
        spam_status = "Spam reputation found" if spam else "No Spam reputation"
        spoofable_status = "Spoofable" if spoofable else "No Spoofable"

        print(f"          {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Disposable : {disposable_status}")
        print(f"          {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Data Breach : {data_breach_status}")
        print(f"          {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Spam reputation : {spam_status}")
        print(f"          {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Spoofable : {spoofable_status}\n")

    except requests.exceptions.RequestException as e:
        print(f"          {Fore.RED}[-]{Fore.LIGHTWHITE_EX} Error with the EmailRep API request: {e}")
    except json.JSONDecodeError:
        print(f"          {Fore.RED}[-]{Fore.LIGHTWHITE_EX} Error decoding the JSON response.")
    except KeyError as e:
        print(f"          {Fore.RED}[-]{Fore.LIGHTWHITE_EX} KeyError: Missing expected key in the response: {e}")

def check_pastebin_dumps(email):
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{email}")
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                print(f'{Fore.LIGHTCYAN_EX}[~]{Fore.LIGHTWHITE_EX} PasteBin Dumps')
                for result in data:
                    print(f"    {Fore.LIGHTMAGENTA_EX}[-]{Fore.LIGHTWHITE_EX} https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(f"    {Fore.RED}[-]{Fore.LIGHTWHITE_EX}ERROR Json")
    else:
        print(f"    {Fore.RED}[-]{Fore.LIGHTWHITE_EX}Error : {resp.status_code}")


def get_email_info(email):
    url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={email}"
    try:
        response = requests.get(url)
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

                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Computer Name{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", computer_name)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Operating System{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", operating_system)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}IP{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", ip)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Malware Path{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", malware_path)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Date Compromised{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", date_compromised)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}AntiViruses{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", antiviruses)
        else:
            print("No data found...")

    except requests.RequestException as e:
        pass


def osint_email_tool(email):
    print(f'{Fore.LIGHTBLACK_EX}[!]{Fore.LIGHTWHITE_EX} Lets go find some information!')
    time.sleep(0.6)
    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Email Information')
    get_company_info(email)
    emailrep(email)
    print(f'{Fore.YELLOW}[!]{Fore.LIGHTWHITE_EX} Site results')
    check_github_email(email)
    pornhub(email)
    check_spotify_email(email)
    check_twitter_email(email)
    check_flickr_email(email)
    check_chess_email(email)
    check_adobe_email(email)
    check_duolingo_email(email)
    check_gravatar_email(email)
    check_pinterest_email(email)
    check_pastebin_dumps(email)
    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Hudsonrock')
    get_email_info(email)

















################################################################################################################################################















def check_http_methods(url):
    methods_to_check = [
        'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT', 'TRACE'
    ]
    
    print(f"{Fore.LIGHTCYAN_EX}[/]{Fore.LIGHTWHITE_EX} Checking HTTP methods for {url}:")
    for method in methods_to_check:
        try:
            response = requests.request(method, url)
            print(f"     {Fore.LIGHTGREEN_EX} [-]{Fore.LIGHTWHITE_EX} {method} : {response.status_code}")
        except requests.RequestException as e:
            print(f"     {Fore.RED} [-]{Fore.LIGHTWHITE_EX} {method} : {e}")

def check_email_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pattern = r'[\w\.-]+@[\w\.-]+'
            emails = set(re.findall(pattern, response.text))
            return list(emails)
        else:
            print(f"     {Fore.RED} [-]{Fore.LIGHTWHITE_EX} Error {response.status_code} Requests")
    except requests.exceptions.RequestException as e:
        print(f"     {Fore.RED} [-]{Fore.LIGHTWHITE_EX} ERROR: {e}")


def website_information(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        ip_address = socket.gethostbyname(domain)
        print(f"      {Fore.LIGHTCYAN_EX}[+]{Fore.LIGHTWHITE_EX} IP : {ip_address}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "None"
        print(f"      {Fore.LIGHTCYAN_EX}[+]{Fore.LIGHTWHITE_EX} Title : {title}")

        geo_request = requests.get(f"https://ipinfo.io/{ip_address}/json")
        geo_info = geo_request.json()
        
        city = geo_info.get("city", "None")
        region = geo_info.get("region", "None")
        country = geo_info.get("country", "None")
        location = geo_info.get("loc", "None")
        
        print(f"      {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} INFO :{Fore.LIGHTMAGENTA_EX} {city} - {region} - {country}")
        print(f"      {Fore.LIGHTCYAN_EX}[+]{Fore.LIGHTWHITE_EX} LOCATION : {location}")
        
    except Exception as e:
        pass

def website_information_usrs(url):
    domain = domain_ex(url)
    api_url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain?domain={domain}"
    
    try:
        response = requests.get(api_url)
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
            print(f'{Fore.LIGHTCYAN_EX}[/]{Fore.LIGHTWHITE_EX} Stealer Families')
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}RedLine{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{redline}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Lumma{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{lumma}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Generic Stealer{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{generic_stealer}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Raccoon{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{raccoon}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}StealC{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{stealc}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Vidar{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{vidar}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Azorult{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{azorult}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}UNKNOWN{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{unknown}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Mystic{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{mystic}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}CRYPTBOT{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{cryptbot}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}DarkCrystal{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{darkcrystal}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Ficker{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{ficker}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Taurus{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{taurus}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Predator{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{predator}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}KPOT{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{kpot}")
            print(f"    {Fore.RED}[{Fore.LIGHTCYAN_EX}Atomic{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}{atomic}")
        else:
            print(f"{Fore.RED}No stealer data found...")
    
    except requests.RequestException as e:
        pass


def get_subdomains(domain):
    subdomains = [
        'www', 'mail', 'ads', 'admin', 'ftp', 'webmail', 
        'secure', 'login', 'api', 'dev', 'test', 'dashboard', 'contents', 'x', 'cdn', 'beta', 'fr', 'en',
        'search', 'videos', 'blog', 'cdn2', 'cdn1'
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
    response = requests.get(url)
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

        print(f'{Fore.LIGHTMAGENTA_EX}[+]{Fore.LIGHTWHITE_EX} SSL information:')
        for key, value in ssl_info.items():
            print(f'     {Fore.LIGHTYELLOW_EX}{key} {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} {value}')

        print(f'{Fore.LIGHTCYAN_EX}[+]{Fore.LIGHTWHITE_EX} HTTP headers:')
        for key, value in headers.items():
            print(f'     {Fore.LIGHTYELLOW_EX}{key} {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} {value}')

        print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Hash URL:')
        for key, value in hash_info.items():
            print(f'     {Fore.LIGHTYELLOW_EX}{key} {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} {value}')

    except Exception as e:
        pass

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
    'cam girl', 'dark net', 'darknet', 'darkweb', 'dark web', 'deepweb', 'deep web', 'Islamic state',
    '4chan', 'ddos', 'kaotic', 'crazyshit', 'rotten', 'sex girl', 'gay', 'playboy', 'play boy', 'cannibal',
    'g0re', 'execution', 'drowing', 'funny death', 'live sex', 'fight'
]

def analyze_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.RequestException as e:
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text()
    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Malicious keywords found :')
    for keyword in MALICIOUS_KEYWORDS:
        if keyword in content.lower():
            print(f'      {Fore.LIGHTCYAN_EX}[-]{Fore.LIGHTWHITE_EX} Found :{Fore.LIGHTGREEN_EX} {keyword}')


def get_resolved_ip(url):
    domain = domain_ex(url)
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_external_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except requests.exceptions.RequestException as req_err:
        return None

def check_dns_leak(url):
    domain = domain_ex(url)
    resolved_ip = get_resolved_ip(url)
    external_ip = get_external_ip()
    
    if resolved_ip is None or external_ip is None:
        return
    print(f'{Fore.LIGHTYELLOW_EX}[*]{Fore.LIGHTRED_EX} DNS Leak:')
    print(f"     {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} URL : {domain}")
    print(f"     {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} Resolved IP address: {resolved_ip}")
    print(f"     {Fore.LIGHTGREEN_EX}[-]{Fore.LIGHTWHITE_EX} External IP address: {external_ip}")



def website_pastebin_dumps(url):
    domain = domain_ex(url)
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{domain}")
    print(f'{Fore.LIGHTYELLOW_EX}[~]{Fore.LIGHTWHITE_EX} PasteBin Dumps:')
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                for result in data:
                    print(f"               {Fore.LIGHTMAGENTA_EX}{result.get('time')}{Fore.LIGHTYELLOW_EX} -{Fore.LIGHTGREEN_EX} https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(f"{Fore.RED}                Error json")
    else:
        print(f"{Fore.RED}               Error : {resp.status_code}")


def check_paths(base_url, wordlist_file):
    with open(wordlist_file, 'r') as f:
        paths_to_check = [line.strip() for line in f.readlines() if line.strip()]
    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Login Page:')
    for path in paths_to_check:
        url = urljoin(base_url, path)
        time.sleep(0.5)
        response = requests.get(url)
        if response.status_code == 200:
            print(f"                     {Fore.LIGHTWHITE_EX} /{Fore.LIGHTGREEN_EX}{path}{Fore.LIGHTRED_EX} (Status :{Fore.LIGHTCYAN_EX} {response.status_code}{Fore.LIGHTRED_EX})")



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

def osint_website_tool(url):
    emails = check_email_website(url)
    if emails:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Email addresses found on {url}:")
        for email in emails:
            print(f'{Fore.LIGHTGREEN_EX}    [-]{Fore.LIGHTWHITE_EX} Found : {email}')
    else:
        print(f"{Fore.RED}    [-]{Fore.LIGHTWHITE_EX} No email address found on : {url}.")


    check_http_methods(url)
    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Website Information : {url}:")
    website_information(url)
    website_information_usrs(url)

    domain = domain_ex(url)
    subdomains_with_ips = get_subdomains(domain)


    if subdomains_with_ips:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Subdomains and IP addresses for {domain}:")
        for subdomain, ip in subdomains_with_ips:
            os_name = detect_os(ip)
            print(f"      {Fore.LIGHTCYAN_EX}{subdomain}{Fore.LIGHTWHITE_EX} -{Fore.LIGHTGREEN_EX} {ip}{Fore.LIGHTWHITE_EX} -{Fore.LIGHTYELLOW_EX} {os_name}")
    else:
        print(f"{Fore.RED}No subdomains found for {domain}.")
    get_website_info(url)
    analyze_website(url)
    check_dns_leak(url)
    website_pastebin_dumps(url)
    wordlist_file = 'wordlist/list.txt'
    check_paths(url, wordlist_file)







################################################################################################################################################








def geolocation_ip(ip):
    url = "https://ipinfo.io/"+ip+"/json"
    respon = requests.get(url)
    if respon.status_code == 200:
        result = respon.json()
        print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP Lookup : {ip}') 
        print(f"    {Fore.RED}[{Fore.LIGHTGREEN_EX}IP{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("ip"))
        print(f"    {Fore.RED}[{Fore.LIGHTGREEN_EX}Country{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("country"))
        print(f"    {Fore.RED}[{Fore.LIGHTGREEN_EX}City{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("city"))
        print(f"    {Fore.RED}[{Fore.LIGHTGREEN_EX}Location{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("loc"))
        print(f"    {Fore.RED}[{Fore.LIGHTGREEN_EX}Hostname{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("hostname"))

def get_info(ip):
    url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-ip?ip={ip}"
    try:
        response = requests.get(url)
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
                print(f'{Fore.LIGHTCYAN_EX}[/]{Fore.LIGHTWHITE_EX} Hudsonrock IP : {ip}') 
                print(f"      {Fore.RED}[{Fore.LIGHTCYAN_EX}Computer Name{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", computer_name)
                print(f"      {Fore.RED}[{Fore.LIGHTCYAN_EX}Operating System{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", operating_system)
                print(f"      {Fore.RED}[{Fore.LIGHTCYAN_EX}IP{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", ip)
                print(f"      {Fore.RED}[{Fore.LIGHTCYAN_EX}Malware Path{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", malware_path)
                print(f"      {Fore.RED}[{Fore.LIGHTCYAN_EX}Date Compromised{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", date_compromised)
                print(f"      {Fore.RED}[{Fore.LIGHTCYAN_EX}AntiViruses{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", antiviruses)
        else:
            print("No data found...")

    except requests.RequestException as e:
        pass


def ip_pastebin_dumps(ip):
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{ip}")
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                print(f'{Fore.LIGHTYELLOW_EX}[~]{Fore.LIGHTWHITE_EX} PasteBin Dumps:')
                for result in data:
                    print(f"               {Fore.LIGHTMAGENTA_EX}{result.get('time')}{Fore.LIGHTYELLOW_EX} -{Fore.LIGHTGREEN_EX} https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(f"{Fore.RED}                Error json")
    else:
        print(f"{Fore.RED}               Error : {resp.status_code}")

def osint_ip_tool(ip):
    geolocation_ip(ip)
    get_info(ip)
    ip_pastebin_dumps(ip)










################################################################################################################################################







def phone_pastebin_dumps(phone):
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{phone}")
    if resp.status_code == 200:
        try:
            data = resp.json()  

            if isinstance(data, list) and len(data) == 0:
                print(f"")
            else:
                print(f'{Fore.LIGHTYELLOW_EX}[~]{Fore.LIGHTWHITE_EX} PasteBin Dumps:')
                for result in data:
                    print(f"               {Fore.LIGHTMAGENTA_EX}{result.get('time')}{Fore.LIGHTYELLOW_EX} -{Fore.LIGHTGREEN_EX} https://pastebin.com/{result.get('id')}")

        except ValueError:
            print(f"{Fore.RED}                Error json")
    else:
        print(f"{Fore.RED}               Error : {resp.status_code}")


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
        headers = {
            'User-Agent': useragent
        }
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
        headers = {
            'User-Agent': useragent
        }
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
    



def get_user_agent():
    ua = UserAgent()
    return ua.random

def search_bing(phone_number):
    encoded_query = quote(f"{phone_number} site:facebook.com")
    search_url = f"https://www.bing.com/search?q={encoded_query}"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

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
    headers = {
        'User-Agent': get_user_agent(),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

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
    headers = {
        'User-Agent': get_user_agent(),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

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


def osint_phone_tool(phone):
    print(f'{Fore.LIGHTYELLOW_EX}/!\{Fore.LIGHTRED_EX} Im really sorry but to get information on the telephone number you have to do this 123-456-7890 {Fore.LIGHTYELLOW_EX}/!\\')
    formatted_num = "+1" + phone.replace("-", "")
    phone_number = phonenumbers.parse(formatted_num)

    if phonenumbers.is_valid_number(phone_number):
        region = geocoder.description_for_number(phone_number, "en")
        international_format = phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(phone_number, PhoneNumberFormat.NATIONAL)
        num_type = number_type(phone_number)
        time_zones = timezone.time_zones_for_number(phone_number)

        type_mapping = {
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
        }

        type_description = type_mapping.get(num_type, "Unknown")
        print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Phone Information:')
        print(f"         {Fore.LIGHTCYAN_EX}[*]{Fore.LIGHTWHITE_EX} Number:{Fore.LIGHTYELLOW_EX} {phone}")
        print(f"         {Fore.LIGHTCYAN_EX}[*]{Fore.LIGHTWHITE_EX} International Format:{Fore.LIGHTYELLOW_EX} {international_format}")
        print(f"         {Fore.LIGHTCYAN_EX}[*]{Fore.LIGHTWHITE_EX} National Format:{Fore.LIGHTYELLOW_EX} {national_format}")
        print(f"         {Fore.LIGHTCYAN_EX}[*]{Fore.LIGHTWHITE_EX} Region:{Fore.LIGHTYELLOW_EX} {region}")
        print(f"         {Fore.LIGHTCYAN_EX}[*]{Fore.LIGHTWHITE_EX} Number Type:{Fore.LIGHTYELLOW_EX} {type_description}")
        print(f"         {Fore.LIGHTCYAN_EX}[*]{Fore.LIGHTWHITE_EX} TimeZones:{Fore.LIGHTYELLOW_EX} {', '.join(time_zones)}")
    else:
        print(f"         {Fore.RED}The number is not valid.")
    
    phone_pastebin_dumps(phone)

    file_types = ["pdf", "xlsx", "docx", "txt", "xls", "doc", "ppt", "rft"]
    print(f'{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Google Dorking:')
    for file_type in file_types:
        search_results = google_dorking_phone(phone, file_type)
    
        if search_results:
            for link in search_results:
                print(f"             {Fore.LIGHTCYAN_EX}[+]{Fore.LIGHTYELLOW_EX} {file_type.upper()} :{Fore.LIGHTGREEN_EX}  {link}")
        else:
            print(f'{Fore.RED}             Not Found')

    html_content = search_bing(phone)

    if html_content:
        results = parse_results(html_content)

        print(f"{Fore.LIGHTCYAN_EX}[/]{Fore.LIGHTWHITE_EX} Facebook search results :")
        for title, link in results:
            print(f"   {Fore.LIGHTYELLOW_EX}[-]{Fore.LIGHTWHITE_EX} Title:{Fore.LIGHTRED_EX} {title}{Fore.LIGHTWHITE_EX} - Link:{Fore.LIGHTCYAN_EX} {link}")


    html_content2 = twitter_scan(phone)

    if html_content2:
        results = parse_results(html_content2)

        print(f"{Fore.LIGHTCYAN_EX}[/]{Fore.LIGHTWHITE_EX} Twitter search results :")
        for title, link in results:
            print(f"   {Fore.LIGHTYELLOW_EX}[-]{Fore.LIGHTWHITE_EX} Title:{Fore.LIGHTRED_EX} {title}{Fore.LIGHTWHITE_EX} - Link:{Fore.LIGHTCYAN_EX} {link}")

    html_content3 = linkedin_scan(phone)

    if html_content3:
        results = parse_results(html_content3)

        print(f"{Fore.LIGHTCYAN_EX}[/]{Fore.LIGHTWHITE_EX} Linkedin search results :")
        for title, link in results:
            print(f"   {Fore.LIGHTYELLOW_EX}[-]{Fore.LIGHTWHITE_EX} Title:{Fore.LIGHTRED_EX} {title}{Fore.LIGHTWHITE_EX} - Link:{Fore.LIGHTCYAN_EX} {link}")




def main():
    choice = input(f'{Fore.LIGHTMAGENTA_EX}TARGET:{Fore.LIGHTWHITE_EX} ')
    
    if '@' in choice:
        osint_email_tool(choice)
    elif choice.startswith('http://') or choice.startswith('https://'):
        osint_website_tool(choice)
    elif '.' in choice:
        osint_ip_tool(choice)
    elif '-' in choice:
        osint_phone_tool(choice)
    else:
        print(f"{Fore.LIGHTRED_EX}[!] Try again, Please enter an email address or URL")


main()
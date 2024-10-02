import requests
from bs4 import BeautifulSoup
import urllib.parse
from fake_useragent import UserAgent
from colorama import Fore, init

init()

ua = UserAgent()
useragent = ua.random

def google_dork_search(phone_number, num_results=10):

    query = f'"{phone_number}"'
    search_url = f'https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results}'

    headers = {
        'User-Agent': useragent
    }

    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"{Fore.RED}ERROR : {response.status_code}")
        return None

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for item in soup.find_all('div', class_='g'):
        title = item.find('h3')
        link = item.find('a')['href']
        snippet = item.find('span', class_='aCOpRe')
        
        if title and link:
            results.append({
                'title': title.get_text(),
                'link': link,
                'snippet': snippet.get_text() if snippet else ''
            })
    
    return results
from urllib.parse import urlencode, urljoin
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
useragent = ua.random


def google_dorking_email(email, file_type):
    query = f"{email} filetype:{file_type}"
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

def google_dorking_scan(email, file_type):
    query = f"{email} filetype:{file_type}"
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
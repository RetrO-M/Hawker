import asyncio, time, requests, random
from colorama import Fore, init
from os import system, name
import concurrent.futures  
from collections import OrderedDict 
import asyncio
import sys

def clear(): 
    if name == 'nt': 
        system('cls')
    else: 
        system('clear')

init()

WEBSITES = OrderedDict([
    ("Instagram", "https://www.instagram.com/{}"),
    ("Facebook", "https://www.facebook.com/{}"),
    ("YouTube", "https://www.youtube.com/@{}"),
    ("Reddit", "https://www.reddit.com/user/{}"),
    ("GitHub", "https://github.com/{}"),
    ("Twitch", "https://www.twitch.tv/{}"),
    ("Pinterest", "https://www.pinterest.com/{}/"),
    ("TikTok", "https://www.tiktok.com/@{}"),
    ("Flickr", "https://www.flickr.com/photos/{}"),
    ("Doxbin", "https://doxbin.org/user/{}"),
    ("Paypal", "https://www.paypal.com/paypalme/{}"),
    ("Snapchat", "https://www.snapchat.com/add/{}"),
    ("Instagram", "https://www.bandlab.com/{}"),
    ("Tinder", "https://tinder.com/@{}"),
    ("Cracked", "https://www.cracked.com/members/{}"),
    ("Friendfinder", "https://www.friendfinder-x.com/profile/{}"),
    ("Buymeacoffee", "https://www.buymeacoffee.com/{}"),
    ("Api.minecraft", "https://api.mojang.com/users/profiles/minecraft/{}"),
    ("Telegram", "https://t.me/{}"),
    ("Spotify", "https://open.spotify.com/user/{}"),
    ("Bio link", "https://bio.link/{}"),
    ("Kick", "https://kick.com/{}"),
    ("Twitch", "https://www.twitch.tv/{}"),
    ("Medium", "https://medium.com/@{}"),
    ("Eyeem", "https://www.eyeem.com/u/{}"),
    ("Gitlab", "https://gitlab.com/{}"),
    ("Pastebin", "https://pastebin.com/u/{}")
])

REQUEST_DELAY = 2  
MAX_RETRIES = 3  
last_request_times = {}

def check_username(website, username):
    url = website.format(username)  
    retries = 0  

    while retries < MAX_RETRIES:
        try:
            current_time = time.time()
            if website in last_request_times and current_time - last_request_times[website] < REQUEST_DELAY:
                delay = REQUEST_DELAY - (current_time - last_request_times[website])
                time.sleep(delay)  

            response = requests.get(url)
            last_request_times[website] = time.time()  

            if response.status_code == 200:  
                return url
            else:
                return False
        except requests.exceptions.RequestException:
            retries += 1  
            delay = random.uniform(1, 3) 
            time.sleep(delay) 


from src.email_checker import check_email
from src.github import check_github_email
from src.gravatar import check_gravatar_email
from src.twitter import check_twitter_email
from src.chess import check_chess_email
from src.flickr import check_flickr_email
from src.pinterest import check_pinterest_email
from src.adobe import check_adobe_email
from src.pornhub import pornhub
from src.deezer import deezer
from src.spotify import check_spotify_email
from src.duolingo import check_duolingo_email

from src.pastebin_dumps.pastebin import check_pastebin_dumps
from src.emailrep.emailrep import emailrep
from src.hudsonrock.hudsonrock_api import get_email_info
from src.google_dorking.email import google_dorking_email

from data.help import help
from data.command import command2

from src.phone_osint.phone import google_dork_search, parse_results

from src.IP_Osint.geolocation import geolocation_ip
from src.IP_Osint.hudsonrock import get_info
from src.IP_Osint.subnet import subnet_mask


print(
        f"""{Fore.RED} 
██╗░░██╗░█████╗░░██╗░░░░░░░██╗██╗░░██╗███████╗██████╗░
██║░░██║██╔══██╗░██║░░██╗░░██║██║░██╔╝██╔════╝██╔══██╗
███████║███████║░╚██╗████╗██╔╝█████═╝░█████╗░░██████╔╝
██╔══██║██╔══██║░░████╔═████║░██╔═██╗░██╔══╝░░██╔══██╗
██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░██║░╚██╗███████╗██║░░██║
╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
        {Fore.RESET}"""
        + f"\t{Fore.BLUE}- By {Fore.GREEN}@D3M3T0R{Fore.RESET}\n"
)

def main():
    while True:
        command = input(f'{Fore.RED}║{Fore.WHITE} HAWKER{Fore.RED} ╠══{Fore.LIGHTRED_EX}>{Fore.GREEN} ')

        if command == "help" or command == "?":
            help()
        elif command == "command" or command == "!":
            command2()
        elif command == "cls" or command == "clear":
            clear()
            print(
        f"""{Fore.RED} 
██╗░░██╗░█████╗░░██╗░░░░░░░██╗██╗░░██╗███████╗██████╗░
██║░░██║██╔══██╗░██║░░██╗░░██║██║░██╔╝██╔════╝██╔══██╗
███████║███████║░╚██╗████╗██╔╝█████═╝░█████╗░░██████╔╝
██╔══██║██╔══██║░░████╔═████║░██╔═██╗░██╔══╝░░██╔══██╗
██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░██║░╚██╗███████╗██║░░██║
╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
        {Fore.RESET}"""
        + f"\t{Fore.BLUE}- By {Fore.GREEN}@D3M3T0R{Fore.RESET}\n"
            )
        elif command == "email" or command == "EMAIL":
            email = input(f"{Fore.RED} └{Fore.WHITE} Email :{Fore.GREEN} ")
            asyncio.run(run_osint(email))
        elif command == "phone" or command == "PHONE":
            phone_number = input(f"{Fore.RED} └{Fore.WHITE} Phone :{Fore.GREEN} ")
            html = google_dork_search(phone_number)
     
            if html:
                results = parse_results(html)
        
                if results:
                    print(f"Result : {phone_number}:")
                    for i, result in enumerate(results):
                        print(f"{i + 1}. {result['title']}\n   Link: {result['link']}\n   Snippet: {result['snippet']}\n")
                else:
                    print(f"{Fore.RED}No results found.")
            else:
                print(f"{Fore.RED}Error retrieving results.")
        elif command == "ip" or command == "IP":
            ip = input(f"{Fore.RED} └{Fore.WHITE} IP :{Fore.GREEN} ")
            geolocation_ip(ip)
            time.sleep(0.3)
            get_info(ip)
            time.sleep(0.3)
            print()
            subnet_mask(ip)
        elif command == "search" or command == "SEARCH":
            username = input(f"{Fore.RED} └{Fore.WHITE} Username :{Fore.GREEN} ")
            results = OrderedDict()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(check_username, website, username): website_name for website_name, website in WEBSITES.items()}
                for future in concurrent.futures.as_completed(futures):
                    website_name = futures[future]  
                    try:
                        result = future.result() 
                    except Exception as exc:
                        print(f"{Fore.RED}{website_name} generated an exception: {exc}")
                        result = False
                    finally:
                         results[website_name] = result 
            for website, result in results.items():
                if result:
                    print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}FOUND{Fore.RED}]{Fore.LIGHTMAGENTA_EX} {website}{Fore.WHITE} :{Fore.LIGHTGREEN_EX} {result}")
                else:
                    print(f"{Fore.RED}[{Fore.LIGHTRED_EX}NOT FOUND{Fore.RED}]{Fore.LIGHTMAGENTA_EX} {website}{Fore.WHITE} :{Fore.LIGHTRED_EX} Not Found")





async def run_osint(email):
    print(f'\n{Fore.WHITE}<======================= Email verification =======================>')
    await check_email(email)
    print(f'\n{Fore.WHITE}=== Site results ===')
    await check_github_email(email)
    await check_gravatar_email(email)
    await check_twitter_email(email)
    await check_chess_email(email)
    await check_flickr_email(email)
    await check_pinterest_email(email)
    await check_adobe_email(email)
    await pornhub(email)
    await deezer(email)
    await check_spotify_email(email)
    await check_duolingo_email(email)
    print(f'{Fore.WHITE}')
    check_pastebin_dumps(email)
    print(f'\n{Fore.WHITE}<======================= EmailREP.io =======================>')
    emailrep(email)
    print(f'{Fore.WHITE}\n<======================= Hudsonrock API =======================>')
    get_email_info(email)
    print(f'{Fore.WHITE}\n<======================= Google Dorking Email =======================>')
    file_types = ["pdf", "xlsx", "docx", "txt", "xls", "doc", "ppt", "rft"]

    for file_type in file_types:
        search_results = google_dorking_email(email, file_type)
    
        if search_results:
            for link in search_results:
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}{file_type.upper()}{Fore.RED}]{Fore.WHITE} :{Fore.GREEN} {link}")
    sys.exit()
    

if __name__ == "__main__":
    main()

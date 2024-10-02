import requests
from colorama import Fore, init

init()

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

                print(f"\n{Fore.RED}[{Fore.LIGHTCYAN_EX}Computer Name{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", computer_name)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Operating System{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", operating_system)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}IP{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", ip)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Malware Path{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", malware_path)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}Date Compromised{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", date_compromised)
                print(f"{Fore.RED}[{Fore.LIGHTCYAN_EX}AntiViruses{Fore.RED}]{Fore.WHITE} : {Fore.LIGHTGREEN_EX}", antiviruses)
        else:
            print("No data found...")

    except requests.RequestException as e:
        pass
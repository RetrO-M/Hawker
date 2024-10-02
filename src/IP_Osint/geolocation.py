import requests
from colorama import Fore, init

init()

def geolocation_ip(ip):
    url = "https://ipinfo.io/"+ip+"/json"
    respon = requests.get(url)
    if respon.status_code == 200:
        result = respon.json() 
        print(f"{Fore.RED}[{Fore.LIGHTGREEN_EX}IP{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("ip"))
        print(f"{Fore.RED}[{Fore.LIGHTGREEN_EX}Country{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("country"))
        print(f"{Fore.RED}[{Fore.LIGHTGREEN_EX}City{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("city"))
        print(f"{Fore.RED}[{Fore.LIGHTGREEN_EX}Location{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("loc"))
        print(f"{Fore.RED}[{Fore.LIGHTGREEN_EX}Hostname{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTMAGENTA_EX} ",result.get("hostname"))
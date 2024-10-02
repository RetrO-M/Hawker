import requests, json
from colorama import Fore, init

init()

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
        results = {
            "Disposable": "Email Disposable" if disposable else "No Disposable Email",
            "Data Breach": "Leaks online found" if data_breach else "No leaks found",
            "Spam Reputation": "Spam reputation found" if spam else "No Spam reputation",
            "Spoofable": "Spoofable" if spoofable else "No Spoofable"
        }

        for key, value in results.items():
            print(f"{Fore.RED}[{Fore.LIGHTMAGENTA_EX}{key}{Fore.RED}]{Fore.WHITE} :{Fore.LIGHTCYAN_EX} {value}")
        print()

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error with the EmailRep API request: {e}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error decoding the JSON response.")
    except KeyError as e:
        print(f"{Fore.RED}KeyError: Missing expected key in the response: {e}")


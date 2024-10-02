import requests
from prettytable import PrettyTable
from colorama import Fore, init

init()

def check_pastebin_dumps(email):
    resp = requests.get(f"https://psbdmp.ws/api/v3/search/{email}")


    if resp.status_code == 200:
        try:
            data = resp.json()

            if isinstance(data, list) and len(data) == 0:
                print(f"{Fore.RED}No results found")
            else:
                table = PrettyTable()
                table.field_names = ["Pastebin ID", "Link"]

                for result in data:
                    paste_id = result.get('id')
                    link = f"{Fore.LIGHTGREEN_EX}https://pastebin.com/{paste_id}{Fore.WHITE}"
                    table.add_row([paste_id, link])

                print(table)

        except ValueError:
            print(f"ERROR :{Fore.RED} JSON decoding error")
    else:
        print(f"Error:{Fore.RED} {resp.status_code}")

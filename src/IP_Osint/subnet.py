import requests

def subnet_mask(ip):
    response = requests.get(f'https://api.hackertarget.com/subnetcalc/?q={ip}')

    print(response.text)
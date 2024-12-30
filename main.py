from colorama                                                 import Fore, init
from os                                                       import system
from curl_cffi.requests                                       import get, Session, head, exceptions
from curl_cffi.requests.exceptions                            import RequestException
from re                                                       import findall
from hashlib                                                  import md5
from bs4                                                      import BeautifulSoup
from random                                                   import choice
from bs4                                                      import BeautifulSoup
from urllib.parse                                             import urlencode, urljoin
from time                                                     import sleep
from phonenumbers                                             import parse, is_valid_number, length_of_national_destination_code, format_number, PhoneNumberFormat, is_possible_number
from phonenumbers                                             import geocoder, carrier, timezone, number_type, PhoneNumberType
from bs4                                                      import BeautifulSoup as BSoup
from json                                                     import loads, JSONDecodeError

init()

class Hawker:
    def __init__(self):
        self.headers = {
            "User-Agent": choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.65 Version/17.0 Mobile/15E148 Safari/604.1", 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/117.0.2045.48 Version/17.0 Mobile/15E148 Safari/604.1", 
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/118.0.2088.68 Version/17.0 Mobile/15E148 Safari/604.1", 
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.86 Version/17.0 Mobile/15E148 Safari/604.1", 
                "Mozilla/5.0 (Linux; Android 8.1.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 PTST/240201.144844",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.78 Version/17.0 Mobile/15E148 Safari/604.1", 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.65 Version/17.0 Mobile/15E148 Safari/604.1", 
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.1.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) AvastSecureBrowser/5.3.1 Mobile/15E148 Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 DuckDuckGo/7 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 OpenWave/94.4.4504.39",
                "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Unique/97.7.7239.70",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/121.2277.107 Mobile/15E148 Safari/605.1.15",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) AvastSecureBrowser/5.3.1 Mobile/15E148 Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 DuckDuckGo/7 Safari/605.1.15",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 Config/92.2.7601.2",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.116 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9979.100",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5; rv:123.0esr) Gecko/20100101 Firefox/123.0esr",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.141 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 Config/91.2.2121.13",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.3 Mobile/15E148 Safari/604.1 RDDocuments/8.7.2.978",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.141 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 RDDocuments/8.4.8.940",
                "Mozilla/5.0 (Linux; Android 8.1.0; C5 2019 Build/OPM2.171019.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/118.0.2088.68 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 AtContent/95.5.5392.49",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 Ddg/17.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 EdgA/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 8.1.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 PTST/240201.144844",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.72 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 OpenWave/94.4.4504.39",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Viewer/99.9.9009.89",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.3 Mobile/15E148 Safari/604.1 RDDocuments/8.7.2.978",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Viewer/99.9.9009.89",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Unique/97.7.7286.70",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/93.3.3695.30",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 RDDocuments/8.4.8.940",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 AtContent/95.5.5392.49",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/92.3.3357.27",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 DuckDuckGo/7 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPad; CPU OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 8.1.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 PTST/240201.144844",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.65 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.3.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPad; CPU OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 Ddg/17.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.2.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.78 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPad; CPU OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.1.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.56 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Android 11; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Trailer/93.3.3516.28",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.79 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9979.100",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.116 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/118.0.2088.68 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9415.94",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.56 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.72 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 Ddg/17.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.3 Mobile/15E148 Safari/604.1 RDDocuments/8.7.2.978",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Agency/98.8.8188.80",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Trailer/93.3.3516.28",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 OpenWave/94.4.4504.39",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.0.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.1.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 Config/91.2.2121.13",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 RDDocuments/8.4.8.940",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/92.3.3357.27",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/92.3.3357.27",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Config/92.2.2788.20",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5; rv:123.0esr) Gecko/20100101 Firefox/123.0esr",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Config/92.2.2788.20",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 AtContent/95.5.5392.49",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.3.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.96 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPad; CPU OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.99 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPad; CPU OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.1.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.96 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9850.99",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.99 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/93.3.3695.30",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.150 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.3 Mobile/15E148 Safari/604.1 RDDocuments/8.7.2.978",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Unique/97.7.7239.70",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.65 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 Config/92.2.7601.2",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Herring/95.1.1930.31",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.2.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/92.3.3357.27",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.99 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.150 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 RDDocuments/8.4.8.940",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 8.1.0; C5 2019 Build/OPM2.171019.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.78 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/93.3.3695.30",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.1.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 EdgA/121.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9415.94",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Viewer/99.9.9009.89",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Viewer/99.9.9009.89",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.2.3",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.126 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 AtContent/95.5.5392.49",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.141 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.2.3",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 RDDocuments/8.4.8.940",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5; rv:123.0esr) Gecko/20100101 Firefox/123.0esr",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.105 Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 DuckDuckGo/7 Safari/605.1.15",
                "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9979.100",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 OpenWave/94.4.4504.39",
                "Mozilla/5.0 (iPad; CPU OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Config/92.2.2788.20",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) AvastSecureBrowser/5.3.1 Mobile/15E148 Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Android 11; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9979.100",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.2.3",
                "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.96 Version/17.0 Mobile/15E148 Safari/604.1"
            ]),
            "Accept-Language": choice([
                "en-US,en;q=0.9", "fr-FR,fr;q=0.9", "es-ES,es;q=0.9", "de-DE,de;q=0.9",
                "it-IT,it;q=0.9", "pt-PT,pt;q=0.9", "ru-RU,ru;q=0.9", "ja-JP,ja;q=0.9",
                "zh-CN,zh;q=0.9", "ko-KR,ko;q=0.9", "nl-NL,nl;q=0.9", "ar-SA,ar;q=0.9",
                "hi-IN,hi;q=0.9", "tr-TR,tr;q=0.9", "sv-SE,sv;q=0.9", "da-DK,da;q=0.9",
                "fi-FI,fi;q=0.9", "no-NO,no;q=0.9", "el-GR,el;q=0.9", "th-TH,th;q=0.9",
                "hu-HU,hu;q=0.9", "ro-RO,ro;q=0.9", "cs-CZ,cs;q=0.9", "sk-SK,sk;q=0.9",
                "bg-BG,bg;q=0.9", "lv-LV,lv;q=0.9", "lt-LT,lt;q=0.9", "sl-SI,sl;q=0.9",
                "et-EE,et;q=0.9", "ms-MY,ms;q=0.9", "vi-VN,vi;q=0.9", "bn-BD,bn;q=0.9",
                "sw-KE,sw;q=0.9", "tl-PH,tl;q=0.9", "iw-IL,iw;q=0.9", "pa-PK,pa;q=0.9",
                "fa-IR,fa;q=0.9", "ne-NP,ne;q=0.9", "sq-AL,sq;q=0.9", "km-KH,km;q=0.9",
                "is-IS,is;q=0.9", "hy-AM,hy;q=0.9", "az-AZ,az;q=0.9", "ka-GE,ka;q=0.9",
                "mt-MT,mt;q=0.9", "cy-GB,cy;q=0.9", "tk-TM,tk;q=0.9", "xh-ZA,xh;q=0.9",
                "zu-ZA,zu;q=0.9", "ar-AE,ar;q=0.9", "uk-UA,uk;q=0.9", "si-LK,si;q=0.9",
                "mn-MN,mn;q=0.9", "la-VN,la;q=0.9", "pa-IN,pa;q=0.9", "sw-TZ,sw;q=0.9",
                "te-IN,te;q=0.9", "ta-LK,ta;q=0.9", "ml-IN,ml;q=0.9", "kn-IN,kn;q=0.9",
                "or-IN,or;q=0.9", "gu-IN,gu;q=0.9", "mr-IN,mr;q=0.9", "as-IN,as;q=0.9",
                "my-MM,my;q=0.9", "bs-BA,bs;q=0.9", "hr-HR,hr;q=0.9", "sr-RS,sr;q=0.9",
                "ca-ES,ca;q=0.9", "eo-EO,eo;q=0.9", "oc-FR,oc;q=0.9", "se-NO,se;q=0.9",
                "ay-PE,ay;q=0.9", "qu-PE,qu;q=0.9", "fy-NL,fy;q=0.9", "jv-ID,jv;q=0.9",
                "su-ID,su;q=0.9", "sc-IT,sc;q=0.9", "gd-GB,gd;q=0.9", "wa-BE,wa;q=0.9",
                "sm-WS,sm;q=0.9", "so-SO,so;q=0.9", "ku-TR,ku;q=0.9", "na-NR,na;q=0.9",
                "fj-FJ,fj;q=0.9", "ht-HT,ht;q=0.9", "ti-ER,ti;q=0.9", "sg-CF,sg;q=0.9",
                "br-FR,br;q=0.9", "gn-PY,gn;q=0.9", "af-ZA,af;q=0.9", "csb-PL,csb;q=0.9",
                "hsb-DE,hsb;q=0.9", "yue-HK,yue;q=0.9", "to-TO,to;q=0.9", "dz-BT,dz;q=0.9",
                "qu-BO,qu;q=0.9", "sa-IN,sa;q=0.9", "rw-RW,rw;q=0.9", "mi-NZ,mi;q=0.9",
                "fo-FO,fo;q=0.9", "haw-US,haw;q=0.9", "gl-ES,gl;q=0.9", "nv-US,nv;q=0.9",
                "arn-CL,arn;q=0.9", "kl-GL,kl;q=0.9", "en-NG,en;q=0.9", "tg-TJ,tg;q=0.9",
                "ps-AF,ps;q=0.9", "prs-AF,prs;q=0.9", "am-ET,am;q=0.9", "ig-NG,ig;q=0.9",
                "yo-NG,yo;q=0.9", "ha-NE,ha;q=0.9", "sh-BA,sh;q=0.9", "sr-ME,sr;q=0.9",
                "tt-RU,tt;q=0.9", "ky-KG,ky;q=0.9", "uz-UZ,uz;q=0.9", "ba-RU,ba;q=0.9",
                "kk-KZ,kk;q=0.9", "be-BY,be;q=0.9", "mo-MD,mo;q=0.9", "ab-GE,ab;q=0.9",
                "os-RU,os;q=0.9", "tt-RU,tt;q=0.9", "ts-BW,ts;q=0.9", "st-LS,st;q=0.9"
            ]),
            "DNT": "1",
            "Referer": choice([
                "https://www.google.com", "https://duckduckgo.com", "https://www.startpage.com",
                "https://www.bing.com", "https://www.qwant.com", "https://www.brave.com/search",
                "https://www.mojeek.com", "https://swisscows.com", "https://www.neeva.com"
            ]),
            "Origin": choice([
                "https://www.google.com", "https://duckduckgo.com", "https://www.startpage.com",
                "https://www.bing.com", "https://www.qwant.com", "https://www.brave.com/search",
                "https://www.mojeek.com", "https://swisscows.com", "https://www.neeva.com"
            ]),
        }



    def title(self):
        system('cls || clear')
        print(
            f"""{Fore.LIGHTWHITE_EX}
                 ..,,;;;;;;,,,,
           .,;'';;,..,;;;,,,,,.''';;,..
        ,,''                    '';;;;,;''
       ;'    ,;@@;'{Fore.LIGHTCYAN_EX}  ,@@;, @@,{Fore.LIGHTWHITE_EX} ';;;@@;,;';.
      ''  ,;@@@@@'{Fore.LIGHTCYAN_EX}  ;@@@@; '' {Fore.LIGHTWHITE_EX}   ;;@@@@@;;;;
         ;;@@@@@; {Fore.LIGHTCYAN_EX}   '''{Fore.LIGHTWHITE_EX}     .,,;;;@@@@@@@;;;
        ;;@@@@@@;           , ';;;@@@@@@@@;;;.
         '';@@@@@,.  ,   .   ',;;;@@@@@@;;;;;;
            .   '';;;;;;;;;,;;;;@@@@@;;' ,.:;'
              ''..,,     ''''    '  .,;'
                   ''''''::''''''''
      ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐
      │  {Fore.LIGHTMAGENTA_EX}01:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Email Information {Fore.LIGHTWHITE_EX}     ┃               │ 
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}02:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Phone Information {Fore.LIGHTWHITE_EX}     ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}03:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Person Information {Fore.LIGHTWHITE_EX}    ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}04:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} IP Information {Fore.LIGHTWHITE_EX}        ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}05:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Bitcoin Information{Fore.LIGHTWHITE_EX}    ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}06:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} TikTok Comment Scraper{Fore.LIGHTWHITE_EX} ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}07:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Tiktok Profile Scraper{Fore.LIGHTWHITE_EX} ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}08:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Tiktok Video Scraper  {Fore.LIGHTWHITE_EX} ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥
    ┃ ┌──────┲━━━━━━━━━━━━━━━━━━━━━━━━┱───────────────┐ ┃
    ┃ │  {Fore.LIGHTMAGENTA_EX}09:{Fore.LIGHTWHITE_EX} ┃{Fore.LIGHTCYAN_EX} Wordpress Lists Users {Fore.LIGHTWHITE_EX} ┃               │ ┃
    ┝━┷━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┷━┥"""
        )



    def doxbin_search(self, text):
        query = f"{text} site:doxbin.org"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'doxbin.org' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'doxbin.org' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None



    def instagram_search(self, text):
        query = f"{text} site:instagram.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'instagram.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'instagram.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def twitter_search(self, text):
        query = f"{text} site:x.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'x.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'x.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def youtube_search(self, text):
        query = f"{text} site:youtube.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'youtube.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'youtube.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def facebook_search(self, text):
        query = f"{text} site:facebook.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'facebook.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'facebook.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def pagesjaunes_search(self, text):
        query = f"{text} site:pagesjaunes.fr"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'pagesjaunes.fr' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'pagesjaunes.fr' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None
        
    def whitepages_search(self, text):
        query = f"{text} site:whitepages.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'whitepages.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'whitepages.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def reddit_search(self, text):
        query = f"{text} site:reddit.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'reddit.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'reddit.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def snapchat_search(self, text):
        query = f"{text} site:snapchat.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'snapchat.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'snapchat.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def github_search(self, text):
        query = f"{text} site:github.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'github.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'github.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def check_chess_email(self, email):
        url = f"https://www.chess.com/callback/email/available?email={email}"
        
        try:
            response = get(url, headers=self.headers, impersonate="chrome")
            data = response.json()
        
            if data.get('isEmailAvailable') == True:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Chess.com account") 
            elif data.get('isEmailAvailable') == False:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com Account Found") 
            else:
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Chess.com account") 
        except:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Chess.com account")

    def check_duolingo_email(self, target: str):
        url = "https://www.duolingo.com/2017-06-30/users"

        params = {
            'email': target
        }

        try:
            response = get(url, params=params, headers=self.headers, impersonate="chrome")

            if response.status_code == 200:
                text_response = response.text

                if '{"users":[]}' in text_response:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Duolingo account")
                else:
                    valid = response.json()['users'][0]['username']
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Duolingo Account Found")

        except Exception as e:
            pass

    def check_flickr_email(self, email):
        url = "https://www.flickr.com/"
        
        response = get(url)
        html = response.text

        key_pattern = r'[a-f0-9]{32}'
        keys = findall(key_pattern, html)

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

                response = get(api_url, params=params, headers=self.headers, impersonate="chrome")
                try:
                    data = response.json()
                    if 'user' in data:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} https://www.flickr.com/people/{data['user']['nsid']}/")
                        flickr_found = True
                        break
                except:
                    continue

        if not flickr_found:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Flickr account")

    def check_github_email(self, email):
        url = f"https://api.github.com/search/users?q={email}+in:email"
        
        try:
            response = get(url, headers=self.headers, impersonate="chrome")
        
            if response.status_code == 200:
                result = response.json()
                if result["total_count"] > 0:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} https://github.com/{result['items'][0]['login']}")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No GitHub account")
        except Exception as e:
            pass

    def check_gravatar_email(self, email):
        email_hash = md5(email.strip().lower().encode()).hexdigest()
        url = f"https://en.gravatar.com/{email_hash}.json"
        
        try:
            response = get(url, headers=self.headers, impersonate="chrome")

            if response.status_code == 200:
                data = response.json()
                display_name = data['entry'][0].get('displayName', 'Unknown')
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} https://gravatar.com/{display_name}")
            elif response.status_code == 404:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Gravatar account")
        except Exception as e:
            pass

    def check_pinterest_email(self, email):
        params = {
            "source_url": "/",
            "data": '{"options": {"email": "' + email + '"}, "context": {}}'
        }
        
        try:
            response = get("https://www.pinterest.fr/resource/EmailExistsResource/get/", params=params, headers=self.headers, impersonate="chrome")
        
            if response.status_code == 200:
                data = response.json()
                if data["resource_response"]["data"]:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pinterest Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pinterest account")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pinterest account")

        except Exception as e:
            pass

    def pornhub(self, target: str):
        try:
            with Session() as session:
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
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pornhub account")
                elif response_json.get('email') == "create_account_failed":
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Pornhub Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pornhub account")

        except Exception as e:
            pass

    def check_spotify_email(self, target: str):
        url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
        
        try:
            response = get(url, headers=self.headers, impersonate="chrome")

            if response.status_code == 200:
                responseData = response.json()
            
                if responseData.get('status') == 20:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Spotify Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Spotify account")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Spotify account")

        except Exception as e:
            pass

    def check_twitter_email(self, email):
        url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
        
        try:
            response = get(url, headers=self.headers, impersonate="chrome")
            if response.status_code == 200:
                data = response.json()
                if not data["valid"]:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Twitter Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Twitter account")
        except Exception as e:
            pass

    def wordpress_email(self, email):
        response = get(f'https://public-api.wordpress.com/rest/v1.1/users/{email}/auth-options', headers=self.headers, impersonate="chrome")

        if '"email_verified":true' in response.text:
            print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Wordpress Account Found')
        else:
            print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Wordpress account')



    def picsart(self, target: str):
        params = {
            'email_encoded': 1,
            'emails': target
        }
        try:
            response = get("https://api.picsart.com/users/email/existence", params=params, headers=self.headers, impersonate="chrome")
            response.raise_for_status() 
            if response.json().get('status') == 'success':
                if response.json().get('response'):
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Picsart Account Found")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Picsart Account")

        except exceptions.RequestException as e:
            pass


    def hudsonrock_api(self, text):
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={text}"
        response = get(url, headers=self.headers, impersonate="chrome")
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
                top_logins = data.get('top_logins', [])
                top_passwords = data.get('top_passwords', [])
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Computer Name{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", computer_name)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Operating System{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", operating_system)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ip)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Malware Path{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", malware_path)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date Compromised{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", date_compromised)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} AntiViruses{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", antiviruses)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Top Logins{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_logins))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Passwords{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")


    def check_pastebin_dumps(self, text):
        resp = get(f"https://psbdmp.ws/api/v3/search/{text}", headers=self.headers, impersonate="chrome")
        if resp.status_code == 200:
            try:
                data = resp.json()  

                if isinstance(data, list) and len(data) == 0:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No Pastebin dumps")
                else:
                    for result in data:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} https://pastebin.com/{Fore.LIGHTCYAN_EX}{result.get('id')}")

            except ValueError:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} ERROR Json")

    def search_tor66_all_links(self, text, timeout=10):
        try:
            tor66_url = f"https://tor66.org/search?q={text}"
            base_url = "https://tor66.org"

            response = get(tor66_url, headers=self.headers, impersonate="chrome", timeout=timeout)
            response.raise_for_status() 

            soup = BeautifulSoup(response.text, "html.parser")
            tor66_results = []

            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_link = urljoin(base_url, href)
                
                if href in ("/", "") or text in href or "?" in href:
                    continue
                
                title = link.get_text(strip=True) or "No Title"
                parent = link.find_parent()
                description = (
                    parent.get_text(strip=True) if parent else "No Description"
                )

                if title.lower() not in ["no title", "onions", "clearnet"]:
                    tor66_results.append({
                        "link": full_link,
                        "title": title,
                        "description": description,
                    })

            if tor66_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                         Tor66                        ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for result in tor66_results:
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Title:{Fore.LIGHTWHITE_EX} {result['title']}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Description:{Fore.LIGHTWHITE_EX} {result['description']}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Link:{Fore.LIGHTWHITE_EX} {result['link']}\n")
            else:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No relevant links found on Tor66 for '{text}'.")
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error occurred: {str(e)}")



    def get_detailed_phone_info(self, phone):
        try:
            parsed_number = parse(phone)
            if not is_valid_number(parsed_number):
                return {"Error": "Invalid phone number."}

            phone_info = {
                "Provided Number": phone,
                "Validated Number": format_number(parsed_number, PhoneNumberFormat.E164),
                "Location": geocoder.description_for_number(parsed_number, "en"),
                "Carrier": carrier.name_for_number(parsed_number, "en"),
                "Time Zones": timezone.time_zones_for_number(parsed_number),
                "Country Code": parsed_number.country_code,
                "Number Type": str(number_type(parsed_number)),
                "E.164 Format": format_number(parsed_number, PhoneNumberFormat.E164),
                "National Format": format_number(parsed_number, PhoneNumberFormat.NATIONAL),
                "RFC3966 Format": format_number(parsed_number, PhoneNumberFormat.RFC3966),
                "Is Premium Rate": "Yes" if number_type(parsed_number) == PhoneNumberType.PREMIUM_RATE else "No",
                "Possible Length": length_of_national_destination_code(parsed_number),
                "Associated Country": geocoder.region_code_for_number(parsed_number),
            }

            phone_info["Is Mobile"] = number_type(parsed_number) == PhoneNumberType.MOBILE
            phone_info["Is Fixed Line"] = number_type(parsed_number) == PhoneNumberType.FIXED_LINE
            phone_info["Is VoIP"] = number_type(parsed_number) == PhoneNumberType.VOIP

            phone_info["Is Valid"] = is_valid_number(parsed_number)
            phone_info["Is Possible"] = is_possible_number(parsed_number)

            return phone_info

        except Exception as e:
            return {"Error": str(e)}

    def google_dorking_name(self, text, file_type):
        query = f"{text} filetype:{file_type}"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
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
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None

    def geolocation_ip(self, ip):
        url = f"https://ipwhois.app/json/{ip}"
        respon = get(url, headers=self.headers, impersonate="chrome")
        if respon.status_code == 200:
            result = respon.json() 
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP : ", result.get("ip"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Country : ", result.get("country"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Region : ", result.get("region"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} City : ", result.get("city"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Location : ", f"{result.get('latitude')}, {result.get('longitude')}")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ISP : ", result.get("isp"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Organization : ", result.get("org"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} ASN : ", result.get("asn"))
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Unable to fetch data for IP: {ip}")

    def hudsonrock_ip_api(self, text):
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-ip?ip={text}"
        response = get(url, headers=self.headers, impersonate="chrome")
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
                top_logins = data.get('top_logins', [])
                top_passwords = data.get('top_passwords', [])
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Computer Name{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", computer_name)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Operating System{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", operating_system)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} IP{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ip)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Malware Path{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", malware_path)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Date Compromised{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", date_compromised)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} AntiViruses{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", antiviruses)
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Top Logins{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_logins))
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Passwords{Fore.LIGHTYELLOW_EX} :{Fore.LIGHTWHITE_EX} ", ', '.join(top_passwords), "\n")
        else:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No data found...")


    def archive_search(self, text):
        query = f"{text} site:archive.ph"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }

        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=self.headers, impersonate="chrome")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'archive.ph' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'archive.ph' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None





    def get_bitcoin_info(self, address):
        url = f"https://blockchain.info/rawaddr/{address}"
        
        try:
            response = get(url, headers=self.headers, impersonate="chrome")
            
            if response.status_code != 200:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} ERROR : {response.status_code}")
                return
            
            data = response.json()

            total_balance = data.get('final_balance', 0) / 1e8
            total_transactions = data.get('n_tx', 0)
            total_received = data.get('total_received', 0) / 1e8 
            total_sent = data.get('total_sent', 0) / 1e8 

            first_tx_time = 'None'
            if data.get('txs', []):
                first_tx_time = data['txs'][0].get('time', 'None')

            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bitcoin : {address}")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Balance : {total_balance} BTC")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Transactions : {total_transactions}")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Received : {total_received} BTC")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Sent : {total_sent} BTC")
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} First Transaction (timestamp) : {first_tx_time}")
            
        except Exception as e:
            pass











    def extract_video_id(self, link):
        try:
            if "vm.tiktok.com" in link or "vt.tiktok.com" in link:
                resolved_url = head(link, allow_redirects=True, timeout=5).url
                video_id = resolved_url.split("/")[5].split("?", 1)[0]
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Shortened link resolved: {Fore.LIGHTMAGENTA_EX}{video_id}{Fore.LIGHTWHITE_EX}")
            else:
                video_id = link.split("/")[5].split("?", 1)[0]
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Extracted video ID:{Fore.LIGHTMAGENTA_EX} {video_id}{Fore.LIGHTWHITE_EX}")
            return video_id
        except Exception as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error while extracting video ID: {e}")
            raise

    def scrape_comments(self, video_id):
        cursor = 0
        total_comments = 0
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
            'referer': f'https://www.tiktok.com/@x/video/{video_id}',
        }

        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Starting comment scraping for video:{Fore.LIGHTMAGENTA_EX} {video_id}{Fore.LIGHTWHITE_EX}")

        while True:
            try:
                response = get(
                    f"https://www.tiktok.com/api/comment/list/"
                    f"?aid=1988&aweme_id={video_id}&count=50&cursor={cursor}",
                    headers=headers
                ).json()

                comments = response.get("comments", [])
                if not comments:
                    print(f"    {Fore.LIGHTYELLOW_EX}[+]{Fore.LIGHTWHITE_EX} No more comments found.")
                    break

                for comment in comments:
                    print(f"    {Fore.LIGHTCYAN_EX}[->]{Fore.LIGHTWHITE_EX} COMMENT{Fore.LIGHTMAGENTA_EX} ->{Fore.LIGHTGREEN_EX} {comment['text']}")
                    sleep(0.05)
                    total_comments += 1

                cursor += len(comments)
            except Exception as e:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error during scraping: {e}")
                break




    def get_tiktoker(self, username: str):
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
        }

        tiktok_url = 'https://www.tiktok.com/@'

        try:
            response = get(tiktok_url + username, headers=headers)
            response.raise_for_status()
        except RequestException as e:
            print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Failed to retrieve data for {username}. Error: {e}")
            return

        soup = BSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

        if script_tag:
            try:
                json_data = loads(script_tag.string)
                user_data = json_data['__DEFAULT_SCOPE__']['webapp.user-detail']
                self.parse_tiktoker_data(username, user_data)
            except JSONDecodeError as error:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error parsing JSON: {error}")
        else:
            print(f'    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} No script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__" found.')

    def parse_tiktoker_data(self, username, field: dict):
        user_data = field["userInfo"]["user"]
        user_stats = field["userInfo"]["stats"]
        user_share_meta = field["shareMeta"]

        profile_pic_url = user_data.get("avatarLarger", "")

        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Profile Picture URL: {profile_pic_url}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Account ID:       {user_data["id"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Unique ID:        {user_data["uniqueId"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Nickname:         {user_data["nickname"]}')
        signature = user_data["signature"].replace('\n', ' ')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Bios:             {signature}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Private Account:  {user_data["privateAccount"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} User Country:     {user_data["region"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Account Language: {user_data["language"]}')
        
        print(f'\n    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Followers:  {user_stats["followerCount"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Following:  {user_stats["followingCount"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Hearts     {user_stats["heartCount"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Total Posts:      {user_stats["videoCount"]}')
        
        print(f'\n    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Title:            {user_share_meta["title"]}')
        print(f'    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Description:      {user_share_meta["desc"]}\n')

    def scrape_tiktok_video(self, video_url):
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
        }
        api_url = f"https://www.tiktok.com/oembed?url={video_url}"
        
        response = get(api_url, headers=headers)
        if response.status_code == 200:
            video_data = response.json()
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Title:", video_data.get("title"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Author:", video_data.get("author_name"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Author URL:", video_data.get("author_url"))
            print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Thumbnail:", video_data.get("thumbnail_url"))



    def enumerate_users(self, url):
        print(
            f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                   Wordpress Users                    ║
    ╚══════════════════════════════════════════════════════╝
            '''
        )
        for i in range(1, 100):
            api_endpoint = f"{url}/wp-json/wp/v2/users/{i}"
            try:
                response = get(api_endpoint, headers=self.headers, impersonate="chrome", timeout=10)
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Name: {user_data.get('name')}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Username: {user_data.get('slug')}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Description: {user_data.get('description')}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Link: {user_data.get('link')}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Meta: {user_data.get('meta', 'N/A')}")
                    print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Avatar URLs: {user_data.get('avatar_urls', {}).get('96', 'N/A')}\n")
                elif response.status_code == 404:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} User with ID {i} not found.")
                else:
                    print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Unexpected response: {response.status_code}")
            except Exception as e:
                print(f"    {Fore.LIGHTRED_EX}[+]{Fore.LIGHTWHITE_EX} Error fetching user: {e}")

def main():
    haw = Hawker()
    haw.title()

    while True:
        print(f'    {Fore.LIGHTWHITE_EX}┌─{Fore.LIGHTCYAN_EX}══{Fore.LIGHTWHITE_EX}──[{Fore.LIGHTCYAN_EX}HAWKER{Fore.LIGHTWHITE_EX}]')
        command = input(f'{Fore.LIGHTWHITE_EX}    └─────>  ')
        if command == "00" or command == "0":
            haw.title()
        elif command == "01" or command == "1":
            email = input(f'{Fore.LIGHTWHITE_EX}      EMAIL {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')

            search_results = haw.doxbin_search(email)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin : {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║   Result of Social Networking Sites Linked to Email  ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.check_github_email(email)
            haw.picsart(email)
            haw.pornhub(email)
            haw.check_spotify_email(email)
            haw.check_twitter_email(email)
            haw.check_flickr_email(email)
            haw.check_chess_email(email)
            haw.check_duolingo_email(email)
            haw.check_gravatar_email(email)
            haw.check_pinterest_email(email)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     Hudsonrock API                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_api(email)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     PasteBin Dumps                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.check_pastebin_dumps(email)


            reddit_results = haw.reddit_search(email)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Reddit.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Reddit : {link}")

            snapchat_results = haw.snapchat_search(email)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                     Snapchat.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SnapChat : {link}")

            github_results = haw.github_search(email)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Github.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(email)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                    Instagram.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(email)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                          X.com                       ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            youtube_results = haw.youtube_search(email)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      Youtube.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(email)
            if facebook_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      FaceBook.com                    ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            haw.search_tor66_all_links(email)

        elif command == "02" or command == "2":
            phone = input(f'{Fore.LIGHTWHITE_EX}      PHONE {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')

            search_results = haw.doxbin_search(phone)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin : {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                 Phone Information                    ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )          
            result = haw.get_detailed_phone_info(phone)
            for key, value in result.items():
                print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {key} {Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} {value}")


            reddit_results = haw.reddit_search(phone)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Reddit.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Reddit : {link}")

            snapchat_results = haw.snapchat_search(phone)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                     Snapchat.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SnapChat : {link}")

            github_results = haw.github_search(phone)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Github.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(phone)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                    Instagram.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(phone)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                          X.com                       ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            youtube_results = haw.youtube_search(phone)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      Youtube.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(phone)
            if facebook_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      FaceBook.com                    ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

        elif command == "03" or command == "3":
            fullname = input(f'{Fore.LIGHTWHITE_EX}      Full Name {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')

            search_results = haw.doxbin_search(fullname)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin : {link}")
            print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                Google Dorking Files                  ║
        ╚══════════════════════════════════════════════════════╝
                '''
            )
            file_types = ["pdf", "xlsx", "docx", "txt", "xls", "doc", "ppt", "rft", "odt", "csv"]
            for file_type in file_types:
                search_results = haw.google_dorking_name(fullname, file_type)
        
                if search_results:
                    for link in search_results:
                        print(f"    {Fore.LIGHTGREEN_EX}[+] {Fore.LIGHTMAGENTA_EX} {file_type.upper()} {Fore.LIGHTWHITE_EX}{link}")


            reddit_results = haw.reddit_search(fullname)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Reddit.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in reddit_results:
                    if 'reddit.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} Reddit : {link}")

            snapchat_results = haw.snapchat_search(fullname)
            if snapchat_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                     Snapchat.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in snapchat_results:
                    if 'snapchat.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} SnapChat : {link}")

            github_results = haw.github_search(fullname)
            if reddit_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                       Github.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in github_results:
                    if 'github.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            instagram_results = haw.instagram_search(fullname)
            if instagram_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                    Instagram.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in instagram_results:
                    if 'instagram.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            twitter_results = haw.twitter_search(fullname)
            if twitter_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                          X.com                       ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in twitter_results:
                    if 'x.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")


            youtube_results = haw.youtube_search(fullname)
            if youtube_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      Youtube.com                     ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in youtube_results:
                    if 'youtube.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")

            facebook_results = haw.facebook_search(fullname)
            if facebook_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
        ╔══════════════════════════════════════════════════════╗
        ║                      FaceBook.com                    ║
        ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in facebook_results:
                    if 'facebook.com' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            haw.search_tor66_all_links(fullname)

        elif command == "04" or command == "4":
            ip = input(f'{Fore.LIGHTWHITE_EX}      IP {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')


            search_results = haw.doxbin_search(ip)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin : {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                    IP Information                    ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.geolocation_ip(ip)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     Hudsonrock API                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.hudsonrock_ip_api(ip)
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                     PasteBin Dumps                   ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.check_pastebin_dumps(ip)

        elif command == "05" or command == "5":
            address = input(f'{Fore.LIGHTWHITE_EX}      Bitcoin Address {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')

            search_results = haw.doxbin_search(address)
            if search_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                       DoxBin.org                     ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in search_results:
                    if 'doxbin.org' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} DoxBin : {link}")
            print(
                f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                  Bitcoin Information                 ║
    ╚══════════════════════════════════════════════════════╝
                '''
            )
            haw.get_bitcoin_info(address)

            archive_results = haw.archive_search(address)
            if archive_results:
                print(
                    f'''{Fore.LIGHTWHITE_EX}  
    ╔══════════════════════════════════════════════════════╗
    ║                      Archive.ph                      ║
    ╚══════════════════════════════════════════════════════╝
                    '''
                )
                for link in archive_results:
                    if 'archive.ph' in link:
                        print(f"    {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTWHITE_EX} {link}")
            haw.search_tor66_all_links(address)
        elif command == "06" or command == "6":
            video_url = input(f'{Fore.LIGHTWHITE_EX}      Enter the TikTok link {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ').strip()
            video_id = haw.extract_video_id(video_url)
            haw.scrape_comments(video_id)
        elif command == "07" or command == "7":
            username = input(f"{Fore.LIGHTWHITE_EX}      Enter TikTok username (without '@') {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ")
            if username:
                haw.get_tiktoker(username)
        elif command == "08" or command == "8":
            video_url = input(f'{Fore.LIGHTWHITE_EX}      Enter the TikTok link {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')
            haw.scrape_tiktok_video(video_url)
        elif command == "09" or command == "9":
            url = input(f'{Fore.LIGHTWHITE_EX}      URL {Fore.LIGHTCYAN_EX}:{Fore.LIGHTMAGENTA_EX} ')
            haw.enumerate_users(url)
if __name__ == "__main__":
    main()

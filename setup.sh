#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
WHITE='\033[0;37m'
BLUE='\033[0;34m'


echo -e "${GREEN}  ___|        |    "
echo -e "\___ \   _ \  __|  |   |  __ \  "
echo -e "      |  __/  |    |   |  |   | "
echo -e "_____/ \___| \__| \__._|  .__/  "
echo -e "                         _|   "
echo -e "${WHITE}"

pip3 install aiohttp
pip3 install requests
pip3 install beautifulsoup4
pip3 install prettytable
pip3 install colorama
pip3 install fake-useragent
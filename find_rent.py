#!/bin/python3

import urllib.request
from bs4 import BeautifulSoup

SITE_URL = "https://www.bazaraki.com"
SITE_FILTER = "/real-estate/houses-and-villas-rent/number-of-bedrooms---2/number-of-bedrooms---3/number-of-bedrooms---4/pafos-district-paphos/?price_max=1500"

req = urllib.request.Request(
    SITE_URL + SITE_FILTER, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

with urllib.request.urlopen(req) as url:
    soup = BeautifulSoup(url.read())
    for item in soup.find_all('li', 'announcement-container'):
        print(SITE_URL + item.a['href'])
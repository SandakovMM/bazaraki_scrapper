#!/bin/python3

import urllib.request
from bs4 import BeautifulSoup

SITE_URL = "https://www.bazaraki.com"
SITE_FILTER = "/real-estate/houses-and-villas-rent/number-of-bedrooms---2/number-of-bedrooms---3/number-of-bedrooms---4/pafos-district-paphos/?price_max=1500"


def get_info(drop_other_regions=True):
    req = urllib.request.Request(
        SITE_URL + SITE_FILTER, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req) as url:
        soup = BeautifulSoup(url.read(), "html.parser")

        list = soup.find('ul', 'list-simple__output')
        for item in list.children:
            if item.name == 'li' and item.a is not None:
                print(SITE_URL + item.a['href'])
            elif drop_other_regions and item.name == 'h2' and item.string == "Ads from other regions":
                # I don't want to see other regions
                break


if __name__ == "__main__":
    get_info()
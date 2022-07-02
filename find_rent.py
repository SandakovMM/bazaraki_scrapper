#!/bin/python3
"""
The script that can bew used to check long term rent suggestions.
For now only Paphos on Cyprus from the bazaraki.com web-site.
Usage:
    find_rent.py [options]
Options:
    -h, --help           Display this message.
    -a, --all-regions    Show suggestions for all regions.
    -f, --known-file     choose the file that contains already checked suggestions. So we could not look for them twice.
"""

import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup

USAGE_TEXT = __doc__
SITE_URL = "https://www.bazaraki.com"
SITE_FILTER = "/real-estate/houses-and-villas-rent/number-of-bedrooms---2/number-of-bedrooms---3/number-of-bedrooms---4/pafos-district-paphos/?price_max=1500"


def usage():
    print(USAGE_TEXT)


def extract_already_known(filename):
    with open(filename, 'r') as knownfile:
        return knownfile.readlines()


def get_suggestions(already_known, drop_other_regions):
    req = urllib.request.Request(
        SITE_URL + SITE_FILTER, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    suggestions = []

    with urllib.request.urlopen(req) as url:
        soup = BeautifulSoup(url.read(), "html.parser")

        list = soup.find('ul', 'list-simple__output')
        for item in list.children:
            if item.name == 'li' and item.a is not None:
                if item.a['href'] not in already_known:
                    suggestions.append(SITE_URL + item.a['href'])
            elif drop_other_regions and item.name == 'h2' and item.string == "Ads from other regions":
                # I don't want to see other regions
                break
    return suggestion


if __name__ == "__main__":
    drop_other_regiouns = True
    already_known_filename = None

    try:
        options, args = getopt.getopt(sys.argv[1:], 'haf:',
                                      ['help', 'all-region', 'known-file='])
    except getopt.error, msg:
        usage()
        sys.exit(1)

    for opt, val in options:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-a', '--all-region'):
            drop_other_regiouns = False
        elif opt in ('-f', '--known-file'):
            already_known_filename = val

    suggestions = get_suggestions(extract_already_known(already_known_filename),
                                  drop_other_regiouns)

    for suggestion in suggestions:
        print(suggestion)
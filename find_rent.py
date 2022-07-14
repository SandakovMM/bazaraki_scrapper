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
    res = []
    with open(filename, 'r') as knownfile:
        for suggestion in knownfile.readlines():
            res.append(suggestion.strip())

    return res


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
                suggestions.append(SITE_URL + item.a['href'])
            elif drop_other_regions and item.name == 'h2' and item.string == "Ads from other regions":
                # I don't want to see other regions
                break
    return suggestions


def process_suggestions(suggestions, known_filename):
    already_known = extract_already_known(known_filename)

    new_suggestion_actions = [
        lambda suggestion: print("+ " + suggestion)
    ]
    expired_suggestions_actions = [
        lambda suggestion: print("- " + suggestion)
    ]
    actual_known_suggestions_actions = [ ]

    next_known_list = []
    if change_known_file:
        new_suggestion_actions.append(lambda suggestion: next_known_list.append(suggestion))
        actual_known_suggestions_actions.append(lambda suggestion: next_known_list.append(suggestion))

    for suggestion in suggestions:
        if suggestion not in already_known:
            for action in new_suggestion_actions:
                action(suggestion)

    for known in already_known:
        if known not in suggestions:
            for action in expired_suggestions_actions:
                action(known)
        else:
            for action in actual_known_suggestions_actions:
                action(known)

    if change_known_file and known_filename is not None:
        with open(known_filename, 'w') as known_file:
            for known in next_known_list:
                known_file.write(known + "\n")

if __name__ == "__main__":
    drop_other_regions = True
    change_known_file = False
    known_filename = None

    try:
        options, args = getopt.getopt(sys.argv[1:], 'haif:',
                                      ['help', 'all-region', 'in-place', 'known-file='])
    except getopt.error:
        usage()
        sys.exit(1)

    for opt, val in options:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-a', '--all-region'):
            drop_other_regions = False
        elif opt in ('-i', '--in-place'):
            change_known_file = True
        elif opt in ('-f', '--known-file'):
            known_filename = val

    suggestions = get_suggestions(drop_other_regions)

    process_suggestions(suggestions, known_filename)

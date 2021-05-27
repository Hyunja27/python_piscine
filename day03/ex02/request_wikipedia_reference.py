#!/usr/bin/env python3

import requests
import sys
import json
import dewiki


def request_and_filed(val: str):
    params = {
        "action": "parse",
        "prop": "wikitext",
        "format": "json",
        "page": val,
    }
    rt = requests.get("https://en.wikipedia.org/w/api.php", params=params)
    data = rt.json()
    
    
    # print(dewiki.from_string(data['parse']['wikitext']['*']))


def main():

    if len(sys.argv) != 2:
        raise Exception("arg num error")
    request_and_filed(sys.argv[1])


if __name__ == '__main__':
    main()

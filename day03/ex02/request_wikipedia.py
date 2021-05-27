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
        "redirect": True
    }
    try:
        rt = requests.get("https://en.wikipedia.org/w/api.php", params=params)
        rt.raise_for_status()
    except requests.HTTPError as m:
        raise m
    try:
        data = json.loads(rt.text)
    except Exception:
        raise Exception("json Error")
    if ("error" == list(data.keys())[0]):
        raise Exception("no result Error")
    f = open(val + ".wiki", 'w')
    f.write(dewiki.from_string(data['parse']['wikitext']['*']))
    f.close()


def main():
    if len(sys.argv) != 2:
        return print("arg num error")
    try:
        request_and_filed(sys.argv[1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

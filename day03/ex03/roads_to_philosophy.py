#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

def road_to_phil(URL: str, prev: str, base: str, count: int, log: list):
	if URL in log:
		return print("It leads to an 'infinite loop !")
	try:
		rt = requests.get(url=URL)
		rt.raise_for_status()
	except requests.HTTPError as e:
		if rt.status_code == 404:
				return print("It's a dead end !")
		return 
	all_a = BeautifulSoup(rt.text, 'html.parser')
	
	tmp = all_a.find(id="mw-content-text")
	rt = tmp.select('p > a')
	
	log.append(URL)
	for i in rt:
		if i.get('href') and i['href'].startswith("/wiki/") and not (i['href'].startswith("/wiki/Help") or i['href'].startswith("/wiki/Wikipedia")):
			url = 'https://en.wikipedia.org{page}'.format(page=i['href'])
			print(URL[30:])
			count += 1
			if URL[30:] == "Philosophy":
				return print("{} roads from {} to {} !".format(count, base, URL[30:]))
			return road_to_phil(url, prev=prev, base=base, count=count, log=log)
	if len(log) == 1:
		return print("It's'a dead end !.")


def main():
	if len(sys.argv) != 2:
		raise Exception("Error : single arg needed")
	arg = "/wiki/" + sys.argv[1]
	URL = 'https://en.wikipedia.org{page}'.format(page=arg)
	log = []
	road_to_phil(URL, prev="none", base=sys.argv[1], count=0, log=log)

if __name__ == '__main__':
    main()

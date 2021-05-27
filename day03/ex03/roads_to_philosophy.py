#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from requests.api import get


def road_to_phil(URL: str):
	rt = requests.get(url=URL)
	all_a = BeautifulSoup(rt.text, 'html.parser')
	rt = all_a.find(id="mw-content-text").find_all('a')
	for i in rt:
		if i.get('href').startwith("/wiki/C"):
			print(i)
	# print(rt)

	# val = str(rt[0]).split('"')
	# print(val[1])
	# url = 'https://en.wikipedia.org{page}'.format(page=val[1])
	# road_to_phil(url)


def main():
	if len(sys.argv) != 2:
		raise Exception("Error : single arg needed")
	arg = "/wiki/" + sys.argv[1]
	URL = 'https://en.wikipedia.org{page}'.format(page=arg)
	road_to_phil(URL)

if __name__ == '__main__':
    main()

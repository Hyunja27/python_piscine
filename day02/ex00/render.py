#!/usr/bin/python3

import sys
import re
import os
import settings

def main():
	if len(sys.argv) != 2:
		print("wrong args")
		return
	base = re.compile(".*\.template")
	if base.match(sys.argv[1]) == None:
		print("wrong filename")
		return
	if not os.path.isfile(sys.argv[1]):
		return print("does not exist file...")
	fd = open("myCV.html", 'w')
	get = open("myCV.template", 'r')
	fd.write(''.join(get.readlines()).format(name=settings.name, sur_name=settings.sur_name, page_title=settings.page_title, real_title=settings.real_title, sub_title=settings.sub_title, age=settings.age, profession=settings.profession))
	fd.close()
	get.close()

if __name__=='__main__':
	main()
	

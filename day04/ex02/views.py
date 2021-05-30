from django.shortcuts import render,redirect
from . import forms
import datetime
import time
from django.conf import settings
import logging
from path import Path

def show_message(request):
	try:
		fd = open("logs.log", 'r')
		line = fd.readlines(True)
	except:
		line = "There are No data!"
	log = {'logs':line}
	return render(request, "log.html", log)

def show_create_form(request):
	form = forms.MsForm()
	context = {'form': form}
	return render(request, "input.html", context)

def create_message(request):
	if request.method == 'POST':
		form =  forms.MsForm(request.POST)
		if form.is_valid():
			try:
				Path.touch("logs.log")
			except:
				pass
			fd = open("logs.log", 'a')
			fd.write("<" + str(datetime.datetime.now())[:-7] + ">_________________[" + form.cleaned_data["your_ms"] + "]\n")
			print(form.cleaned_data)
			print(datetime.datetime.now())
			try:
				fd = open("logs.log", 'r')
				line = fd.readlines(True)
			except:
				line = "There are No data!"
			log = {'logs':line}
			return render(request, "log.html", log)
	render(request, "thanks.html")
	form = forms.MsForm()
	context = {'form': form}
	return render(request, "input.html", context)



# def main():

#     try:
#         Path.mkdir("spark_dir")
#     except FileExistsError as e:
#         print(e)
#     Path.touch("spark_dir/spark_note")
#     f = Path("spark_dir/spark_note")

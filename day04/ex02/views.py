from django.shortcuts import render,redirect
from . import forms
import datetime
import time
from django.conf import settings
import logging

def show_message(request):
	return render(request, "log.html")

def show_create_form(request):
	form = forms.MsForm()
	context = {'form': form}
	return render(request, "input.html", context)

def create_message(request):
	if request.method == 'POST':
		form =  forms.MsForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			print(datetime.datetime.now())
			form = forms.MsForm()
			context = {'form': form}
			return render(request, "log.html", context)
	render(request, "thanks.html")
	form = forms.MsForm()
	context = {'form': form}
	return render(request, "input.html", context)

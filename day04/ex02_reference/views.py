from django.shortcuts import render,redirect
from . import forms
from django.conf import settings
import logging

# def show_page_input(request):
# 	return render(request, "input.html")

def show_page_log(request):
	return render(request, "log.html")

logg = logging.getLogger('log')

def control_page(request):
	if request.method == 'POST':
		form =  forms.MsForm(request.POST)
		if form.is_valid():
			logg.info(form.cleaned_data['log'])
			return redirect('log')
	form = forms.MsForm()
	context = {'form': form}
	return render(request, "input.html", context)

def log(request):
	fd = open(settings.LOG_RT, 'r')
	get_line = [l for l in fd.readlines()]
	return render(request, 'log.html', {'log' : get_line})

def thanks(request):
    return render(request, 'thanks.html')
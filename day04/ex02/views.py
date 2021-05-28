from django.shortcuts import render
from django import forms
from .forms import MsForm

def show_page_input(request):
	return render(request, "input.html")

def show_page_log(request):
	return render(request, "log.html")

# def control_page(request):
# 	if request.method == 'POST':
# 		# create a form instance and populate it with data from the request:
# 		form =  MsForm(request.POST)

# 		# check whether it's valid:
# 		if form.is_valid():
# 			forms.your_ms <= 확인된 데이터
# 			# process the data in form.cleaned_data as required
# 			# ...
# 			# redirect to a new URL:
# 			return HttpResponseRedirect('/myform/thanks/')
# 	return render(request, "input.html")

def thanks(request):
    return render(request, 'myform/thanks.html')
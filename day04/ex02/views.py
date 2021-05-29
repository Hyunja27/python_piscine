from django.shortcuts import render
from django import forms
from .forms import MsForm

# def show_page_input(request):
# 	return render(request, "input.html")

def show_page_log(request):
	return render(request, "log.html")

def control_page(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form =  MsForm(request.POST)

		
		print(forms.cleaned_data[form])
		print(form)
		print('!!message =', form)
		# check whether it's valid:
		if form.is_valid():
			vaild_ms = forms.cleaned_data['your_ms']
			print('message =', vaild_ms)
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return HttpResponseRedirect('thanks/')
	else:
		form = MsForm()
		context = {'form': form}
	return render(request, "input.html", context)

def thanks(request):
    return render(request, 'thanks.html')
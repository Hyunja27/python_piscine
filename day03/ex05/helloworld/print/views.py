from django.shortcuts import render

# Create your views here.

def hello(request):
	return render(request, 'helloworld.html')

def ehnkim(request):
	return render(request, 'ehnkim.html')
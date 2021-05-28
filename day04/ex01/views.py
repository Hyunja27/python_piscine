from django.shortcuts import render

# Create your views here.
def show_html_1(request):
	return render(request, "01_django.html")

def show_html_2(request):
	return render(request, "02_display.html")

def show_html_3(request):
	return render(request, "03_temp_engine.html")
from django.shortcuts import render

# Create your views here.

def show_color(request):
	val = []
	k = 1
	for i in range(50):
		val.append(k)
		k += 255 / 51
	table = {'table': val}
	return render(request, "color.html", table)

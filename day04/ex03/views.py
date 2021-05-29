from django.shortcuts import render

# Create your views here.

def show_color(request):

	table = [{'noir':16777215,
			'rough':16711680,
			'bleu':16711680,
			'vert':232462
			 }]
	table.append({'noir': noir })
	
	return render(request, "color.html")

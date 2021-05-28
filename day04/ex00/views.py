from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

def view_mark(request):
    return render(request, 'index.html')

def test2(request):
    return render(request, 'test.html')

def test1(request):
    data = {
        "hi": [
            "spark",
            "jaeskim"
        ]
    }
    return JsonResponse(data)

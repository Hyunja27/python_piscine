from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Movies
from collections import defaultdict
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2
from django import forms

# Create your views here.

def populate(request):
    movie_list = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19"
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        }
    ]
    result = []
    for i in movie_list:
        print(i)
        try:
            Movies.objects.create(
                title=i['title'],
                episode_nb=i['episode_nb'],
                director=i['director'],
                producer=i['producer'],
                release_date=i['release_date']
            )
            result.append("OK")
        except Exception as e:
            result.append(e)
    return HttpResponse("<br />".join([str(i) for i in result]))


class TextChoose(forms.Form):
    update = forms.CharField(required=True)
    titles = forms.ChoiceField(choices=(), required=True)
    def __init__(self, choices=(), *args, **kwargs):
        super(TextChoose, self).__init__(*args, **kwargs)
        self.fields['titles'].choices = choices


def update(request: HttpRequest):
    try:
        movie_list = Movies.objects.all()
        choices = ((movie.title, movie.title) for movie in movie_list)
        if request.method == 'POST':
            data = TextChoose(choices, request.POST)
            if data.is_valid():
                tmp = Movies.objects.get(title=data.cleaned_data['titles'])
                tmp.opening_crawl = data.cleaned_data['update']
                tmp.save()
            return redirect(request.path)
        return render(request, 'remove_05.html', {'choice_field': TextChoose(choices)})
    except Exception as e:
        print(e)
        return HttpResponse("No data available")


def display(request):
    try:
        tmp = Movies.objects.all()
        tmp
    except Exception as e:
        return HttpResponse("No data available")
    return render(request, 'base_07.html', {'movies': tmp})

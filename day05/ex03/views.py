from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Movies
from collections import defaultdict
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2


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


def display(request):
    try:
        tmp = Movies.objects.all()
    except Exception("No data available") as e:
        return HttpResponse(e)
    return render(request, 'base2.html', {'movies': tmp })

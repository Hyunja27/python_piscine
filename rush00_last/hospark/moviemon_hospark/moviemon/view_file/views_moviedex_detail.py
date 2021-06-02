from django.http import request, Http404

from django.shortcuts import render, redirect
from ..movie_data import movie_total
from django.urls import path, include
from ..middlewares.loadSessionMiddleware import loadSession_middleware
from ..utils.game_data import G_Data, load_data, save_data
from ..settings import basic_data
from .views_moviedex import movie_inf

def views_detail(request, imdbID):
    g = G_Data.load(load_data())
    dict_cap_mon = {}
    for i in g.captured_list:
        for key, values in i.items() :
            dict_cap_mon[key] = values

    data = dict_cap_mon[imdbID]
    choice = movie_inf(imdbID=imdbID, Title=data["title"], Poster=data["poster"], Director=data["director"], Year=data["year"], imdbRating=data["rating"], Plot=data["plot"], Actors=data["actors"])
    temp = {
        'detail' : choice
    }
    if request.GET.get('key', None) is not None:
        return get_id(request)
    return render(request, 'pages/Moviedex_detail.html', temp)

def get_id(request):
    id = request.GET.get('key', None)
    print(id)
    if id == "B":
        print("B")
        try :
            return redirect("Moviedex")
        except :
            raise Http404("this is an error")
    try :
        return redirect(request.path)
    except :
        raise Http404("this is an error")
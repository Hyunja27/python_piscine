from tkinter.constants import NO
from django.http import request, Http404
from django.shortcuts import render, redirect
from ..middlewares.loadSessionMiddleware import loadSession_middleware
from ..utils.game_data import G_Data, load_data, save_data
from ..settings import basic_data
import random
# Create your views here.

player_pos = {
    'x': 5,
    'y': 5
}

battlemenu = {
    'a': 0,
    'b': 0,
}

mon_info = {
    'rating': 0,
    'title': 0,
    'year': 0,
    'directer': 0,
    'plot': 0,
    'winnig': 0
}


X_MAX = 9
Y_MAX = 9

def get_mon_info(id):
    g = G_Data.load(load_data())
    dict_mon = {}
    for i in g.left_moviemon:
        for key, values in i.items() :
            dict_mon[key] = values
    mon_info['rating'] = dict_mon[id]['rating']
    mon_info['title'] = dict_mon[id]['title']
    mon_info['year'] = dict_mon[id]['year']
    mon_info['director'] = dict_mon[id]['director']
    mon_info['plot'] = dict_mon[id]['plot']
    mon_info['poster'] = dict_mon[id]['poster']
    catch_or_not()
    


def catch_or_not():
    g = G_Data.load(load_data())
    c = 50 -  (mon_info['rating'] * 10) + (g.get_strength() * 5)
    # c = 90
    if c < 1: c = 1.0
    if c > 90: c = 90.0
    mon_info['winnig'] = c
    if random.randint(0, 100) <= c: return True 
    else: return False

def toss_coin():
    return random.randint(0,1)

def encounter_something(request):
    g = G_Data.load(load_data())
    if toss_coin():
        if toss_coin():
            if toss_coin() and g.movieballCount < 42:
                if toss_coin(): ball_amount = 2
                else: ball_amount = 1
                g.movieballCount += ball_amount
                # print("\n\n====Ball_obt :", ball_amount, "====\n\n")
                # context = {'old_ball': g.movieballCount, 'obt_ball' : ball_amount}
                save_data(g.dump())
                return redirect('situation_obt')
                # print("\n\n====ToTal_ball :", g.movieballCount, "====\n\n")
                # return render(request, 'pages/Obtain.html', context)
            # mon_index = random.randint(0, len(g.left_moviemon))
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_up(request):
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_left(request):
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_right(request):
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_down(request):
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_A(request, id):
    g:G_Data = G_Data.load(load_data())
    battlemenu['b'] = 0
    context = {'mon_id': id,
           'ballnum': g.movieballCount,
           'ch_a': "8px",
            'ch_b': "0px",
            'poster': mon_info['poster'],
            'winnig': mon_info['winnig'],
            'strength': g.get_strength(),
            'rating': mon_info['rating']
            }
    if battlemenu['a'] == 0:
        battlemenu['b'] = 0
        battlemenu['a'] = 1
        return render(request, 'pages/Battle.html', context)
    caught = None
    if g.movieballCount > 0:
        g.movieballCount -= 1
        context['ballnum'] = g.movieballCount
        if catch_or_not() is True:
            for i, dili in enumerate(g.left_moviemon):
                if dili.get(id):
                    g.captured_list.append(dili)
                    g.left_moviemon.remove(dili)
                    # print("@@@",len(g.captured_list))
                    break
            save_data(g.dump())
            return redirect('situation_cap')
    context['missed'] = "Holy shit... Missed!"
    context['runch'] = "Launch Movieball !"
    save_data(g.dump())
    if len(g.left_moviemon) == 0 :
        return redirect('End')
    return render(request, 'pages/Battle.html', context)


def press_B(request, id):
    g = G_Data.load(load_data())
    battlemenu['a'] = 0
    get_mon_info(id)
    context = {'mon_id': id,
           'ballnum': g.movieballCount,
           'ch_a': "0px",
            'ch_b': "8px",
            'poster': mon_info['poster'],
            'winnig': mon_info['winnig'],
            'strength': g.get_strength(),
            'rating': mon_info['rating']
            }
    if battlemenu['b'] == 0:
        battlemenu['a'] = 0
        battlemenu['b'] = 1
        context['missed'] = "Holy shit..."
        return render(request, 'pages/Battle.html', context)
    try :
        return redirect('Worldmap_page')
    except :
        raise Http404("redirect error")

def press_Start(request):
    print("Start")
    try :
        return redirect('Option')
    except :
        raise Http404("redirect error")


def press_Select(request):
    print("Select")
    try :
        return redirect('Moviedex')
    except :
        raise Http404("redirect error")


def get_id(request, id):
    k = request.GET.get('key', None)
    if k == "up":
        return press_up(request)
    elif k == "left":
        return press_left(request)
    elif k == "right":
        return press_right(request)
    elif k == "down":
        return press_down(request)
    elif k == "A":
        return press_A(request, id)
    elif k == "B":
        return press_B(request, id)
    elif k == "Start":
        return press_Start(request)
    elif k == "Select":
        return press_Select(request)
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def Titlescreen(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request, id)
    return render(request, 'pages/Titlescreen.html')

@loadSession_middleware
def Worldmap(request):
    g = G_Data.load(load_data())
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    context = {'cur_x': g.px,
               'cur_y': g.py,  "ten": [i for i in range(10)], 'ballnum': g.movieballCount}
    return render(request, 'pages/Worldmap.html', context)


def Battle(request, id):
    get_mon_info(id)
    key = request.GET.get('key', None)
    if key is not None:
        return get_id(request, id)
    g = G_Data.load(load_data())
    context = {'mon_id': id,
           'ballnum': g.movieballCount,
           'ch_a': "0px",
            'ch_b': "0px",
            'poster': mon_info['poster'],
            'winnig': mon_info['winnig'],
            'strength': g.get_strength(),
            'rating': mon_info['rating']
            }
    return render(request, 'pages/Battle.html', context)


def Moviedex(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/Moviedex.html')


def Detail(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/Moviedex.html')


def Option(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/Options.html')


def Save(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/options/save_game.html')


def Load(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/options/load_game.html')

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

situation = {
    'battle': 0,
    'getball': 0,
}


X_MAX = 9
Y_MAX = 9

def get_one_mon():
    g = G_Data.load(load_data())
    pick = random.randint(0, len(g.left_moviemon) - 1)
    return pick

def toss_coin():
    return random.randint(0,1)

def encounter_something(request):
    situation['getball'] = 1
    g = G_Data.load(load_data())
    if toss_coin():
        if toss_coin():
            if toss_coin() and g.movieballCount < 42:
                if toss_coin(): ball_amount = 2
                else: ball_amount = 1
                g.movieballCount += ball_amount
                save_data(g.dump())
                try :
                    return redirect('situation_obt')
                except :
                    raise Http404("redirect error")
        elif toss_coin():   
            save_data(g.dump())
            # pick = get_one_mon()
            # id = list(g.left_moviemon[pick])[0]
            try :
                return redirect('situation_enc')
            except :
                raise Http404("redirect error")
            # return redirect('battle/' + id)
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_up(request):
    if (situation['battle'] != 1 and situation['battle'] != 1):
        g = G_Data.load(load_data())
        if (g.py > 0):
            g.py -= 1
        if len(g.left_moviemon) > 0:
            save_data(g.dump())
            return encounter_something(request)
        save_data(g.dump())
        try :
            return redirect(request.path)
        except :
            raise Http404("redirect error")


def press_left(request):
    if (situation['battle'] != 1 and situation['battle'] != 1):
        g = G_Data.load(load_data())
        if (g.px > 0):
            g.px -= 1
        if len(g.left_moviemon) > 0:
            save_data(g.dump())
            return encounter_something(request)
        save_data(g.dump())
        try :
            return redirect(request.path)
        except :
            raise Http404("redirect error")


def press_right(request):
    if (situation['battle'] != 1 and situation['battle'] != 1):
        g = G_Data.load(load_data())
        if (g.px < X_MAX):
            g.px += 1
        if len(g.left_moviemon) > 0:
            save_data(g.dump())
            return encounter_something(request)
        save_data(g.dump())
        try :
            return redirect(request.path)
        except :
            raise Http404("redirect error")


def press_down(request):
    if (situation['battle'] != 1 and situation['battle'] != 1):
        g = G_Data.load(load_data())
        if (g.py < Y_MAX):
            g.py += 1
        if len(g.left_moviemon) > 0:
            save_data(g.dump())
            return encounter_something(request)
        save_data(g.dump())
        try :
            return redirect(request.path)
        except :
            raise Http404("redirect error")


def press_A(request):
    if (situation['battle'] == 1 or situation['battle'] == 1):
        print("A")
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_B(request):
    if (situation['battle'] == 1 or situation['battle'] == 1):
        print("B")
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def press_Start(request):
    print("Start")
    try :
        return redirect('Option')
    except :
        raise Http404("redirect error")


def press_Select(request):
    try :
        return redirect('Moviedex')
    except :
        raise Http404("redirect error")


def get_id(request):
    id = request.GET.get('key', None)
    if id == "up":
        return press_up(request)
    elif id == "left":
        return press_left(request)
    elif id == "right":
        return press_right(request)
    elif id == "down":
        return press_down(request)
    elif id == "A":
        return press_A(request)
    elif id == "B":
        return press_B(request)
    elif id == "Start":
        return press_Start(request)
    elif id == "Select":
        return press_Select(request)
    try :
        return redirect(request.path)
    except :
        raise Http404("redirect error")


def Titlescreen(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/Titlescreen.html')

@loadSession_middleware
def Worldmap(request):
    g = G_Data.load(load_data())
    print("[",g,"]")
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    context = {'cur_x': g.px,
               'cur_y': g.py,  "ten": [i for i in range(10)], 'ballnum': g.movieballCount}
    return render(request, 'pages/Worldmap.html', context)


def Battle(request):
    id = request.GET.get('key', None)
    if id is not None:
        return get_id(request)
    return render(request, 'pages/Battle.html')


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

  

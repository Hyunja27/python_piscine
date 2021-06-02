import pickle
import django
from django.http import Http404
from tkinter.constants import NO, NONE
from django.shortcuts import render, redirect

from ..utils.game_data import G_Data, load_data, load_data
import sys
import os
import re


class Index():
    g = G_Data.load(load_data())
    def __init__(self, index, saveA={}, saveB={}, saveC={}):
        self.index = index
        self.saveA = saveA
        self.saveB = saveB
        self.saveC = saveC


    def press_left(self):
        if (self.index == 0):
            self.index = 2
        else:
            self.index = self.index - 1

    def press_right(self):
        if (self.index == 2):
            self.index = 0
        else:
            self.index = self.index + 1

    def press_A(self):
        if self.index == 0:
            type = "slota"
        elif self.index == 1:
            type = "slotb"
        elif self.index == 2:
            type = "slotc"
        regex = re.compile(type)
        path = "./moviemon/saved_game/"
        for file in sorted(os.listdir(path)):
            if re.match(regex, file) is not None:
                os.remove(path + file)
        file = ""
        f = open("session.bin", "rb")
        data = pickle.load(f)
        f.close()
        data = load_data()
        file = type + "_" + str(len(data["captured_list"])) + "_" + "15.mmg"
        path = "./moviemon/saved_game/" + file
        with open(path, "wb") as f:
            pickle.dump(data, f)
        return ('Titlescreen_page')

    def check(self, saveA={}, saveB={}, saveC={}):
        a_regex = re.compile("slota")
        b_regex = re.compile("slotb")
        c_regex = re.compile("slotc")
        path = "./moviemon/saved_game/"
        for file in sorted(os.listdir(path)):
            if re.match(a_regex, file) is not None:
                self.saveA = load_data(path+file)
                break
            else:
                self.saveA = {}
        for file in sorted(os.listdir(path)):
            if re.match(b_regex, file) is not None:
                self.saveB = load_data(path+file)
                print(self.saveB)
                break
            else:
                self.saveB = {}
        for file in sorted(os.listdir(path)):
            if re.match(c_regex, file) is not None:
                self.saveC = load_data(path+file)
                break
            else:
                self.saveC = {}

index = Index(0, 0)

def views_Save(request):
    if request.GET.get('key', None) is not None:
        return get_id(request, index)
    color = [0, 0, 0]
    color[index.index] = "#ffd700"
    index.check()
    a = "x"
    b = "x"
    c = "x"
    if not index.saveA:
        pass
    else:
        a = str(len(index.saveA["captured_list"]))
    if not index.saveB:
        pass
    else:
        b = str(len(index.saveB["captured_list"]))
    if not index.saveC:
        pass
    else:
        c = str(len(index.saveC["captured_list"]))
    
    tmp = {
        'A': color[0],
        'B': color[1],
        'C': color[2],
        "save_A": a,
        "save_B": b,
        "save_C": c,
    }
    return render(request, 'pages/Save.html', tmp)


def get_id(request, index):
    id = request.GET.get('key', None)
    if id == "left":
        print("left")
        index.press_left()
    elif id == "right":
        print("right")
        index.press_right()
    elif id == "A":
        print("A")
        t = index.press_A()
        print(t)
        index.index = 0
        return (redirect(t))
    elif id == "B":
        index.index = 0
        try :
            return redirect('Option')
        except :
           raise Http404("redirect error")
    try : 
        return redirect(request.path)
    except :
        raise Http404("redirect error")
        

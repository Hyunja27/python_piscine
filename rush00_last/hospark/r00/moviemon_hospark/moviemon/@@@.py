# from tkinter.constants import NO
# from django.shortcuts import render, redirect
# # Create your views here.

# titlemenu = {
#     'a': 0,
#     'b': 1
# }


# def press_up(request):
#     print("up")


# def press_left(request):
#     print("left")


# def press_right(request):
#     print("right")


# def press_down(request):
#     print("down")


# def press_A(request):
#     if titlemenu['a'] == 0:
#         titlemenu['b'] = 0
#         titlemenu['a'] = 1
#         context = {
#             'ch_a': "14px",
#             'ch_b': "0px"
#         }
#         print(context)
#         return render(request, 'pages/Titlescreen.html', context)
#     print("A")
#     return Titlescreen(request)


# def press_B(request):
#     if titlemenu['b'] == 0:
#         titlemenu['a'] = 0
#         titlemenu['b'] = 1
#         context = {
#             'ch_a': "0px",
#             'ch_b': "14px"
#         }
#         print(context)
#         return render(request, 'pages/Titlescreen.html', context)
#     print("B")
#     return Titlescreen(request)


# def press_Start(request):
#     print("Start")

# def press_Select(request):
#     print("Select")

# def get_id(request):
#     id = request.GET.get('key', None)
#     if id == "up":
#         return press_up(request)
#     elif id == "left":
#         return press_left(request)
#     elif id == "right":
#         return press_right(request)
#     elif id == "down":
#         return press_down(request)
#     elif id == "A":
#         return press_A(request)
#     elif id == "B":
#         return press_B(request)
#     elif id == "Start":
#         return press_Start(request)
#     elif id == "Select":
#         return press_Select(request)
#     return redirect(request.path)


# def Titlescreen(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return render(request, 'pages/Titlescreen.html')


# def Worldmap(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return render(request, 'pages/Worldmap.html', {'num' : 20})

# def Battle(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return render(request, 'pages/Battle.html')


# def Moviedex(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return views_movie.views_movies(request, "pages/Moviedex.html")


# def Detail(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return 


# def Option(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return render(request, 'pages/Options.html')


# def Save(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return render(request, 'pages/options/save_game.html')


# def Load(request):
#     id = request.GET.get('key', None)
#     if id is not None:
#         return get_id(request)
#     return render(request, 'pages/options/load_game.html')

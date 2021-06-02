from django.shortcuts import redirect
from functools import wraps
from ..utils.game_data import G_Data, load_data


def loadSession_middleware(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        data = load_data()
        if data is None:
            return redirect("")
        return view_function(request, *args, **kwargs)

    return wrap
from django.urls import path

from . import views

urlpatterns = [
    path('ex00', views.view_mark, name='view_mark'),
]

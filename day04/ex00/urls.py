from django.urls import path

from . import views

urlpatterns = [
    path('ex00', views.view_mark, name='view_mark'),
    path('1', views.test1, name='test1'),
    path('2', views.test2, name='test2'),
]

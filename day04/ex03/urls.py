from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('', views.show_color, name='show_color'),
]
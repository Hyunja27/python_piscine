from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('', views.show_create_form, name='show_create_form'),
	path('input', views.show_create_form, name='show_create_form'),
	path('log', views.show_message, name='show_message'),
	path('thanks', views.create_message, name='create_message')
]
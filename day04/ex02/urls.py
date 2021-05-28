from django.urls import path

from . import views

urlpatterns = [
	path('input', views.show_page_input, name='show_page_input'),
	path('log', views.show_page_log, name='show_page_log')
]
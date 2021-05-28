
from django.urls import path

from . import views

urlpatterns = [
	path('django', views.show_html_1, name='show_html_1'),
	path('display', views.show_html_2, name='show_html_2'),
	path('templates', views.show_html_3, name='show_html_3')	
]
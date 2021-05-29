from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('input', views.control_page, name='control_page'),
	path('log', views.show_page_log, name='show_page_log'),
	url('thanks', views.thanks),
]
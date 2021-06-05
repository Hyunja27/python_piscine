
from django.shortcuts import redirect
from django.urls import path
from .views import views
from .views.views import Register, Show_Page 

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('tip/', views.Tip.as_view(), name='tip'),
]
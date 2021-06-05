
from django.shortcuts import redirect
from django.urls import path
from .views import views
from django.conf.urls.static import static
from .views.views import Register, Show_Page 
from rush01 import settings

urlpatterns = [
	path('index/', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('tip/', views.Tip.as_view(), name='tip'),
    path('profile/', views.Profile_Edit, name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


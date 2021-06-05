
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleView.as_view(), name='article'),
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('publicate/', views.PublicView.as_view(), name='publication'),
    path('register/', views.Register_View.as_view(), name='register'),
    path('populate/', views.populate, name='populate'),
    path('detail/<pk>', views.Detail_View.as_view(), name='detail'),
    path('favorite/', views.Favorite_View.as_view(), name='favorite'),
    path('publish/', views.Publish.as_view(), name='publish')
]


from django.urls import path
from . import views
from ex00 import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Image_show.as_view(), name='index')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
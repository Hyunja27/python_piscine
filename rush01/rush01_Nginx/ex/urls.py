from django.shortcuts import redirect
from django.urls import path
from .views import views
from django.conf.urls.static import static
from .views.views import Register, Show_Page
from rush01 import settings

urlpatterns = [
    path("index/", views.Index.as_view(), name="index"),
    path("register/", views.Register.as_view(), name="register"),
    path("", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("tip/", views.Tip.as_view(), name="tip"),
    path("profile/", views.Profile_Edit, name="profile"),
    path("admin/", views.Admin_edit, name="admin"),
    path("articles/", views.ArticleView.as_view(), name="article"),
    # path("detail/<pk>", views.Detail_View.as_view(), name="detail"),
    path("detail/<pk>", views.article_detail, name="detail"),
    path("publicate/", views.PublicView.as_view(), name="publication"),
    path("publish/", views.Publish.as_view(), name="publish"),
    path(
        "create_comment/<int:commnets_id>",
        views.Create_comment.as_view(),
        name="create_comment",
    ),
    path(
        "create_recomment/<int:commnets_id>", views.Create_recomment, name="create_recomment"
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

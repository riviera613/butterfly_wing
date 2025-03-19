from django.urls import path
from api import views

urlpatterns = [
    path("post/list", views.get_post_list),
    path("post/detail", views.get_post_detail),
    path("post/add", views.add_post),

    path("comment/list", views.get_comment_list),
    path("comment/add", views.add_comment),

    path("user/register", views.user_register),
    path("user/name", views.get_username),
]
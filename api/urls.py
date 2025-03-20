from django.urls import path
from api.views import post, user

urlpatterns = [
    path("post/list", post.get_post_list),
    path("post/detail", post.get_post_detail),
    path("post/add", post.add_post),

    path("comment/list", post.get_comment_list),
    path("comment/add", post.add_comment),

    path("user/register", user.user_register),
    path("user/login", user.user_login),
    path("user/logout", user.user_logout),
    path("user/info", user.get_userinfo),

    path("wechat/login", user.wechat_login),
    path("wechat/callback", user.wechat_callback),
]
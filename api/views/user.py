import json
import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user_register(request):
    post_data = json.loads(request.body)
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")
    if not username or not email or not password:
        return JsonResponse(dict(code=1, message="Input error"))
    if User.objects.filter(username=username).first():
        return JsonResponse(dict(code=1, message="Username exist"))
    User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    return JsonResponse(dict(code=0, message="Success"))


@csrf_exempt
def user_login(request):
    post_data = json.loads(request.body)
    username = post_data.get("username")
    password = post_data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(dict(code=0, message="Success"))
    else:
        return JsonResponse(dict(code=1, message="Login failed"))
    

@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse(dict(code=0, message="Success"))


@csrf_exempt
def get_userinfo(request):
    return JsonResponse(dict(code=0, message="Success", data=dict(
        username=request.user.username,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        email=request.user.email
    )))


def wechat_login(request):
    base_url = "https://open.weixin.qq.com/connect/qrconnect"
    params = {
        "appid": settings.WECHAT_APPID,
        "redirect_uri": settings.WECHAT_REDIRECT_URI,
        "response_type": "code",
        "scope": "snsapi_login",
        "state": "STATE"
    }
    url = f"{base_url}?{"&".join([f"{k}={v}" for k, v in params.items()])}#wechat_redirect"
    return redirect(url)


def wechat_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("/")

    # 获取 access_token
    base_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    params = {
        "appid": settings.WECHAT_APPID,
        "secret": settings.WECHAT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    access_token = data.get("access_token")
    openid = data.get("openid")

    if not access_token or not openid:
        return redirect("/")

    # # 获取用户信息
    # base_url = "https://api.weixin.qq.com/sns/userinfo"
    # params = {
    #     "access_token": access_token,
    #     "openid": openid
    # }
    # response = requests.get(base_url, params=params)
    # user_info = response.json()

    username = "wechat_user_{openid}"
    password = username
    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(username=username, email=f"{username}@test.com", password=password)
    login(request, user)
    return redirect("/")

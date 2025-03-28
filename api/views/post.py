import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Post, Comment


def get_post_list(request):
    page = int(request.GET.get("page") or 1)
    size = int(request.GET.get("size") or 100)

    total = Post.objects.all().count()
    post_list = Post.objects.all().order_by("-id")[(page - 1) * size: page * size]
    return JsonResponse(dict(
        code=0,
        message="Success",
        data=dict(
            total=total,
            post_list=list(map(lambda x: x.to_dict(), post_list))
        )
    ))


def get_post_detail(request):
    post_id = int(request.GET.get("id") or 0)
    if not post_id:
        return JsonResponse(dict(code=1, message="Post ID not exist"))
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return JsonResponse(dict(code=1, message="Post ID not exist"))
    return JsonResponse(dict(code=0, message="Success", data=post.to_dict()))


@csrf_exempt
def add_post(request):
    if not request.user or not request.user.username:
        return JsonResponse(dict(code=1, message="User not login"))
    post_data = json.loads(request.body)
    post = Post(
        title=post_data.get("title"),
        content=post_data.get("content"),
        username=request.user.username
    )
    post.save()
    return JsonResponse(dict(code=0, message="Success"))


def get_comment_list(request):
    post_id = int(request.GET.get("post_id") or 0)
    page = int(request.GET.get("page") or 1)
    size = int(request.GET.get("size") or 100)

    total = Comment.objects.filter(post_id=post_id).count()
    comment_list = Comment.objects.filter(post_id=post_id).order_by("id")[(page - 1) * size: page * size]
    return JsonResponse(dict(
        code=0,
        message="Success",
        data=dict(
            total=total,
            comment_list=list(map(lambda x: x[0].to_dict(x[1] + 1), zip(comment_list, range(len(comment_list)))))
        )
    ))


@csrf_exempt
def add_comment(request):
    if not request.user or not request.user.username:
        return JsonResponse(dict(code=1, message="User not login"))
    post_data = json.loads(request.body)
    post_id = int(post_data.get("post_id") or 0)
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return JsonResponse(dict(code=1, message="Post ID not exist"))
    comment = Comment(
        post_id=post_id,
        content=post_data.get("content"),
        username=request.user.username
    )
    comment.save()
    return JsonResponse(dict(code=0, message="Success"))

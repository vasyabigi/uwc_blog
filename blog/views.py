from django.shortcuts import render
from models import Post


def post_list(request, template_name='blog/post_list.html'):
    post_list = Post.objects.published()
    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)

from django.shortcuts import render
from blog.models import Post


def home(request, template_name='home.html'):
    posts = Post.objects.published()
    return render(request, template_name, {'posts': posts})

from django.shortcuts import render
from blog.models import Category


def home(request, template_name='home.html'):
    categories = Category.objects.all()
    return render(request, template_name, {'categories': categories})

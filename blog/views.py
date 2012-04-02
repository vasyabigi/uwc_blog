import time
import datetime

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404

from models import Post, Category


def post_list(request, template_name='blog/post_list.html'):
    post_list = Post.objects.published()
    return render(request, template_name, {'post_list': post_list})


def archive_year(request, year, template_name="blog/archive_year.html"):
    """Blog yearly archive view."""
    lookup_kwargs = {'publish__year': year}

    now = timezone.now()
    if int(year) >= now.year:
        lookup_kwargs['publish__lte'] = now

    posts = Post.objects.published().filter(**lookup_kwargs)
    if not posts:
        raise Http404

    date_list = posts.dates('publish', 'month')

    context = {
        'posts': posts,
        'date_list': date_list,
        'year': year,
    }
    return render(request, template_name, context)


def archive_month(request, year, month, template_name="blog/archive_month.html"):
    """Blog monthly archive view."""
    try:
        tt = time.strptime("%s-%s" % (year, month), '%s-%s' % ('%Y', '%b'))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)

    lookup_kwargs = {
        'publish__gte': first_day,
        'publish__lt': last_day,
    }

    now = timezone.now()
    if last_day >= now.date():
        lookup_kwargs['publish__lte'] = now

    posts = Post.objects.published().filter(**lookup_kwargs)
    if not posts:
        raise Http404

    date_list = posts.dates('publish', 'month')

    context = {
        'posts': posts,
        'date_list': date_list,
        'month': date,
    }
    return render(request, template_name, context)


def archive_day(request, year, month, day, template_name="blog/archive_day.html"):
    """Blog daily archive view."""
    try:
        tt = time.strptime('%s-%s-%s' % (year, month, day),
                           '%s-%s-%s' % ('%Y', '%b', '%d'))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    lookup_kwargs = {
        'publish': date,
    }

    now = timezone.now()
    if int(year) >= now.year:
        lookup_kwargs['publish__lte'] = now

    posts = Post.objects.published().filter(**lookup_kwargs)
    context = {
        'posts': posts,
        'day': date,
    }

    return render(request, template_name, context)


def post_detail(request, slug, year, month, day, template_name="blog/post_detail.html"):
    try:
        tt = time.strptime('%s-%s-%s' % (year, month, day),
                           '%s-%s-%s' % ('%Y', '%b', '%d'))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    lookup_kwargs = {
        'publish': date,
        'slug__exact': slug,
    }

    now = timezone.now()
    if date >= now.date():
        lookup_kwargs['publish__lte'] = now

    try:
        post = Post.objects.published().get(**lookup_kwargs)
    except Post.DoesNotExist:
        raise Http404
    return render(request, template_name, {'post': post})


def category_detail(request, slug, template_name="blog/category_detail.html"):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.published()
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, template_name, context)

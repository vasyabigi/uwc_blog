import datetime
from django.db import models
from django.db.models import Manager


class PublicManager(Manager):
    """Returns published posts that are not in the future."""

    def published(self):
        return self.get_query_set().filter(status__gte=2, publish__lte=datetime.datetime.now())


class Category(models.Model):
    """Blog category model."""
    title = models.CharField(u'Title', max_length=255)
    slug = models.SlugField(u'Slug', unique=True)

    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'

    def __unicode__(self):
        return self.title


class Post(models.Model):
    """Blog post model."""
    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
    )
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('Slug', unique_for_date='publish')
    author = models.CharField('Author', max_length=255)
    content = models.TextField('Content',)
    status = models.IntegerField('Status', choices=STATUS_CHOICES, default=2)
    publish = models.DateTimeField('Publish', default=datetime.datetime.now)
    categories = models.ManyToManyField(Category, blank=True)
    updated = models.DateTimeField('Created', auto_now=True)
    created = models.DateTimeField('Created', auto_now_add=True)

    objects = PublicManager()

    class Meta:
        verbose_name = u'Post'
        verbose_name_plural = u'Posts'
        ordering = ('-publish',)

    def __unicode__(self):
        return self.title
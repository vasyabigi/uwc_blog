from django.db import models
from django.db.models import Manager
from django.utils import timezone


class PublicManager(Manager):
    """Returns published posts that are not in the future."""

    def published(self):
        return self.get_query_set().filter(status__gte=2, publish__lte=timezone.now())


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
    publish = models.DateField('Publish', default=timezone.now)
    categories = models.ManyToManyField(Category, blank=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created = models.DateTimeField('Created', auto_now_add=True)

    objects = PublicManager()

    class Meta:
        verbose_name = u'Post'
        verbose_name_plural = u'Posts'
        ordering = ('-publish',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)

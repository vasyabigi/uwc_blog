from django.db import models
from django.db.models import Manager
from django.utils import timezone


class Tag(models.Model):
    """Tag model."""
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField()

    class Meta:
        verbose_name = u'Tag'
        verbose_name_plural = u'Tags'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('blog:tag_detail', (self.slug,))


class PublicManager(Manager):
    """Returns published posts that are not in the future."""
    def published(self):
        return self.get_query_set().filter(status__gte=2, publish__lte=timezone.now())


class Category(models.Model):
    """Blog category model."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:category_detail', (self.slug,))


class Post(models.Model):
    """Blog post model."""
    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publish')
    content = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    publish = models.DateField(default=timezone.now)
    categories = models.ManyToManyField(Category, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    allow_comments = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

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


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.CharField(max_length=63, blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s: %s' % (self.post, self.content[:60])


class SimpleSpamProtection(models.Model):
    question = models.CharField(max_length=255)
    answer = models.IntegerField()

    class Meta:
        verbose_name = 'Spam protection'
        verbose_name_plural = 'Spam protection'
        ordering = ('question',)

    def __unicode__(self):
        return u'%s: %s' % (self.question[:60], self.answer)

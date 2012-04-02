from django.conf.urls import patterns, url

from views import post_list, archive_year, archive_month, post_detail, archive_day

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        post_detail, name='detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        archive_day, name='archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', archive_month, name='archive_month'),
    url(r'^(?P<year>\d{4})/$', archive_year, name='archive_year'),

    url(r'^$', post_list, name="post_list"),
)

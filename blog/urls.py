from django.conf.urls import patterns, url

from views import post_list

urlpatterns = patterns('',
    url(r'^list/$', post_list, name="post_list"),
)

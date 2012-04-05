from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from views import home

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^imperavi/', include('imperavi.urls')),

    url(r'^$', home, name="home"),
    url(r'^ablout/$', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^blog/', include('blog.urls', namespace="blog")),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

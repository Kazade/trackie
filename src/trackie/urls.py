from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from djangae.utils import on_production

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scaffold.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^_ah/', include('djangae.urls')),
    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
)


urlpatterns += patterns('public.views',
    url(r'^$', 'landing', name="landing"),
    url(r'^(?P<project_id>\d+)/$', 'project_home', name="project_home"),
    url(r'^(?P<project_id>\d+)/new/$', 'project_new_issue', name="project_new_issue"),
    url(r'^(?P<project_id>\d+)/(?P<issue_id>\d+)/$', 'project_issue', name="project_issue"),
)


if not on_production():
    urlpatterns += staticfiles_urlpatterns()

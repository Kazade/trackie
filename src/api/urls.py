from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    url(r"v1/projects/$", "project_list", name="projects-list"),
    url(r"v1/(?P<project_id>\d+)/issues/$", "issue_list", name="issues-list")
)

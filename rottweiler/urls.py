# -*- coding: utf-8 -*-

from django.conf.urls import include, patterns, url

from .views import ShowAllRules, ListUrls, ShowPermission

rottweiler_urlpatterns = patterns(
    '',
    url(r'^show-all-rules$', ShowAllRules.as_view(), name="all_rules"),
    url(r'^list-urls$', ListUrls.as_view(), name="all_urls"),
    url(r'^list-urls/(?P<app_label>\w+)/(?P<codename>\w+)/$', 
        ShowPermission.as_view(), 
        name="show_permission"
    ),
)

urlpatterns = patterns(
    '',
    url(r'^', include(rottweiler_urlpatterns, namespace="rottweiler")),
)

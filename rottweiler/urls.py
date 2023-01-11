# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from .views import ShowAllRules, ListUrls, ShowPermission

rottweiler_urlpatterns = [
    url(r'^show-all-rules$', ShowAllRules.as_view(), name="all_rules"),
    url(r'^list-urls$', ListUrls.as_view(), name="all_urls"),
    url(r'^list-urls/(?P<app_label>\w+)/(?P<codename>\w+)/$',
        ShowPermission.as_view(),
        name="show_permission"
    ),
]

urlpatterns = [
    url(r'^', include((rottweiler_urlpatterns, 'rottweiler'), namespace="rottweiler")),
]

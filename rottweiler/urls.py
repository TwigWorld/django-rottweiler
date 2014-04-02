# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import ShowAllRules, ListUrls, ShowPermission

urlpatterns = patterns(
    '',
    url(r'^show-all-rules$', ShowAllRules.as_view(), name="rottweiler_show_all"),
    url(r'^list-urls$', ListUrls.as_view(), name="list_urls"),
    url(r'^list-urls/(?P<app_label>\w+)/(?P<codename>\w+)/$', ShowPermission.as_view(), name="list_perms"),
)

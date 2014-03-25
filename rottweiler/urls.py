# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import ShowAllRules

urlpatterns = patterns(
    '',
    url(r'^show_all_rules$', ShowAllRules.as_view(), name="rottweiler_show_all"),
)

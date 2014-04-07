from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import rottweiler
rottweiler.fetch_permissions()

from project.views import RottyView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'rottweiler/', include('rottweiler.urls')),
    url(r'rottywookieman/$',RottyView.as_view(),name='rotty_wookie'),
)

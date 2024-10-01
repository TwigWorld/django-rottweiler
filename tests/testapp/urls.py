from django.conf.urls import include, url

from django.contrib import admin

admin.autodiscover()

import rottweiler

rottweiler.fetch_permissions()

from project.views import RottyView

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"rottweiler/", include("rottweiler.urls")),
    url(r"rottywookieman/$", RottyView.as_view(), name="rotty_wookie"),
]

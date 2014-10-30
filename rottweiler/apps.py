from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RottweilerConfig(AppConfig):
    name = 'rottweiler'
    verbose_name = _('Rottweiler')

    def ready(self):
        super(RottweilerConfig, self).ready()
        self.module.fetch_permissions()

from django.utils.module_loading import autodiscover_modules

default_app_config = 'rottweiler.apps.RottweilerConfig'


def fetch_permissions():
    autodiscover_modules('permissions')

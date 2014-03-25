def fetch_permissions():
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # try to import the submodule and fail silently if it is
        # not present
        try:
            import_module('%s.permissions' % app)
        # raise the exception if it is not related to the submodule
        # being absent
        except:
            if module_has_submodule(mod, 'permissions'):
                raise

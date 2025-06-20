import importlib
import inspect
import sys

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.contrib.auth.models import Permission
from django.core.exceptions import ViewDoesNotExist
from django.urls import URLPattern
from django.urls import URLResolver

from rulez.registry import registry


def get_all_rules():
    all_rules = []
    for k, v in registry.items():
        class_name = k.__name__
        permissions = []
        for rule_name, rule in v.items():
            definition = "".join(
                inspect.getsourcelines(getattr(rule.model(), rule.field_name))[0][1:]
            )
            permissions.append({"name": rule_name, "definition": definition})

        all_rules.append({"model_name": class_name, "permissions": permissions})

    return all_rules


def find_roles_for_permission(app_label, codename):
    roles = []
    for model_permissions in get_all_rules():
        for permission in model_permissions["permissions"]:
            if permission["name"] == f"{app_label}.{codename}":
                roles.append(permission["definition"])
    return roles


def extract_views_from_urlpatterns(urlpatterns, base=""):
    """
    Return a list of views from a list of urlpatterns.

    Each object in the returned list is a two-tuple: (view_func, regex)
    """
    views = []
    for p in urlpatterns:
        regex_pattern = p.pattern.regex.pattern
        if isinstance(p, URLPattern):
            try:
                views.append((p.callback, base + regex_pattern, p.name))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, URLResolver):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + regex_pattern))
        elif hasattr(p, "_get_callback"):
            try:
                views.append((p._get_callback(), base + regex_pattern, p.name))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, "url_patterns") or hasattr(p, "_get_url_patterns"):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + regex_pattern))
        else:
            raise TypeError(f"{p} does not appear to be a urlpattern object")
    return views


def get_all_views():
    if settings.ADMIN_FOR:
        settings_modules = [__import__(m, {}, {}, [""]) for m in settings.ADMIN_FOR]
    else:
        settings_modules = [settings]
    views = []
    for settings_mod in settings_modules:
        try:
            urlconf = __import__(settings_mod.ROOT_URLCONF, {}, {}, [""])
        except:
            continue
    view_functions = extract_views_from_urlpatterns(urlconf.urlpatterns)
    for func, regex, url_name in view_functions:
        if hasattr(func, "__name__"):
            func_name = func.__name__
            somemodule = importlib.import_module(func.__module__)
            klass = getattr(somemodule, func_name, None)
            if klass and hasattr(klass, "permission_required"):
                try:
                    perm = Permission.objects.get(
                        codename=klass.permission_required.split(".")[1]
                    )
                except:
                    perm = None
                if perm:
                    views.append(
                        {
                            "name": func_name,
                            "module": func.__module__,
                            "permission_codename": perm.codename,
                            "permission_applabel": perm.content_type.app_label,
                            "url": simplify_regex(regex),
                        }
                    )
    return views

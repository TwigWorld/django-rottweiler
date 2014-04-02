import inspect
import importlib

from rulez.registry import registry

from django.conf import settings
from django.core.exceptions import ViewDoesNotExist
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.db.models import Q

from django.views.generic import DetailView, TemplateView


try:
    # 2008-05-30 admindocs found in newforms-admin brand
    from django.contrib.admindocs.views import simplify_regex
    assert simplify_regex
except ImportError:
    # fall back to trunk, pre-NFA merge
    from django.contrib.admin.views.doc import simplify_regex

def extract_views_from_urlpatterns(urlpatterns, base=''):
    """
    Return a list of views from a list of urlpatterns.

    Each object in the returned list is a two-tuple: (view_func, regex)
    """
    views = []
    for p in urlpatterns:
        if isinstance(p, RegexURLPattern):
            try:
                views.append((p.callback, base + p.regex.pattern, p.name))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, RegexURLResolver):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + p.regex.pattern))
        elif hasattr(p, '_get_callback'):
            try:
                views.append((p._get_callback(), base + p.regex.pattern, p.name))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + p.regex.pattern))
        else:
            raise TypeError("%s does not appear to be a urlpattern object" % p)
    return views


class ListUrls(DetailView):
    template_name = 'rottweiler/urls.html'

    def get_object(self, queryset=None):
        if settings.ADMIN_FOR:
            settings_modules = [__import__(m, {}, {}, ['']) for m in settings.ADMIN_FOR]
        else:
            settings_modules = [settings]

        views = []
        for settings_mod in settings_modules:
            try:
                urlconf = __import__(settings_mod.ROOT_URLCONF, {}, {}, [''])
            except:
                continue
        view_functions = extract_views_from_urlpatterns(urlconf.urlpatterns)

        for (func, regex, url_name) in view_functions:
            if hasattr(func, '__name__'):
                func_name = func.__name__
                somemodule = importlib.import_module(func.__module__)
                klass = getattr(somemodule, func_name, None)
                if klass and hasattr(klass, 'permission_required'):
                    try:
                        perm = Permission.objects.get(codename=klass.permission_required.split('.')[1])
                    except:
                        perm = None

                    if perm:
                        views.append({
                            'name': func_name,
                            'module': func.__module__,
                            'permission_codename': perm.codename,
                            'permission_applabel': perm.content_type.app_label,
                            'url': simplify_regex(regex),
                        })

        return views


class ShowPermission(TemplateView):
    template_name = 'rottweiler/permission.html'

    def get_context_data(self, **kwargs):
        context_data = super(ShowPermission, self).get_context_data(**kwargs)
        context_data['user_groups'] = Group.objects.filter(
            Q(permissions__codename=kwargs['codename'])).distinct()
        context_data['users'] = get_user_model().objects.filter(
            Q(user_permissions__codename=kwargs['codename'])
            ).distinct()

        for k, v in registry.iteritems():
            for rule_name, rule in v.iteritems():
                definition = "".join(
                    inspect.getsourcelines(
                        getattr(rule.model(), rule.field_name))[0][1:])
                if rule_name == "%s.%s" % (kwargs['app_label'],kwargs['codename']):
                    context_data['role'] = definition

        return context_data


class ShowAllRules(DetailView):
    template_name = 'rottweiler/index.html'

    def get_object(self, queryset=None):
        if not self.request.user.is_superuser:
            raise PermissionDenied

        all_rules = []

        for k, v in registry.iteritems():
            class_name = k.__name__
            permissions = []
            for rule_name, rule in v.iteritems():
                definition = "".join(
                    inspect.getsourcelines(
                        getattr(rule.model(), rule.field_name))[0][1:])
                permissions.append({'name': rule_name,
                                    'definition': definition})

            all_rules.append({'model_name': class_name,
                              'permissions': permissions})

        return all_rules

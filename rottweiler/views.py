from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  Group
from django.db.models import Q
from django.views.generic import TemplateView

from .view_helpers import (
    get_all_rules,
    get_all_views,
    find_roles_for_permission,
)


class SuperUserOnly(object):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return  super(SuperUserOnly, self).get(request, *args, **kwargs)


class ListUrls(SuperUserOnly, TemplateView):
    template_name = 'rottweiler/urls.html'

    def get_context_data(self, **kwargs):
        context_data = super(ListUrls, self).get_context_data(**kwargs)
        context_data['object'] = get_all_views()

        return context_data


class ShowPermission(SuperUserOnly, TemplateView):
    template_name = 'rottweiler/permission.html'

    def get_context_data(self, **kwargs):
        context_data = super(ShowPermission, self).get_context_data(**kwargs)

        context_data['user_groups'] = Group.objects.filter(
                Q(permissions__codename=kwargs['codename'])
            ).distinct()
        context_data['users'] = get_user_model().objects.filter(
                Q(user_permissions__codename=kwargs['codename'])
            ).distinct()
        context_data['roles'] = find_roles_for_permission(kwargs['app_label'], kwargs['codename'])

        return context_data


class ShowAllRules(SuperUserOnly, TemplateView):
    template_name = 'rottweiler/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(ShowAllRules, self).get_context_data(**kwargs)
        context_data['object'] = get_all_rules()

        return context_data

import inspect

from rulez import registry

from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView


class ShowAllRules(DetailView):
    template_name = 'rottweiler/index.html'

    def get_object(self, queryset=None):
        if not self.request.user.is_superuser:
            raise PermissionDenied

        all_rules = []

        for k,v in registry.registry.iteritems():
            class_name = k.__name__
            permissions = []
            for rule_name, rule in v.iteritems():
                definition = "".join(inspect.getsourcelines(getattr(rule.model(),rule.field_name))[0][1:])
                permissions.append({'name': rule_name, 'definition': definition})

            all_rules.append({'model_name': class_name, 'permissions': permissions})

        return all_rules

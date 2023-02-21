from django.test import TestCase
from django.template import Template, Context

from django.contrib.auth import get_user_model

from rottweiler import registry
from .stubs import ModelStub


def positive_permission(self, user):
    return True


def negative_permission(self, user):
        return False


class TestRottweilerPerms(TestCase):
    User = get_user_model()
    def test_user_has_permissions_against_model_instance(self):
        registry.register('positive_permission',
                          positive_permission,
                          ModelStub)
        user = self.User()
        user.save()
        context = Context({'user': user, 'object': ModelStub()})
        template = Template("""
            {% load rottweiler_tags %}
            {% rottweiler_perms positive_permission object as can_access %}
        """)
        template.render(context)
        self.assertTrue(context['can_access'])

    def test_user_does_not_have_permissions_against_model_instance(self):
        registry.register('negative_permission',
                          negative_permission,
                          ModelStub)
        user = self.User()
        user.save()
        context = Context({'user': user, 'object': ModelStub()})
        template = Template("""
            {% load rottweiler_tags %}
            {% rottweiler_perms negative_permission object as can_access %}
        """)
        template.render(context)
        self.assertFalse(context['can_access'])

    def test_user_has_global_permissions(self):
        registry.register('positive_permission',
                          positive_permission)
        user = self.User()
        user.save()
        context = Context({'user': user})
        template = Template("""
            {% load rottweiler_tags %}
            {% rottweiler_perms positive_permission as can_access %}
        """)
        template.render(context)
        self.assertTrue(context['can_access'])

    def test_user_does_not_have_global_permissions(self):
        registry.register('negative_permission',
                          negative_permission)
        user = self.User()
        user.save()
        context = Context({'user': user})
        template = Template("""
            {% load rottweiler_tags %}
            {% rottweiler_perms negative_permission as can_access %}
        """)
        template.render(context)
        self.assertFalse(context['can_access'])

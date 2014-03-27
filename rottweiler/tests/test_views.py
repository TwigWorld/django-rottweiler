from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory

from rottweiler import registry
from rottweiler.views import ShowAllRules
from .stubs import ModelStub


def first_permission(self, user):
    return user.is_superuser or user.is_staff


def second_permission(self, user):
    return user.is_active


class TestShowAllRulesView(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.request.method = 'GET'

    def test_access_denied_if_user_is_not_superuser(self):
        self.request.user = User(is_superuser=False)
        view = ShowAllRules.as_view()
        with self.assertRaises(PermissionDenied):
            view(self.request)

    def test_returns_200_if_user_is_superuser(self):
        self.request.user = User(is_superuser=True)
        view = ShowAllRules.as_view()
        response = view(self.request)
        self.assertEqual(200, response.status_code)

    def test_assigns_list_of_all_rules_to_object(self):
        registry.register('first_permission', first_permission, ModelStub)
        registry.register('second_permission', second_permission, ModelStub)
        self.request.user = User(is_superuser=True)
        view = ShowAllRules.as_view()
        response = view(self.request)
        model_stub_rule = None
        for rule in response.context_data['object']:
            if rule['model_name'] == 'ModelStub':
                model_stub_rule = rule
                break
        self.assertTrue(model_stub_rule)
        self.assertTrue({'name': 'first_permission',
                         'definition': '    return user.is_superuser or user.is_staff\n'} in
                        model_stub_rule['permissions'])
        self.assertTrue({'name': 'second_permission',
                         'definition': '    return user.is_active\n'} in
                        model_stub_rule['permissions'])

from django.test import TestCase

from django.contrib.auth.models import User

from rottweiler import registry
from rottweiler.backends import PermissionBackend
from .stubs import ModelStub


def test_global_permission(self, user):
    return user.is_superuser


def test_object_permission(self, user):
    return self.return_value


registry.register('test_permission', test_global_permission)
registry.register('test_permission', test_object_permission, ModelStub)


class TestBackends(TestCase):
    def test_user_is_checked_for_global_permission(self):
        user = User(is_active=True, is_superuser=True)
        backend = PermissionBackend()
        self.assertTrue(backend.has_perm(user, 'test_permission'))

    def test_user_is_checked_for_object_permission(self):
        user = User(is_active=True, is_superuser=False)
        backend = PermissionBackend()
        self.assertTrue(backend.has_perm(user, 'test_permission', ModelStub()))

    def test_returns_false_if_rule_does_not_exist(self):
        user = User(is_active=True, is_superuser=True)
        backend = PermissionBackend()
        self.assertFalse(backend.has_perm(user, 'absent_permission'))

    def test_inactive_user_has_no_permissions(self):
        user = User(is_active=False, is_superuser=True)
        backend = PermissionBackend()
        self.assertFalse(backend.has_perm(user, 'test_permission'))

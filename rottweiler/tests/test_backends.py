from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from rottweiler import registry
from rottweiler.backends import PermissionBackend
from .stubs import ModelStub


def dummy_global_permission(self, user):
    return user.is_staff


def dummy_object_permission(self, user):
    return self.return_value


registry.register("test_app.test_permission", dummy_global_permission)
registry.register("test_app.test_permission", dummy_object_permission, ModelStub)


class TestBackends(TestCase):
    User = get_user_model()

    def test_user_is_checked_for_global_rule_permission(self):
        user = self.User(is_active=True, is_staff=True)
        user.save()
        backend = PermissionBackend()
        self.assertTrue(backend.has_perm(user, "test_app.test_permission"))

    def test_user_is_checked_for_global_db_permission(self):
        user = self.User(is_active=True)
        user.save()
        content_type = ContentType(app_label="test_app")
        content_type.save()
        permission = Permission(content_type=content_type, codename="test_permission")
        permission.save()
        user.user_permissions.add(permission)
        backend = PermissionBackend()
        self.assertTrue(backend.has_perm(user, "test_app.test_permission"))

    def test_user_is_checked_for_object_rule_permission(self):
        user = self.User(is_active=True, is_staff=False)
        user.save()
        backend = PermissionBackend()
        self.assertTrue(backend.has_perm(user, "test_app.test_permission", ModelStub()))

    def test_returns_false_if_rule_does_not_exist(self):
        user = self.User(is_active=True, is_staff=True)
        user.save()
        backend = PermissionBackend()
        self.assertFalse(backend.has_perm(user, "test_app.absent_permission"))

    def test_inactive_user_has_no_permissions(self):
        user = self.User(is_active=False, is_staff=True)
        user.save()
        backend = PermissionBackend()
        self.assertFalse(backend.has_perm(user, "test_app.test_permission"))

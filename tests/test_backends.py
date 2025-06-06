from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import pytest

from rottweiler import registry
from rottweiler.backends import PermissionBackend


def dummy_global_permission(self, user):
    return user.is_staff


def dummy_object_permission(self, user):
    return self.return_value


registry.register("test_app.test_permission", dummy_global_permission)


@pytest.mark.django_db
def test_user_is_checked_for_global_rule_permission():
    user = User(is_active=True, is_staff=True)
    user.save()
    backend = PermissionBackend()
    assert backend.has_perm(user, "test_app.test_permission") is True


@pytest.mark.django_db
def test_user_is_checked_for_global_db_permission():
    user = User(is_active=True)
    user.save()
    content_type = ContentType(app_label="test_app")
    content_type.save()
    permission = Permission(content_type=content_type, codename="test_permission")
    permission.save()
    user.user_permissions.add(permission)
    backend = PermissionBackend()
    assert backend.has_perm(user, "test_app.test_permission") is True


@pytest.mark.django_db
def test_user_is_checked_for_object_rule_permission(mock_model_stub):
    registry.register(
        "test_app.test_permission", dummy_object_permission, mock_model_stub
    )
    user = User(is_active=True, is_staff=False)
    user.save()
    backend = PermissionBackend()
    assert backend.has_perm(user, "test_app.test_permission", mock_model_stub()) is True


@pytest.mark.django_db
def test_returns_false_if_rule_does_not_exist():
    user = User(is_active=True, is_staff=True)
    user.save()
    backend = PermissionBackend()
    assert backend.has_perm(user, "test_app.absent_permission") is False


@pytest.mark.django_db
def test_inactive_user_has_no_permissions():
    user = User(is_active=False, is_staff=True)
    user.save()
    backend = PermissionBackend()
    assert backend.has_perm(user, "test_app.test_permission") is False

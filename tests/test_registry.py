from django.contrib.auth.models import User

import pytest

from rottweiler import registry


def dummy_permission(user):
    return True


@pytest.mark.django_db
def test_add_object_permission(mock_model_stub):
    registry.register("test_permission", dummy_permission, mock_model_stub)
    user = User()
    user.save()
    assert user.has_perm("test_permission", mock_model_stub()) is True


@pytest.mark.django_db
def test_add_global_permission():
    registry.register("test_permission", dummy_permission)
    user = User()
    user.save()
    assert user.has_perm("test_permission") is True

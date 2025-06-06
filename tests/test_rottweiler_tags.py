from django.template import Template, Context
from django.contrib.auth.models import User

import pytest

from rottweiler import registry


def positive_permission(user):
    return True


def negative_permission(user):
    return False


@pytest.mark.django_db
def test_user_has_permissions_against_model_instance(mock_model_stub):
    registry.register("positive_permission", positive_permission, mock_model_stub)
    user = User()
    user.save()
    context = Context({"user": user, "object": mock_model_stub()})
    template = Template(
        """
        {% load rottweiler_tags %}
        {% rottweiler_perms positive_permission object as can_access %}
    """
    )
    template.render(context)
    assert context["can_access"] is True


@pytest.mark.django_db
def test_user_does_not_have_permissions_against_model_instance(mock_model_stub):
    registry.register("negative_permission", negative_permission, mock_model_stub)
    user = User()
    user.save()
    context = Context({"user": user, "object": mock_model_stub()})
    template = Template(
        """
        {% load rottweiler_tags %}
        {% rottweiler_perms negative_permission object as can_access %}
    """
    )
    template.render(context)
    assert context["can_access"] is False


@pytest.mark.django_db
def test_user_has_global_permissions():
    registry.register("positive_permission", positive_permission)
    user = User()
    user.save()
    context = Context({"user": user})
    template = Template(
        """
        {% load rottweiler_tags %}
        {% rottweiler_perms positive_permission as can_access %}
    """
    )
    template.render(context)
    assert context["can_access"] is True


@pytest.mark.django_db
def test_user_does_not_have_global_permissions():
    registry.register("negative_permission", negative_permission)
    user = User()
    user.save()
    context = Context({"user": user})
    template = Template(
        """
        {% load rottweiler_tags %}
        {% rottweiler_perms negative_permission as can_access %}
    """
    )
    template.render(context)
    assert context["can_access"] is False

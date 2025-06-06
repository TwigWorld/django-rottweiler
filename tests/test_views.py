from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

import pytest

from rottweiler import registry
from rottweiler.views import ShowAllRules


def first_permission(self, user):
    return user.is_superuser or user.is_staff


def second_permission(self, user):
    return user.is_active


def test_access_denied_if_user_is_not_superuser(rf):
    request = rf.get("show-all-rules")
    request.user = User(is_superuser=False)
    view = ShowAllRules.as_view()
    with pytest.raises(PermissionDenied):
        view(request)

def test_returns_200_if_user_is_superuser(rf, admin_user):
    request = rf.get("show-all-rules")
    request.user = admin_user
    view = ShowAllRules.as_view()
    response = view(request)
    assert response.status_code == 200


def test_assigns_list_of_all_rules_to_object(rf, admin_user, mock_model_stub):
    registry.register("first_permission", first_permission, mock_model_stub)
    registry.register("second_permission", second_permission, mock_model_stub)
    request = rf.get("show-all-rules")
    request.user = admin_user
    view = ShowAllRules.as_view()
    response = view(request)
    model_stub_rule = None
    for rule in response.context_data["object"]:
        if rule["model_name"] == "ModelStub":
            model_stub_rule = rule
            break
    assert {
        "name": "first_permission",
        "definition": "    return user.is_superuser or user.is_staff\n",
    } in model_stub_rule["permissions"]
    assert {
        "name": "second_permission",
        "definition": "    return user.is_active\n",
    } in model_stub_rule["permissions"]

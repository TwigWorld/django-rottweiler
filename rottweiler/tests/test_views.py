from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from mock import Mock
from mock import patch

from rottweiler import registry
from rottweiler.views import ListUrls
from rottweiler.views import ShowAllRules
from rottweiler.views import ShowPermission

from .stubs import ModelStub


def first_permission(self, user):
    return user.is_superuser or user.is_staff


def second_permission(self, user):
    return user.is_active


class TestShowPermissionView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("list-urls/project/barkbark/")

    @patch("rottweiler.views.get_user_model")
    @patch("rottweiler.views.Group")
    def test_show_permission(self, group_filter, user_filter):
        url = reverse("rottweiler:all_rules")
        self.request.user = User(is_superuser=True)
        view = ShowPermission.as_view()

        response = view(self.request, codename="change_user", app_label="project")

        assert (
            response.context_data["users"] == user_filter().objects.filter().distinct()
        )

        assert (
            response.context_data["user_groups"]
            == group_filter.objects.filter().distinct()
        )
        assert response.context_data["roles"] == [
            "    return True\n",
            "    return True\n",
        ]
        assert 200 == response.status_code


class TestShowAllUrlsView(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.request.method = "GET"

    @patch("rottweiler.view_helpers.Permission.objects.get")
    def test_list_all_urls(self, permission_get):
        permission_get.return_value = Mock(
            codename="lala.lalala", content_type=Mock(app_label="lala")
        )
        self.request.user = User(is_superuser=True)
        view = ListUrls.as_view()

        response = view(self.request)

        assert response.context_data["object"] == [
            {
                "module": "project.views",
                "name": "RottyView",
                "permission_applabel": "lala",
                "permission_codename": "lala.lalala",
                "url": "/rottywookieman/",
            }
        ]

        assert 200 == response.status_code


class TestShowAllRulesView(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.request.method = "GET"

    def test_access_denied_if_user_is_not_superuser(self):
        self.request.user = User(is_superuser=False)
        view = ShowAllRules.as_view()
        with self.assertRaises(PermissionDenied):
            view(self.request)

    def test_returns_200_if_user_is_superuser(self):
        self.request.user = User(is_superuser=True)
        view = ShowAllRules.as_view()
        response = view(self.request)
        assert 200 == response.status_code

    def test_assigns_list_of_all_rules_to_object(self):
        registry.register("first_permission", first_permission, ModelStub)
        registry.register("second_permission", second_permission, ModelStub)
        self.request.user = User(is_superuser=True)
        view = ShowAllRules.as_view()
        response = view(self.request)
        model_stub_rule = None
        for rule in response.context_data["object"]:
            if rule["model_name"] == "ModelStub":
                model_stub_rule = rule
                break
        self.assertTrue(model_stub_rule)
        self.assertTrue(
            {
                "name": "first_permission",
                "definition": "    return user.is_superuser or user.is_staff\n",
            }
            in model_stub_rule["permissions"]
        )
        self.assertTrue(
            {"name": "second_permission", "definition": "    return user.is_active\n"}
            in model_stub_rule["permissions"]
        )

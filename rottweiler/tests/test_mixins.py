from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, RequestFactory

from mock import patch
from rottweiler.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ModifiedRequestFactory(RequestFactory):
    def build_absolute_uri(self):
        return ""

    def get_full_path(self):
        return ""


class BaseView(object):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse()


class LoginView(LoginRequiredMixin, BaseView):
    pass


class PermissionView(PermissionRequiredMixin, BaseView):
    permission_required = "test_permission"

    def get_restricted_object(self):
        return "object"


class TestLoginRequiredMixin(TestCase):
    def test_the_user_is_redirected_if_not_logged_in(self):
        request = ModifiedRequestFactory()
        request.user = AnonymousUser()
        view = LoginView()
        response = view.dispatch(request)
        self.assertEqual("HttpResponseRedirect", response.__class__.__name__)

    def test_the_user_gets_through_if_they_are_logged_in(self):
        request = ModifiedRequestFactory()
        request.user = User()
        view = LoginView()
        response = view.dispatch(request)
        self.assertEqual("HttpResponse", response.__class__.__name__)


class TestPermissionRequiredMixin(TestCase):
    def test_the_user_is_redirected_if_not_logged_in(self):
        request = ModifiedRequestFactory()
        request.user = AnonymousUser()
        view = PermissionView()
        response = view.dispatch(request)
        self.assertEqual("HttpResponseRedirect", response.__class__.__name__)

    @patch("django.contrib.auth.models.User.has_perm")
    def test_user_denied_access_if_they_do_not_have_permission(self, has_perm):
        has_perm.return_value = False
        request = ModifiedRequestFactory()
        request.user = User()
        view = PermissionView()
        with self.assertRaises(PermissionDenied):
            view.dispatch(request)
        has_perm.assert_any_call("test_permission", "object")

    @patch("django.contrib.auth.models.User.has_perm")
    def test_user_given_access_if_they_have_permission(self, has_perm):
        has_perm.return_value = True
        request = ModifiedRequestFactory()
        request.user = User()
        view = PermissionView()
        response = view.dispatch(request)
        self.assertEqual("HttpResponse", response.__class__.__name__)
        has_perm.assert_called_with("test_permission", "object")

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from rottweiler.mixins import LoginRequiredMixin


class ModifiedRequestFactory(RequestFactory):
    def build_absolute_uri(self):
        return ''

    def get_full_path(self):
        return ''


class LoginView(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class TestLoginRequiredMixin(TestCase):
    def test_the_user_is_redirected_if_not_logged_in(self):
        request = ModifiedRequestFactory()
        request.user = AnonymousUser()
        view = LoginView()
        response = view.dispatch(request)
        self.assertEqual('HttpResponseRedirect', response.__class__.__name__)

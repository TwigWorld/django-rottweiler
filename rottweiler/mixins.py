from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permissions.

    View can select which object to check permissions against by
    overriding the get_restricted_object() function.

    Settings:

    Example Usage:

        class SomeView(PermissionsRequiredMixin, ListView):
            ...
            permission_required = 'permission_a'
            ...
    """
    permission_required = ''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_restricted_object()

        if (
            not request.user.has_perm(self.permission_required, obj) and
            not request.user.has_perm(self.permission_required)
        ):
            raise PermissionDenied
        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def get_restricted_object(self):
        try:
            return (hasattr(self, 'get_object') and self.get_object()
                    or getattr(self, 'object', None))
        except AttributeError:
            return None

from django.contrib.auth.backends import ModelBackend
from rulez.backends import ObjectPermissionBackend
from .global_permission import GlobalPermission


class PermissionBackend(object):
    """
    Backend that checks whether a user has permissions against a model
    instance or otherwise checks whether they have global permissions.
    """
    def has_perm(self, user_obj, perm, obj=None):
        if ModelBackend().has_perm(user_obj, perm):
            return True

        if obj is None:
            obj = GlobalPermission()

        return ObjectPermissionBackend().has_perm(user_obj, perm, obj)

    def authenticate(self, username=None, password=None):
        return None

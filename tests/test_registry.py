from django.test import TestCase

from django.contrib.auth import get_user_model
from rottweiler import registry
from .stubs import ModelStub


def test_permission():
    return True


class TestRegistry(TestCase):
    User = get_user_model()
    def test_add_object_permission(self):
        registry.register('test_permission', test_permission, ModelStub)
        user = self.User()
        user.save()
        self.assertTrue(user.has_perm('test_permission', ModelStub()))

    def test_add_global_permission(self):
        registry.register('test_permission', test_permission)
        user = self.User()
        user.save()
        self.assertTrue(user.has_perm('test_permission'))

from django.test import TestCase

from customuser.tests.factories import UserFactory
from rottweiler import registry
from .stubs import ModelStub


def test_permission(self, user):
    return True


class TestRegistry(TestCase):
    def test_add_object_permission(self):
        registry.register('test_permission', test_permission, ModelStub)
        user = UserFactory()
        self.assertTrue(user.has_perm('test_permission', ModelStub()))

    def test_add_global_permission(self):
        registry.register('test_permission', test_permission)
        user = UserFactory()
        self.assertTrue(user.has_perm('test_permission'))

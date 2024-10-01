from rottweiler import registry
from django.contrib.auth import get_user_model


def change_user(self, user):
    return True


registry.register("project.change_user", change_user)
registry.register("project.change_user", change_user, get_user_model())

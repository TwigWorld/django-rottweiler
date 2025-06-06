from django.conf import settings

import pytest


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "rottweiler",
        ],
        ROOT_URLCONF="rottweiler.urls",
        AUTHENTICATION_BACKENDS=[
            "rottweiler.backends.PermissionBackend",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
    )


class ModelStub(object):
    def __init__(self, return_value=True):
        self.return_value = return_value

    @classmethod
    def add_to_class(cls, name, value):
        if hasattr(value, "contribute_to_class"):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


@pytest.fixture(scope="session")
def mock_model_stub():
    return ModelStub

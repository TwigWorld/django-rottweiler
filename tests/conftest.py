import django
import pytest

@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass

@pytest.fixture(scope='session')
def django_db_use_migrations():
    return False

@pytest.fixture(scope='session')
def django_db_keepdb():
    return False

def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
        ),
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        SITE_ID=1,
        SECRET_KEY='test',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='test_rottweiler.testapp.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    "debug": True,  # We want template errors to raise
                }
            },
        ],
        MIDDLEWARE=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'test_rottweiler.testapp.project',
            'rottweiler',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        ADMIN_FOR = []
    )
    django.setup()
import os

from setuptools import find_packages
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

PACKAGE_DATA = list()
for root, dirs, files in os.walk(os.path.join("rottweiler", "templates")):
    for filename in files:
        PACKAGE_DATA.append(f"{root[len('rottweiler') + 1 :]}/{filename}")

setup(
    name="django-rottweiler",
    version="2.1.0",
    packages=find_packages(),
    package_data={"": PACKAGE_DATA},
    license="MIT License",
    description="""A permission model that allows global and object-level
                 rule-based permissions""",
    url="https://github.com/TwigWorld/django-rottweiler",
    long_description=README,
    author="Charlie Quinn & Chris Wright",
    install_requires=[
        "Django<3",
        "django-rulez@git+https://github.com/TwigWorld/django-rulez.git@2.0.0#egg=django-rulez",
    ],
    extras_require={
        "testing": [
            "mock",
            "pytest",
            "pytest-django",
            "black",
            "isort",
            "pre-commit",
            "check_pdb_hook",
        ]
    },
)

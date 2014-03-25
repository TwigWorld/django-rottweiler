import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__),
                           'README.md')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),
                                       os.pardir)))

setup(
    name='django-rottweiler',
    version='0.1',
    packages=['rottweiler'],
    license='MIT License',
    description='''A permission model that allows global and object-level
                 rule-based permissions''',
    url='https://github.com/TwigWorld/django-rottweiler',
    long_description=README,
    author='Charlie Quinn & Chris Wright',
    install_requires=["Django >= 1.4", "django-rulez == 1.0.1"]
)

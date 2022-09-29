import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__),
                           'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),
                                       os.pardir)))

PACKAGE_DATA = list()
for root, dirs, files in os.walk(os.path.join('rottweiler', 'templates')):
    for filename in files:
        PACKAGE_DATA.append("%s/%s" % (root[len('rottweiler')+1:], filename))

setup(
    name='django-rottweiler',
    version='2.0.0',
    packages=find_packages(),
    package_data={'': PACKAGE_DATA},
    license='MIT License',
    description='''A permission model that allows global and object-level
                 rule-based permissions''',
    url='https://github.com/TwigWorld/django-rottweiler',
    long_description=README,
    author='Charlie Quinn & Chris Wright',
    python_requires='>=2.7.0',
    install_requires=[
        "Django>=1.11, <2.0",
        "django-rulez@git+https://github.com/chrisglass/django-rulez.git@0f869f330a7e50aacf953265e1ce16ada16cb98a#egg=django-rulez-1.0.2",
    ],
)

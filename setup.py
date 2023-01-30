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
    python_requires='>=3.7.0',
    install_requires=[
        "Django>=2.2, <3.2",
        "django-rulez@git+https://github.com/TwigWorld/django-rulez.git@547b246e7531df260828381598f30ad01125b4a5#egg=django-rulez-1.0.2",
    ],
)

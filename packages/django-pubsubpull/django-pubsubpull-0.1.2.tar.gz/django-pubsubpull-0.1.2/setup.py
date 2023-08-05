import os
from setuptools import setup
import sys

def read(fname1, fname2):
    if os.path.exists(fname1):
        fname = fname1
    else:
        fname = fname2
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name = "django-pubsubpull",
    version = "0.1.2",
    author = "Kirit Saelensminde",
    author_email = "kirit@felspar.com",
    url='https://github.com/KayEss/django-pubsubpull',
    description = ("Pub/sub and pull for Django"),
    long_description = read('README','README.md'),
    license = "Boost Software License - Version 1.0 - August 17th, 2003",
    keywords = "django rest data pub-sub pull",
    packages = [
        'pubsubpull', 'pubsubpull.operations', 'pubsubpull.tests',
        'pubsubpull.migrations', 'pubsubpull.south_migrations'],
    package_data ={'pubsubpull': ['*.sql']},
    install_requires = ['django-async'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved",
    ],
    **extra
)

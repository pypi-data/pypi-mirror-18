#!/usr/bin/env python
#
# Copyright (c) 2011-2013 Ivan Zakrevsky
# Licensed under the terms of the BSD License (see LICENSE.txt)
import os.path
from setuptools import setup, find_packages

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

setup(
    name = app_name,
    version = '0.7.7.40',

    packages = find_packages(),
    include_package_data=True,

    author = "Ivan Zakrevsky",
    author_email = "ivzak@yandex.ru",
    description = "Project has been moved to https://pypi.python.org/pypi/cache-dependencies",
    long_description="Project has been moved to https://pypi.python.org/pypi/cache-dependencies",
    license = "BSD License",
    keywords = "django cache tagging",
    tests_require = [
        'Django>=1.3',
        'mock',
    ],
    test_suite = 'runtests.main',
    classifiers = [
        'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url = "https://pypi.python.org/pypi/cache-dependencies",
)

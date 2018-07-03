#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = []

SETUP_REQUIREMENTS = ['pytest-runner', ]

TEST_REQUIREMENTS = [
    'alabaster==0.7.10',
    'argh==0.26.2',
    'astroid==1.6.2',
    'attrs==17.4.0',
    'babel==2.5.3',
    'bumpversion==0.5.3',
    'certifi==2018.1.18',
    'chardet==3.0.4',
    'coverage==4.5.1',
    'docutils==0.14',
    'idna==2.6',
    'imagesize==1.0.0',
    'isort==4.3.4',
    'jinja2==2.10',
    'lazy-object-proxy==1.3.1',
    'markupsafe==1.0',
    'mccabe==0.6.1',
    'packaging==17.1',
    'pathtools==0.1.2',
    'pkginfo==1.4.2',
    'pluggy==0.6.0',
    'py==1.5.3',
    'pycodestyle==2.3.1',
    'pyflakes==1.6.0',
    'pygments==2.2.0',
    'pylint==1.8.3',
    'pyparsing==2.2.0',
    'pytest-cov==2.5.1',
    'pytest-pylint==0.9.0',
    'pytest-runner==2.11.1',
    'pytest==3.4.2',
    'pytz==2018.3',
    'pyyaml==3.12',
    'requests-toolbelt==0.8.0',
    'requests==2.18.4',
    'six==1.11.0',
    'snowballstemmer==1.2.1',
    'sphinx==1.7.1',
    'sphinxcontrib-websupport==1.0.1',
    'tox==2.9.1',
    'tqdm==4.19.9',
    'twine==1.10.0',
    'urllib3==1.22',
    'watchdog==0.8.3',
    'wrapt==1.10.11',
    "virtualenv==15.2.0; python_version != '3.2'",
]

setup(
    author="Walter Danilo Galante",
    author_email='walterdangalante@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Minimal environment variables reader",
    install_requires=REQUIREMENTS,
    license="MIT license",
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords='envi',
    name='envi',
    packages=find_packages(include=['envi']),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    url='https://github.com/OvalMoney/envi',
    version='0.1.0',
    zip_safe=False,
)

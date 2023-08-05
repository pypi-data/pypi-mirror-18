#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup

with open('README.rst', 'r') as fp:
    readme = fp.read()

with open('HISTORY.rst', 'r') as fp:
    history = fp.read().replace('.. :changelog:', '')

with open('requirements.txt', 'r') as fp:
    requirements = list(filter(bool, (line.strip() for line in fp)))

with open('requirements-dev.txt', 'r') as fp:
    dev_requirements = list(filter(bool, (line.strip() for line in fp)))

# Require pytest-runner only when running tests
pytest_runner = (['pytest-runner>=2.0,<3dev']
                 if any(arg in sys.argv for arg in ('pytest', 'test'))
                 else [])

setup_requires = pytest_runner

setup(
    name='scikit-ci-addons',

    version='0.2.0',

    author='The scikit-build team',
    author_email='scikit-build@googlegroups.com',

    url='https://github.com/scikit-build/scikit-ci-addons',

    description='scikit-ci-addons is a command line tool and a set of scripts'
                ' useful to install prerequisites for building Python extension'
                ' on CI services.',
    long_description=readme + '\n\n' + history,

    entry_points={'console_scripts': ['ci_addons=ci_addons.__main__:main']},

    packages=['anyci', 'appveyor', 'ci_addons', 'circle', 'travis'],
    package_data={'anyci': ['*.sh'], 'appveyor': ['*.cmd'], 'travis': ['*.sh']},
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Build Tools'
    ],

    license="Apache",

    keywords='CI Appveyor CircleCI Travis',

    setup_requires=setup_requires,
    install_requires=requirements,
    tests_require=dev_requirements,
)

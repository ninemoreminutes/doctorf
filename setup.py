#!/usr/bin/env python

# Python
import os
import sys

# Setuptools
from setuptools import setup, find_packages

# Doctor F
from doctorf import __version__

tests_require = [
    'Django>=1.7',
    'django-hotrunner>=0.2.2',
    'django-setuptest>=0.1.4',
    'djangorestframework',
]
try:
    import argparse
except ImportError:
    tests_require.append('argparse')

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    #extra['convert_2to3_doctests'] = ['src/your/module/README.txt']
    #extra['use_2to3_fixers'] = ['your.fixers']

setup(
    name='doctorf',
    version=__version__,
    author='Nine More Minutes, Inc.',
    author_email='support@ninemoreminutes.com',
    description='Extra utilities and mixins for Django REST Framework (DRF).',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'),
                          'rb').read().decode('utf-8'),
    license='BSD',
    keywords='django rest framework',
    url='https://github.com/ninemoreminutes/doctorf/',
    packages=find_packages(exclude=['test_project', 'test_app']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.7',
        'djangorestframework>=3',
        'drf-extensions',
    ],
    setup_requires=[],
    #tests_require=tests_require,
    #test_suite='test_suite.TestSuite',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
    options={
        'egg_info': {
            'tag_build': '.dev',
        },
        'aliases': {
            'dev_build': 'egg_info sdist',
            'release_build': 'egg_info -b "" -R sdist',
        },
    },
    **extra
)

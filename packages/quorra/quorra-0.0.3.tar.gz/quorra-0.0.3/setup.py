#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package setup
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# config
# ------
import quorra
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# requirements
# ------------
with open('requirements.txt', 'r') as reqs:
    requirements = reqs.readlines()

test_requirements = [
    'nose',
    'nose-parameterized'
]


# files
# -----
with open('README.rst') as fi:
    readme = fi.read()


# exec
# ----
setup(
    name='quorra',
    version=quorra.__version__,
    description='A python extension for generating quorra.js plots directly from python',
    long_description=readme,
    author='Blake Printy',
    author_email='bprinty@gmail.com',
    url='https://github.com/bprinty/quorra',
    packages=['quorra'],
    package_data={'quorra': ['tmpl/*.html']},
    package_dir={'quorra': 'quorra'},
    # entry_points={
    #     'console_scripts': [
    #         'quorra = quorra.__main__:main'
    #     ]
    # },
    include_package_data=True,
    install_requires=requirements,
    license='Apache-2.0',
    zip_safe=False,
    keywords=['quorra', 'visualization', 'plotting', 'charts', 'data'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apple Public Source License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)

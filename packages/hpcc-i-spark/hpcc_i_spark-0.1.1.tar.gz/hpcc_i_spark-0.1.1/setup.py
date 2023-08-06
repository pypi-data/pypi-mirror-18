#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'ujson',
    'xmltodict',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='hpcc_i_spark',
    version='0.1.1',
    description="This package can be used to connect to any hpcc cluster and use the data",
    long_description=readme + '\n\n' + history,
    author="Vivek Nair",
    author_email='vivekaxl@gmail.com',
    url='https://github.com/vivekaxl/hpcc_i_spark',
    packages=['hpcc_i_spark'],

    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='hpcc_converter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)


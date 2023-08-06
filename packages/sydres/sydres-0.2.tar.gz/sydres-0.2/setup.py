#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for redsys client.
"""

from setuptools import setup

PACKAGES = ['sydres', ]
PACKAGES_DATA = {'sydres.tests': []}

setup(name='sydres',
    description='A client to submit payment orders to the Redsys service.',
    author='Alex Barcelo',
    author_email='alex.barcelo@gmail.com',
    url="https://github.com/alexbarcelo/sydres",
    version='0.2',
    license='General Public Licence 3',
    provides=['sydres'],
    install_requires=['pycrypto',],
    packages=PACKAGES,
    package_data=PACKAGES_DATA,
    scripts=[],
    test_suite='sydres.tests',
)

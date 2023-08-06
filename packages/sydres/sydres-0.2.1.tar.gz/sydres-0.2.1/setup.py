"""
Sydres
======

Sydres is a Redsys Client, fork of python-redsys. Original project is available
at https://bitbucket.org/zikzakmedia/python-redsys

This fork presents some modifications in order to add support for Python 3.

If you are using Python 3 and need to use Redsys and are looking for a simple 
client library, then Sydres is the package you are looking for.

In the same scenario but while using Python 2, maybe you will prefer to use the
original project (this one has not been used with Python 2).
"""

from setuptools import setup

PACKAGES = ['sydres', ]
PACKAGES_DATA = {'sydres.tests': []}

setup(name='sydres',
    description='A client to submit payment orders to the Redsys service.',
    long_description=__doc__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Web Environment",
    ],
    keywords=['redsys', 'sydres'],
    author='Alex Barcelo',
    author_email='alex.barcelo@gmail.com',
    url="https://github.com/alexbarcelo/sydres",
    version='0.2.1',
    license='General Public Licence 3',
    provides=['sydres'],
    install_requires=['pycrypto',],
    packages=PACKAGES,
    package_data=PACKAGES_DATA,
    scripts=[],
    test_suite='sydres.tests',
)

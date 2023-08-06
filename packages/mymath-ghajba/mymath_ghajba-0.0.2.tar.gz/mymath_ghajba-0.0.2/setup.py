# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="mymath_ghajba",
    version="0.0.2",
    description="A simple mathematics package to demonstrate the usage of pip-init and setuptools",
    license="MIT",
    author="Gábor László Hajba",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ]
)

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="cinit",
    version="0.1.0",
    description="Create a c/c++ directory structure",
    license="MIT",
    author="JuanPabloAJ",
    packages=find_packages(),
    install_requires=[],
    author_email="jpabloaj@gmail.com",
    url="https://github.com/juanpabloaj/cinit",
    entry_points={
        'console_scripts': [
            'cinit=cinit:main',
        ],
    },
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)

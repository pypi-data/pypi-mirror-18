#!/usr/bin/env python
from setuptools import setup

setup(
    name='nameko-objectstorage',
    version='0.1.2',
    description='A dependency for IBM Bluemix Object Storage',
    author='frisellcpl',
    author_email='johan@trell.se',
    url='http://github.com/frisellcpl/nameko-objectstorage',
    packages=['nameko_objectstorage'],
    install_requires=[
        "nameko==2.4.3"
    ],
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)

#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'FOFA',
    version = '1.0.0',
    description = 'Python library and command-line utility for FOFA (https://fofa.so)',
    author = 'gcr',
    author_email = 'yzjjaheim@163.com',
    url = 'http://fofa.so',
    packages = ['fofa', 'fofa.poc', 'fofa.src'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
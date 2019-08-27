#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unofficial Detux.org API wrapper
Pre-alpha release still under active development
====
Zeroharbor Research & Development
https://www.zeroharbor.org
"""

from setuptools import setup, find_packages

setup(
    name='detux',
    version='0.0.1',
    url='https://github.com/zeroharbor/detux-api',
    author='Adam M. Swanda (Zeroharbor)',
    author_email='adam@zeroharbor.com',
    description="""Assistant for interacting with the Detux.org Linux malware sandbox API""",
    keywords='detux detux.org malware sandbox linux',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'requests=='2.20.0',
        'boto3==1.4.3'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

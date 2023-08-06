#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name            = 'cmsplugin-survey',
    version         = '1.0.0',
    description     = 'django CMS plugin to show simple surveys',
    author          = 'Jakub Dorňák',
    author_email    = 'jakub.dornak@misli.cz',
    license         = 'BSD',
    url             = 'https://github.com/misli/cmsplugin-survey',
    packages        = find_packages(),
    include_package_data = True,
    classifiers     = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Czech',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)

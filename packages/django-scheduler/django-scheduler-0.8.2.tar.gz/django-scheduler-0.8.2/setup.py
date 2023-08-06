#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='django-scheduler',
    version='0.8.2',
    description='A calendaring app for Django.',
    author='Leonardo Lazzaro',
    author_email='lazzaroleonardo@gmail.com',
    url='https://github.com/llazzaro/django-scheduler',
    packages=[
        'schedule',
        'schedule.feeds',
        'schedule.management',
        'schedule.management.commands',
        'schedule.models',
        'schedule.migrations',
        'schedule.templatetags',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Django>=1.8',
        'python-dateutil>=2.1',
        'pytz>=2013.9',
        'icalendar>=3.8.4',
        'django-annoying>=0.8.0',
    ],
    license='BSD',
    test_suite='runtests.runtests',
)

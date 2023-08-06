#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class TestCommand(TestCommand):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings

        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=(
                'videofield',
            ),
        )

        import django
        from django.test.utils import get_runner

        django.setup()

        TestRunner = get_runner(settings)
        runner = TestRunner(verbosity=1, interactive=False, failfast=False)

        failures = runner.run_tests([])

        if failures > 0:
            sys.exit(1)


setup(
    name='django-videofield',
    version='0.1.1',
    description='Support for video upload in Django models',
    long_description=open('README.rst', 'r').read(),
    author='André Luiz',
    author_email='contato@xdvl.info',
    url='https://github.com/dvl/django-videofield',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='django video model field',
    install_requires=['Django >= 1.8'],
    tests_require=['Django >= 1.8'],
    packages=['videofield'],
    cmdclass={'test': TestCommand}
)

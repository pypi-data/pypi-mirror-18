# -*- coding: utf-8 -*-
import os
import sys

from setuptools import Command, setup, find_packages

from requests_tracker import __version__

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCommand(Command):

    description = "use `python manage.py test` instead."
    user_options = []

    def run(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testapp.settings')

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


description = "Tracking http requests send by python-requests " \
              "inside a Django application"

install_requires = [
    'Django>=1.8',
    'requests>=2.10,<2.11',
]

setup(
    name='django-requests-tracker',
    version=__version__,
    description=description,
    author='sveinchen',
    author_email='sveinchen@gmail.com',
    url='https://sveinchen.github.io/django-requests-tracker',
    packages=find_packages(include=['requests_tracker',
                                    'requests_tracker.*']),
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'test': TestCommand,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)

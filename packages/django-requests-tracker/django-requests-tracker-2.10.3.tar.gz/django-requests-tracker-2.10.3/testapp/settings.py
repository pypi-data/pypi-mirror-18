# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib
import os

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'bml(#c5n-&)j03uf!7)#-(d95z(nz^xx6zw=_cxe+l&-=5al)p'

INSTALLED_APPS = (
    'requests_tracker',
)

MIDDLEWARE_CLASSES = tuple()


#
# PyMySQL
#

try:
    import pymysql
except ImportError:
    pass
else:
    pymysql.install_as_MySQLdb()


#
# Django-celery
#

try:
    import djcelery
except ImportError:
    pass
else:
    djcelery.setup_loader()


#
# Django-nose
#

django_nose_installed = False

try:
    importlib.import_module('django_nose')
    django_nose_installed = True
except ImproperlyConfigured:
    django_nose_installed = True
except ImportError:
    pass

if django_nose_installed:
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#
# Coverage.py
#

try:
    importlib.import_module('coverage')
except ImportError:
    pass
else:
    cover_packages = []
    for app in INSTALLED_APPS:
        module_name = app.split('.')[0]
        if os.path.isfile(os.path.join(BASE_DIR, module_name, '__init__.py')):
            cover_packages.append(module_name)

    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=%s' % ','.join(cover_packages),
        '--cover-inclusive',
    ]

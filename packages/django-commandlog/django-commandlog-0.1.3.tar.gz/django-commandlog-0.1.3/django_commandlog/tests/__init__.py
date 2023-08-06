# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django, sys
from django.conf import settings

if not settings.configured:  # Prevent this from running in django installation
	settings.configure(DEBUG=True,
	                   DATABASES={
	                       'default': {
	                           'ENGINE': 'django.db.backends.sqlite3',
	                           'NAME': ':memory:',
	                       }
	                   },
	                   INSTALLED_APPS=('django.contrib.auth',
	                                   'django.contrib.contenttypes',
	                                   'django.contrib.sessions',
	                                   'django.contrib.admin',
	                                   'django_commandlog',))

	try:
	    # Django <= 1.8
	    from django.test.simple import DjangoTestSuiteRunner
	    test_runner = DjangoTestSuiteRunner(verbosity=1)
	except ImportError:
	    # Django >= 1.8
	    django.setup()
	    from django.test.runner import DiscoverRunner
	    test_runner = DiscoverRunner(verbosity=1)

	failures = test_runner.run_tests(['django_commandlog'])
	if failures:
	    sys.exit(failures)

==========================================
Django CommandLog - Django Command logging
==========================================

.. image:: https://travis-ci.org/achedeuzot/django-commandlog.svg?branch=master
    :target: https://travis-ci.org/achedeuzot/django-commandlog?branch=master

.. image:: https://coveralls.io/repos/github/achedeuzot/django-commandlog/badge.svg?branch=master
    :target: https://coveralls.io/github/achedeuzot/django-commandlog?branch=master



Django CommandLog adds the possibility to log django management commands. The log is then available in the admin interface.

Quick start
-----------

1. Add "django_commandlog" to your ``INSTALLED_APPS`` settings like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_commandlog',
    ]


2. Run `python manage.py migrate` to add the tables of `django_commandlog` to your database.

3. To log an admin command, add the `@command_log` decorator above the class. It currently
supports only custom management commands. If you wish to add this to default django manage commands
you'll have to create a child class with the decorator. Pull/Merge requests are welcome with a fix for this. Example below:

.. code-block:: python

    @command_log
    class SampleCommand(BaseCommand):

        def handle(self, *args, **options):
            ...

Requirements
------------

- python 2.7, 3.3
- django 1.10


Tested on `Django`_ 1.10.3

.. _Django: http://www.djangoproject.com/


==========================================
Django CommandLog - Django Command logging
==========================================

.. image:: https://travis-ci.org/achedeuzot/django-commandlog.svg?branch=master
    :target: https://travis-ci.org/achedeuzot/django-commandlog?branch=master

.. image:: https://coveralls.io/repos/github/achedeuzot/django-commandlog/badge.svg?branch=master
    :target: https://coveralls.io/github/achedeuzot/django-commandlog?branch=master

Django CommandLog adds the feature of logging the django management commands into the database so it's available in the admin interface.

We've been using this to check the result of scheduled management commands directly through the admin interface. It works by copying the stream of ``stdout`` and ``stderr``.

The decorator also adds some helper methods, see below.

Quick start
-----------

1. Add "django_commandlog" to your ``INSTALLED_APPS`` settings like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_commandlog',
    ]


2. Run `python manage.py migrate` to add the tables of `django_commandlog` to your database.

3. To log an admin command, add the `@command_log` decorator above the class
(see example below). Thus, it currently supports only custom management
commands. If you wish to add this to default django manage commands you'll
have to create a child class with the decorator. Pull/Merge requests
are welcome with a fix for this.

.. code-block:: python

    @command_log
    class SampleCommand(BaseCommand):

        def handle(self, *args, **options):
            ...

Configuration
-------------

There are currently no configuration values.

Helper methods
--------------
When your class is decorated with ``@command_log``, you have access to additional methods.

CommandLog includes counters for basic CRUD operations (Create, Read, Update, Delete) which can be used
through helper methods provided:

.. code-block:: python

    add_created(10)
    add_read(30)
    add_updated(20)
    add_deleted(30)
    add_errors(14)

There are two fields used to track the commands or runs: reference and user.
Reference is any number you want to track in your manage commands.

You can also add a user to the tracking by using the `add_log_user(user)` method. `user` can be a string which will be kept as-is or you can use a `settings.AUTH_USER_MODEL` object.

.. code-block:: python

    add_log_reference("C1235342321")
    add_log_user("user:ldap:username")
    # or
    add_log_user(user_instance)

Requirements
------------

- python 2.7, 3.3
- django 1.10


Tested on `Django`_ 1.10.3

.. _Django: http://www.djangoproject.com/


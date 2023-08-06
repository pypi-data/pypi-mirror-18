# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import traceback

from functools import wraps

from six import string_types
from django.apps import apps
from django.conf import settings
from django.utils import timezone

from django_commandlog.helpers import OutputTeeWrapper
from django_commandlog.models import CommandLog


def command_log(cls):

    def init__decorator(fn):
        @wraps(fn, assigned=('__name__', '__doc__'))
        def wrapper(self, *args, **kwargs):
            fn(self, *args, **kwargs)
            if hasattr(self, '_cmdlog'):
                raise AttributeError("%s already has a _cmdlog attribute "
                                     "that conflicts with the @command_log "
                                     "decorator" % cls.__class__.__name__)
            self._cmdlog = CommandLog.objects.create(
                command_name=self.__class__.__name__,
            )
            self.stdout = OutputTeeWrapper(self.stdout, self._cmdlog, 'stdout')
            self.stderr = OutputTeeWrapper(self.stderr, self._cmdlog, 'stderr')
        return wrapper

    def handle_decorator(fn):
        @wraps(fn, assigned=('__name__', '__doc__'))
        def wrapper(self, *args, **kwargs):
            try:
                fn(self, *args, **kwargs)
                self._cmdlog.success = True
            except Exception:
                self._cmdlog.traceback = traceback.format_exc()
                self._cmdlog.success = False
                raise
            finally:
                self._cmdlog.end_at = timezone.now()
                self._cmdlog.total = self._cmdlog.created + \
                                      self._cmdlog.updated + \
                                      self._cmdlog.deleted
                self._cmdlog.save()
        return wrapper

    cls.__init__ = init__decorator(cls.__init__)
    cls.handle = handle_decorator(cls.handle)

    def _add_cmdlog_func(fn, name):
        if hasattr(cls, name):
            raise AttributeError(
                "%s already has a %s attribute "
                "that conflicts with the @command_log "
                "decorator" % (cls.__name__, name)
            )
        setattr(cls, name, fn)

    def _add_to_counter(self, field_name, value):
        self._cmdlog.__dict__[field_name] += value
        self._cmdlog.save()
    _add_cmdlog_func(_add_to_counter, '_cmdlog_add_to_counter')

    # CRUD helpers
    def add_log_created(self, value=1):
        self._cmdlog_add_to_counter('created', value)
    _add_cmdlog_func(add_log_created, 'add_log_created')

    def add_log_read(self, value=1):
        self._cmdlog_add_to_counter('read', value)
    _add_cmdlog_func(add_log_read, 'add_log_read')

    def add_log_updated(self, value=1):
        self._cmdlog_add_to_counter('updated', value)
    _add_cmdlog_func(add_log_updated, 'add_log_updated')

    def add_log_deleted(self, value=1):
        self._cmdlog_add_to_counter('deleted', value)
    _add_cmdlog_func(add_log_deleted, 'add_log_deleted')

    def add_log_errors(self, value=1):
        self._cmdlog_add_to_counter('errors', value)
    _add_cmdlog_func(add_log_errors, 'add_log_errors')

    # Logging helpers
    def write_success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))
    _add_cmdlog_func(write_success, 'write_success')

    def write_warning(self, msg):
        self.stdout.write(self.style.WARNING(msg))
    _add_cmdlog_func(write_warning, 'write_warning')

    def write_notice(self, msg):
        self.stdout.write(self.style.NOTICE(msg))
    _add_cmdlog_func(write_notice, 'write_notice')

    def write_error(self, msg):
        self.stderr.write(self.style.ERROR(msg))
    _add_cmdlog_func(write_error, 'write_error')

    # Add reference
    def add_log_reference(self, ref):
        self._cmdlog.reference = ref
        self._cmdlog.save()
    _add_cmdlog_func(add_log_reference, 'add_log_reference')

    # Add User
    def add_log_user(self, user):
        UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        if isinstance(user, UserModel):
            self._cmdlog.imported_by_user = user
            self._cmdlog.imported_by_str = str(user)
            self._cmdlog.save()
        elif isinstance(user, string_types):
            self._cmdlog.imported_by_str = user
            self._cmdlog.save()
        else:
            raise ValueError("`add_log_user()` accepts only settings.AUTH_USER_MODEL or string values.")
    _add_cmdlog_func(add_log_user, 'add_log_user')

    return cls

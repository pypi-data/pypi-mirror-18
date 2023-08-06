# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import traceback

from functools import wraps

from django.utils import timezone

from django_commandlog import app_settings
from django_commandlog.helpers import OutputTeeWrapper
from django_commandlog.models import CommandLog


def command_log(cls):

    def init__decorator(fn):
        @wraps(fn)
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
        @wraps(fn)
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
                if app_settings.ENABLE_COUNTER_FIELDS:
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

    # Add shortcut functions
    if app_settings.ENABLE_COUNTER_FIELDS:

        def _add_to_counter(self, field_name, value):
            self._cmdlog.__dict__[field_name] += value
            self._cmdlog.save()
        _add_cmdlog_func(_add_to_counter, '_cmdlog_add_to_counter')

        # Add helper function for the 4 basic operation counters
        def add_created(self, value=1):
            self._cmdlog_add_to_counter('created', value)
        _add_cmdlog_func(add_created, 'add_created')

        def add_read(self, value=1):
            self._cmdlog_add_to_counter('read', value)
        _add_cmdlog_func(add_read, 'add_read')

        def add_updated(self, value=1):
            self._cmdlog_add_to_counter('updated', value)
        _add_cmdlog_func(add_updated, 'add_updated')

        def add_deleted(self, value=1):
            self._cmdlog_add_to_counter('deleted', value)
        _add_cmdlog_func(add_deleted, 'add_deleted')

        def add_errors(self, value=1):
            self._cmdlog_add_to_counter('errors', value)
        _add_cmdlog_func(add_errors, 'add_errors')

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

    return cls

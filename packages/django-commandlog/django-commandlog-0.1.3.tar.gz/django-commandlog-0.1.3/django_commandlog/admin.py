# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.contrib import admin

from django_commandlog.models import CommandLog
from .app_settings import *


class CommandLogAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'start_at', 'end_at', 'duration', 'success', 'reference']
    list_filter = ['command_name', 'reference']
    readonly_fields = ['uuid', 'command_name', 'reference',
                       'start_at', 'end_at',
                       'success',
                       'raw_output', 'stdout', 'stderr',
                       'imported_by_user', 'imported_by_str', ]
    if ENABLE_COUNTER_FIELDS:
        readonly_fields += ['created', 'read', 'updated', 'deleted', 'errors']

    @staticmethod
    def duration(obj):
        return obj.get_duration()

    if ENABLE_COUNTER_FIELDS:
        @staticmethod
        def total_crud(obj):
            return obj.get_total_crud()

admin.site.register(CommandLog, CommandLogAdmin)

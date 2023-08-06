# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.contrib import admin

from django_commandlog.models import CommandLog
from .app_settings import *


class CommandLogAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'reference', 'start_at', 'end_at', 'duration', 'success', 'total_crud']
    list_filter = ['command_name', ]
    readonly_fields = ['uuid', 'command_name', 'reference',
                       'start_at', 'end_at',
                       'success',
                       'raw_output', 'stdout', 'stderr',
                       'imported_by_user', 'imported_by_str',
                       'created', 'read', 'updated', 'deleted', 'errors']

    @staticmethod
    def duration(obj):
        return obj.get_duration()

    @staticmethod
    def total_crud(obj):
        return obj.get_total_crud()

admin.site.register(CommandLog, CommandLogAdmin)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class CommandLogConfig(AppConfig):
    name = 'django_commandlog'
    verbose_name = ugettext_lazy('Command Log')

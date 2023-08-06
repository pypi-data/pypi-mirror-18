# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.conf import settings

ENABLE_COUNTER_FIELDS = getattr(settings, 'COMMANDLOG_ENABLE_COUNTER_FIELDS', True)

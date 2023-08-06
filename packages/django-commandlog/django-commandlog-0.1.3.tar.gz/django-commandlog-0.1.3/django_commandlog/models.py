# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import uuid
import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django_timestampable.models import TimestampableModel
from django.utils.timezone import now

from django_commandlog.app_settings import *


class CommandLog(TimestampableModel, models.Model):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    command_name = models.CharField(max_length=255, null=False, blank=False, editable=False)
    start_at = models.DateTimeField(null=False, editable=False)
    end_at = models.DateTimeField(null=True, editable=False)
    success = models.NullBooleanField(default=None, editable=False)
    raw_output = models.TextField(null=True, editable=False)
    stdout = models.TextField(null=True, editable=False)
    stderr = models.TextField(null=True, editable=False)
    traceback = models.TextField(null=True, editable=False)

    # Generic field if you need to sort or filter your commands
    reference = models.CharField(max_length=255, editable=False)

    imported_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=False)
    imported_by_str = models.CharField(max_length=255, editable=False)

    if ENABLE_COUNTER_FIELDS:
        created = models.BigIntegerField(default=0, editable=False)
        read = models.BigIntegerField(default=0, editable=False)
        updated = models.BigIntegerField(default=0, editable=False)
        deleted = models.BigIntegerField(default=0, editable=False)

        errors = models.BigIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _('command log')
        verbose_name_plural = _('command logs')
        ordering = ['-created_at']

    def __str__(self):
        imported_by = ""
        if self.imported_by_user:
            imported_by = " by {user}".format(user=self.imported_by_user)
        elif self.imported_by_str:
            imported_by = " by {user}".format(user=self.imported_by_str)
        return "{command_name} at {start_at}{imported_by}".format(
            command_name=self.command_name,
            start_at=datetime.datetime.strftime(self.start_at, '%Y-%m-%d %H:%M:%S'),
            imported_by=imported_by)

    def get_duration(self):
        if self.end_at:
            return self.end_at - self.start_at
        else:
            return datetime.timedelta()

    if ENABLE_COUNTER_FIELDS:
        def get_total_crud(self):
            return self.created + self.read + self.updated + self.deleted


@receiver(pre_save)
def update_commandlog_start_at(sender, instance, *args, **kwargs):
    """
    Using signals guarantees that the start time is set no matter what:
    loading fixtures, bulk inserts, bulk updates, etc.
    Indeed, the `save()` method is *not* called when using fixtures.
    """
    if not isinstance(instance, CommandLog):
        return
    if not instance.pk:
        instance.start_at = now()

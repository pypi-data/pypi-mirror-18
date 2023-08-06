# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function


import datetime
from django.contrib.admin import AdminSite
from django.test import TestCase
from django.utils.timezone import make_aware

from django_commandlog.admin import CommandLogAdmin
from django_commandlog.models import CommandLog


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class CommandLogAdminTestCase(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.cmdlog = CommandLog()
        self.cmdlog.save()
        self.cmdlog.start_at = make_aware(datetime.datetime(year=2016, month=2, day=2, hour=13, minute=37, second=42))
        self.cmdlog.end_at = self.cmdlog.start_at + datetime.timedelta(days=1)
        self.cmdlog.created = 42
        self.cmdlog.deleted = 21
        self.cmdlog.save()

    def test_log_admin_duration(self):
        self.assertEqual(CommandLogAdmin.duration(self.cmdlog), datetime.timedelta(days=1))

    def test_log_admin_total_crud(self):
        self.assertEqual(CommandLogAdmin.total_crud(self.cmdlog), 63)

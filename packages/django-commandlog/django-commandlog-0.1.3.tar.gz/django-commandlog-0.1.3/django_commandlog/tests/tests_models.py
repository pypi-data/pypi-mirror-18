# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import override_settings

from django_commandlog.models import CommandLog


class CommandLogModelTestCase(TestCase):
    """
    Test the CommandLog Mixin !
    """

    def test_commandlog_model_without_counter_fields(self):
        with override_settings(ENABLE_COUNTER_FIELDS=False):
            inst = CommandLog()
            inst.save()
            self.assertIsNotNone(inst.uuid)
            self.assertIsNotNone(inst.command_name)
            self.assertIsNotNone(inst.start_at)
            self.assertIsNone(inst.end_at)
            self.assertIsNone(inst.success)

    def test_commandlog_model_with_counter_fields(self):
        with override_settings(ENABLE_COUNTER_FIELDS=True):
            inst = CommandLog()
            inst.save()
            self.assertIsNotNone(inst.uuid)
            self.assertIsNotNone(inst.command_name)
            self.assertIsNotNone(inst.start_at)
            self.assertIsNone(inst.end_at)
            self.assertIsNone(inst.success)
            self.assertEqual(inst.created, 0)
            self.assertEqual(inst.read, 0)
            self.assertEqual(inst.updated, 0)
            self.assertEqual(inst.deleted, 0)
            self.assertEqual(inst.errors, 0)

    def test_commandlog_model_str_output_simple(self):
        inst = CommandLog()
        inst.save()
        start_at_str = datetime.datetime.strftime(inst.start_at, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(str(inst), " at " + start_at_str + "")

    def test_commandlog_model_str_output_complete(self):
        inst = CommandLog()
        inst.save()
        inst.command_name = self.__class__.__name__
        inst.imported_by_str = "Test User"
        start_at_str = datetime.datetime.strftime(inst.start_at, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(str(inst), self.__class__.__name__ + " at " + start_at_str + " by Test User")

    def test_commandlog_model_str_output_complete_with_user(self):
        u = User.objects.create(username="test", email="test@example.org")
        inst = CommandLog()
        inst.save()
        inst.command_name = self.__class__.__name__
        inst.imported_by_user = u
        start_at_str = datetime.datetime.strftime(inst.start_at, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(str(inst), self.__class__.__name__ + " at " + start_at_str + " by test")

    def test_commandlog_model_duration_calculation(self):
        inst = CommandLog()
        inst.start_at = datetime.datetime(year=2016, month=2, day=2, hour=13, minute=37, second=42)
        inst.end_at = inst.start_at + datetime.timedelta(days=1)
        self.assertEqual(inst.get_duration(), datetime.timedelta(days=1))

    def test_commandlog_model_duration_empty(self):
        inst = CommandLog()
        inst.save()
        self.assertEqual(inst.get_duration(), datetime.timedelta())

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.test import TestCase
from django.test import override_settings

from django_commandlog.decorators import command_log
from django_commandlog.helpers import uncolorize, OutputTeeWrapper, no_output
from django_commandlog.models import CommandLog


class TestException(Exception):
    pass


@command_log
class SampleCommand(BaseCommand):

    help = 'Tests the decorator'

    def add_arguments(self, parser):
        parser.add_argument('--test',
                            action='store_true',
                            dest='test_flag',
                            default=False,
                            help='Test flag argument',)

    def handle(self, *args, **options):
        if options.get('test_flag', False):
            self.stdout.write("Test flag: True")
        else:
            self.stdout.write("Test flag: False")

        if options.get('raise_error', False):
            raise TestException

        if options.get('counters_enabled', False):
            self.add_log_created(84)
            self.add_log_read(42)
            self.add_log_updated(21)
            self.add_log_deleted(10)

            self.add_log_errors(5)


class CommandLogDecoratorTestCase(TestCase):

    def test_sample_command_instanciation(self):
        cmd = SampleCommand()
        # Check CommandLog object has been added to class
        self.assertIsNotNone(cmd._cmdlog)

    def test_sample_command_instanciation_with_conflicting_attribute(self):
        # Subclass to test attribute conflict
        class ChildOfSampleCommand(SampleCommand):
            _cmdlog = True
        with self.assertRaises(AttributeError):
            ChildOfSampleCommand()

    def test_sample_command_instanciation_with_conflicting_function_attribute(self):
        with no_output():
            class TestConflictingAttributeCommand(object):
                def handle(self):
                    pass

                def add_log_created(self):
                    pass
            with self.assertRaises(AttributeError):
                command_log(TestConflictingAttributeCommand)

    def test_sample_command_can_be_called(self):
        with no_output():
            cmd = SampleCommand()
            cmd.handle()
        self.assertEqual(cmd._cmdlog.stdout, "Test flag: False\n")

    def test_sample_command_with_options(self):
        with no_output():
            cmd = SampleCommand()
            cmd.handle(test_flag=True)
        self.assertEqual(cmd._cmdlog.stdout, "Test flag: True\n")

    def test_handle_decorated_with_success(self):
        with no_output():
            cmd = SampleCommand()
            cmd.handle()
        self.assertTrue(cmd._cmdlog.success)  # Should have succeeded
        self.assertIsNotNone(cmd._cmdlog.end_at)  # End time should be set

    def test_handle_decorated_with_exception(self):
        with no_output():
            cmd = SampleCommand()
            with self.assertRaises(TestException):
                cmd.handle(raise_error=True)
        self.assertFalse(cmd._cmdlog.success)  # Should be marked as failed
        self.assertIsNotNone(cmd._cmdlog.end_at)  # End time should be set
        self.assertIsNotNone(cmd._cmdlog.traceback)

    def test_counters(self):
        with no_output():
            cmd = SampleCommand()
            cmd.handle(counters_enabled=True)
            self.assertEqual(cmd._cmdlog.created, 84)
            self.assertEqual(cmd._cmdlog.read, 42)
            self.assertEqual(cmd._cmdlog.updated, 21)
            self.assertEqual(cmd._cmdlog.deleted, 10)
            self.assertEqual(cmd._cmdlog.errors, 5)
            self.assertEqual(cmd._cmdlog.get_total_crud(), 157)

    def test_write_shortcuts(self):
        with no_output():
            cmd = SampleCommand()
            cmd.write_success("Success message")
            cmd.write_warning("Warning message")
            cmd.write_notice("Notice message")
            cmd.write_error("ERROR message")

    def test_add_reference(self):
        test_ref = "R987654321"
        with no_output():
            cmd = SampleCommand()
            cmd.add_log_reference(test_ref)
            self.assertEqual(CommandLog.objects.get(reference=test_ref).reference, test_ref)

    def test_add_log_user_str(self):
        test_str = "user:ldap:username"
        with no_output():
            cmd = SampleCommand()
            cmd.add_log_user(test_str)
            self.assertEqual(CommandLog.objects.get(imported_by_str=test_str).imported_by_str, test_str)

    def test_add_log_user_object(self):
        UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        test_user = UserModel.objects.create(username="test",
                                             email="test@example.com")
        with no_output():
            cmd = SampleCommand()
            cmd.add_log_user(test_user)
            self.assertEqual(CommandLog.objects.get(imported_by_user=test_user).imported_by_str, str(test_user))
            self.assertEqual(CommandLog.objects.get(imported_by_user=test_user).imported_by_user, test_user)

    def test_add_log_user_wrong_type(self):
        test_user_wrong = True
        with no_output():
            cmd = SampleCommand()
            with self.assertRaises(ValueError):
                cmd.add_log_user(test_user_wrong)

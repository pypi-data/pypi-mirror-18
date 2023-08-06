# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys
from django.test import TestCase

from django_commandlog.helpers import uncolorize, OutputTeeWrapper, no_output
from django_commandlog.models import CommandLog


class UncolorizeHelperFunctionTestCase(TestCase):

    def test_uncolorize_function(self):
        colorized_str = "\033[0;31m Very Bad Error \033[0m"
        uncolorized_str = " Very Bad Error "
        self.assertEqual(uncolorize(colorized_str), uncolorized_str)

    def test_uncolorize_function_without_coloring(self):
        colorized_str = "Some text..."
        uncolorized_str = "Some text..."
        self.assertEqual(uncolorize(colorized_str), uncolorized_str)

    def test_uncolorize_function_with_only_opening_tag(self):
        # We do not test this because django logic always encloses
        # the message between two tags of ANSI graphics codes.
        pass


class OutputWrapperTestCase(TestCase):

    def test_empty_output(self):
        cmd_log = CommandLog.objects.create(
            command_name='test_output_wrapper',
        )
        OutputTeeWrapper(sys.stdout, cmd_log, 'stdout')
        self.assertEqual(cmd_log.stdout, "")
        self.assertEqual(cmd_log.raw_output, "")

    def test_some_stdout(self):
        cmd_log = CommandLog.objects.create(
            command_name='test_output_wrapper',
        )
        with no_output():
            inst = OutputTeeWrapper(sys.stdout, cmd_log, 'stdout')
            msg = "Some stuff written to stdout...\n"
            inst.write(msg)
            self.assertEqual(cmd_log.stdout, msg)
            self.assertEqual(cmd_log.raw_output, msg)

    def test_some_stdout_without_newline(self):
        cmd_log = CommandLog.objects.create(
            command_name='test_output_wrapper',
        )
        with no_output():
            inst = OutputTeeWrapper(sys.stdout, cmd_log, 'stdout')
            msg = "Some stuff written to stdout..."
            inst.write(msg)
            self.assertEqual(cmd_log.stdout, msg + "\n")
            self.assertEqual(cmd_log.raw_output, msg + "\n")

    def test_wrong_attribute(self):
        cmd_log = CommandLog.objects.create(
            command_name='test_output_wrapper',
        )
        with self.assertRaises(AttributeError):
            OutputTeeWrapper(sys.stdout, cmd_log, 'stdunknown')


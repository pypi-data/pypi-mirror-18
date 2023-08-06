# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import contextlib
import re
import sys
from django.core.management.base import OutputWrapper as BaseOutputWrapper
from django.utils.encoding import force_str
from django.utils.termcolors import RESET


def uncolorize(msg):
    start_pattern = re.compile(u'^\x1b\[[\d+;*]+m')
    end_pattern = re.compile(u'\x1b\[%sm$' % RESET)
    start_match = re.search(start_pattern, msg)
    end_match = re.search(end_pattern, msg)
    if start_match and end_match:
        return msg[len(start_match.group(0)):-len(end_match.group(0))]
    return msg


class OutputTeeWrapper(BaseOutputWrapper):

    def __init__(self, out, cmd_log, cmd_log_attr):
        super(OutputTeeWrapper, self).__init__(out)
        self._cmd_log = cmd_log
        if not hasattr(cmd_log, cmd_log_attr):
            raise AttributeError("CommandLog has not attribute %s" % cmd_log_attr)
        self._cmd_log_attr = cmd_log_attr
        # Init empty string
        self._cmd_log.__dict__[self._cmd_log_attr] = ""
        self._cmd_log.raw_output = ""
        self._cmd_log.save()

    def write(self, msg, style_func=None, ending=None):
        super(OutputTeeWrapper, self).write(msg, style_func=style_func, ending=ending)
        msg = uncolorize(msg)
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        self._cmd_log.__dict__[self._cmd_log_attr] += force_str(msg)
        self._cmd_log.raw_output += force_str(msg)
        self._cmd_log.save()


@contextlib.contextmanager
def no_output():
    save_stderr = sys.stderr
    save_stdout = sys.stdout

    class Devnull(object):

        def write(self, _): pass

        def flush(self): pass

    sys.stderr = Devnull()
    sys.stdout = Devnull()
    try:
        yield
    finally:
        sys.stderr = save_stderr
        sys.stdout = save_stdout


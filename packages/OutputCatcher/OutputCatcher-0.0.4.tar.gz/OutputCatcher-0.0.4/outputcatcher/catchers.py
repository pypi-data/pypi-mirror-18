#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from io import UnsupportedOperation

__version__ = '0.0.4'


class StdOutCatcher(object):
    """ Catches stdout for code inside the 'with' block.

        Usage:
            with StdOutCatcher(safe=True, maxlength=160) as fakestdout:
                # stdout is stored in fakestdout.output
                print('okay')
            # stdout is back to normal
            # retrieve the captured output..
            print('output was: {}'.format(fakestdout.output))
    """
    stdout = sys.stdout

    def __init__(self, escaped=False, max_length=160):
        # Use safe_output?
        self.escaped = escaped
        # Maximum length before trimming output
        self.max_length = max_length
        # Output
        self._output = ''
        self.length = 0
        self.max_exceeded = False

    def __enter__(self):
        # Replace fileobj with self, fileobj.write() will be self.write()
        sys.stdout = self
        return self

    def __exit__(self, type, value, traceback):
        # Fix stdout.
        sys.stdout = sys.__stdout__

    @property
    def name(self):
        return getattr(
            self.stdout,
            'name',
            getattr(self.stdout, '__name__', type(self.stdout).__name__)
        )

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        """ Sets self._output, escaping first if self.escaped is truthy. """
        if self.escaped:
            self._output = self.make_safe(value)
            return None
        self._output = value
        return None

    @staticmethod
    def make_safe(s):
        """ Escape output using python's repr(). """
        return repr(s)[1:-1]

    def write(self, s):
        if (not s) or self.max_exceeded:
            # Nothing to write, or max-length was already exceeded.
            return 0

        # Save output
        self.output = ''.join((
            self.output,
            s
        ))
        # Trim and block the next call if we are already at max_length.
        if len(self.output) >= self.max_length:
            self.output = self.output[:self.max_length]
            self.max_exceeded = True
        self.length = len(self.output)
        return len(s)

    def writeln(self, s):
        """ Convenience method for green.output.GreenStreams. """
        return self.write('{}\n'.format(s))


class StdErrCatcher(StdOutCatcher):
    stderr = sys.stderr

    def __enter__(self):
        # Replace stderr with self, stderr.write() will be self.write()
        sys.stderr = self
        return self

    def __exit__(self, type, value, traceback):
        # Fix stderr.
        sys.stderr = sys.__stderr__

    @property
    def name(self):
        return getattr(
            self.stderr,
            'name',
            getattr(self.stderr, '__name__', type(self.stderr).__name__)
        )

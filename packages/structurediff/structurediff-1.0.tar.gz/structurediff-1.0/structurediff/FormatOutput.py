#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
import sys
from pprint import pformat
from termcolor import colored
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


def formatoutput(args, comparison):
    '''build output string for console'''
    ret = []
    if comparison.equivalent and args.verbose:
        if sys.stdout.isatty():
            ret.append(colored("The inputs contain equivalent data.",
                               'green'))
        else:
            ret.append("The inputs contain equivalent data.")
    elif not comparison.equivalent and sys.stdout.isatty():
        if args.verbose:
            ret.extend([
                colored("The inputs do not contain equivalent data.",
                        'red',
                        attrs=['underline', 'bold']),
                ''.join(["Changes in ",
                         colored(args.input2, 'cyan', attrs=['bold']),
                         " from ",
                         colored(args.input1, 'cyan', attrs=['bold']),
                         ":"]),
                colored("-----------------------------------------", 'cyan')])
        ret.append(highlight(pformat(comparison.diff,
                                     indent=args.indent_level),
                             JsonLexer(),
                             TerminalFormatter()))
    elif not comparison.equivalent:
        if args.verbose:
            ret.extend([
                "The inputs do not contain equivalent data.",
                ''.join(["Changes in ",
                         args.input2,
                         " from ",
                         args.input1,
                         ":"]),
                "-----------------------------------------"])
            ret.append(pformat(comparison.diff, indent=args.indent_level))
    return '\n'.join(ret)

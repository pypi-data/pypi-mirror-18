#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
import argparse


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--diff-verbosity",
                        dest="diff_verbosity",
                        help="set the DeepDiff verbose_level, 0-2 (default 1)",
                        default=2,
                        action="store",
                        type=int)
    parser.add_argument("-i", "--indent-level",
                        dest="indent_level",
                        help="set the pprint indent spacing (default 2)",
                        default=2,
                        action="store",
                        type=int)
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        help="make output verbose",
                        action="store_true")
    parser.add_argument("input1",
                        help="initial input",
                        type=str)
    parser.add_argument("input2",
                        help="input to compare against input1",
                        type=str)
    return parser.parse_args()

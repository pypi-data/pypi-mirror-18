#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
from ArgsHandler import argparser
from FormatOutput import formatoutput
from DataFile import DataFile
from DataComparison import DataComparison


def main():
    args = argparser()
    print(formatoutput(args,
                       DataComparison(
                           DataFile(args.input1).data,
                           DataFile(args.input2).data,
                           args.diff_verbosity
                       )))


if __name__ == '__main__':
    main()

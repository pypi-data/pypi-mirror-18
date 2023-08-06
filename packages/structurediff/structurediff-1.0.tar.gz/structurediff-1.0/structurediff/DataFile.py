#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
import yaml


class DataFile(object):

    def __init__(self, path):
        ''' Initialise a datafile object '''
        self._path = path
        self._data = dict()
        self._read()
    path = property(lambda self: self._path)
    data = property(lambda self: self._data)

    def _read(self):
        with open(self._path) as datafile:
            rawtext = datafile.read()
            try:
                self._data = yaml.safe_load(rawtext)
            except ValueError:
                print(' '.join(["FATAL: Could not load",
                                self._path,
                                "with any available parser"]))

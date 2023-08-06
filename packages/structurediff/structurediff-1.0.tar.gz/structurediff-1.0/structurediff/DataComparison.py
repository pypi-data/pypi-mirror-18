#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
from deepdiff import DeepDiff


class DataComparison(object):

    def __init__(self, dicta, dictb, verbosity=1):
        '''object storing information on the relationship between two dicts'''
        self._dicta = dicta
        self._dictb = dictb
        self._equivalent = None
        self._diff = {}
        self._compare(self._dicta, self._dictb, verbosity)
    dicta = property(lambda self: self._dicta)
    dictb = property(lambda self: self._dictb)
    equivalent = property(lambda self: self._equivalent)
    diff = property(lambda self: self._diff)

    def _compare(self, dicta, dictb, verbosity):
        '''method for performing comparison'''
        self._diff = DeepDiff(self._dicta,
                              self._dictb,
                              verbose_level=verbosity)
        self._equivalent = (self._diff == {})

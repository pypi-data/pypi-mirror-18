# Copyright 2016 VMware, Inc.  All rights reserved. -- VMware Confidential
# coding: utf-8
import logging
from unittest import TestCase


class Loggable(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @property
    def logger(self):
        """

        :return: The logger
        :rtype: logging.Logger
        """
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(__name__)
        return self._logger

    @logger.setter
    def logger(self, value):
        """

        :param value: logger
        :type value: logging.Logger
        """
        self._logger = value


class A(Loggable):
    pass


class B(dict, Loggable):
    pass


class TestLoggable(TestCase):
    def test_a(self):
        a = A()
        self.assertTrue(isinstance(a.logger, logging.Logger))

    def test_b(self):
        b = B()
        self.assertTrue(isinstance(b.logger, logging.Logger))

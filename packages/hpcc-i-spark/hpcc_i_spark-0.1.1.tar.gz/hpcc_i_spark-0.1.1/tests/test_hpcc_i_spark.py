#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hpcc_i_spark
----------------------------------

Tests for `hpcc_i_spark` module.
"""

import unittest

import hpcc_i_spark


class TestHpcc_i_spark(unittest.TestCase):

    def setUp(self):
        self.hello_message = "Hello, Python"

    def test_prints_hello_python(self):
    	output = hpcc_i_spark.cli.hello()
        assert(output == self.hello_message)

    def tearDown(self):
        pass

# import pdb
# pdb.set_trace()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# testing for coda
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imporobj
# -------
import unittest
import os
import sys
import subprocess
import pandas
import random
from datetime import datetime

import quorra
from . import __base__


# tests
# -----
class TestEntryPoints(unittest.TestCase):

    def call(self, subcommand, *args):
        return subprocess.check_output('python -m quorra {} {}'.format(
            subcommand, ' '.join(args)
        ), stderr=subprocess.STDOUT, shell=True, cwd=__base__)

    def test_version(self):
        res = self.call('version')
        self.assertTrue(res, quorra.__version__)
        return


class TestExport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._time = datetime.now()
        return

    @classmethod
    def tearDownClass(cls):
        qtime = datetime.now() - cls._time
        if qtime.microseconds > 500000:
            sys.stderr.write('\n\nWarning: Export tests took more than 5s to run!\n\n')
        return

    def test_light_export(self):
        data = pandas.DataFrame({
            'x': [i for i in range(0, 10)],
            'y': [round(random.gauss(100, 10), 2) for i in range(0, 10)],
            'group': ['default']*10
        })
        plt = quorra.line()\
            .data(data, x='x', y='y', group='group')\
            .xlabel('X Label').ylabel('Y Label')\
            .zoomable(True)
        outfile = '.quorra-export-test-light-export.png'
        quorra.export(plt, outfile)
        self.assertTrue(os.path.exists(outfile))
        os.remove(outfile)
        return

    def test_heavy_export(self):
        points = 10000
        groups = ['one', 'two', 'three', 'four', 'five']
        data = pandas.DataFrame({
            'x': [i for i in range(0, points)]*len(groups),
            'y': [round(random.gauss(100, 10), 2) for i in range(0, points*len(groups))],
            'group': [grp for grp in groups for j in range(0, points)]
        })
        plt = quorra.line()\
            .data(data, x='x', y='y', group='group')\
            .xlabel('X Label').ylabel('Y Label')
        outfile = '.quorra-export-test-heavy-export.png'
        quorra.export(plt, outfile)
        self.assertTrue(os.path.exists(outfile))
        os.remove(outfile)
        return


# exec
# ----
if __name__ == '__main__':
    unittest.main()

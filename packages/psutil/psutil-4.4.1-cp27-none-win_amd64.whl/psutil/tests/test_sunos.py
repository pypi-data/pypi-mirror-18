#!/usr/bin/env python

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Sun OS specific tests."""

import os

import psutil
from psutil import SUNOS
from psutil.tests import run_test_module_by_name
from psutil.tests import sh
from psutil.tests import unittest


@unittest.skipUnless(SUNOS, "SUNOS only")
class SunOSSpecificTestCase(unittest.TestCase):

    def test_swap_memory(self):
        out = sh('env PATH=/usr/sbin:/sbin:%s swap -l' % os.environ['PATH'])
        lines = out.strip().split('\n')[1:]
        if not lines:
            raise ValueError('no swap device(s) configured')
        total = free = 0
        for line in lines:
            line = line.split()
            t, f = line[-2:]
            total += int(int(t) * 512)
            free += int(int(f) * 512)
        used = total - free

        psutil_swap = psutil.swap_memory()
        self.assertEqual(psutil_swap.total, total)
        self.assertEqual(psutil_swap.used, used)
        self.assertEqual(psutil_swap.free, free)


if __name__ == '__main__':
    run_test_module_by_name(__file__)

# coding: utf-8

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os
import shutil
import ctypes
import random
import unittest
import tempfile

import filelock

from filedict import *


class Storage1000(BaseStorage):
    _LOCK_TIMEOUT = 0

    max_records = 1000
    key_types = ctypes.c_uint64,
    val_types = ctypes.c_uint32, ctypes.c_uint32


class Storage2000(Storage1000):
    max_records = 2000


path = os.path.join(
    tempfile.gettempdir(),
    'filedict_{}'.format(random.randint(1000000, 9999999))
)


class SmokeTestCase(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_wrong_size(self):
        with Storage1000(path):
            # check creation
            pass
        with Storage1000(path):
            # check reopen
            pass
        try:
            with Storage2000(path):
                # check wrong size
                pass
        except WrongFileSizeError:
            return
        raise AssertionError('open storage with wrong size')

    def test_write_locks(self):
        try:
            with Storage1000(path):
                # write lock acquired here
                with Storage1000(path):
                    # unable to acquire lock here
                    pass
        except filelock.Timeout:
            return
        raise AssertionError('multiple writers allowed')

    def test_write_in_read_only_mode(self):
        with Storage1000(path) as db:
            # test if ok in write mode
            db.add((0,), (0, 0))
        try:
            with Storage1000(path, read_only=True) as db:
                db.add((0,), (0, 0))
        except WriteInReadOnlyModeError:
            return
        raise AssertionError('multiple writers allowed')

    def test_storage_full(self):
        r = random.randint
        with Storage1000(path) as db:
            for i in xrange(1000):
                key = r(0, 10000),
                val = r(0, 10000), r(0, 10000)
                db.add(key, val)
            try:
                db.add(key, val)
            except StorageIsFullError:
                return
        raise AssertionError('storage is full, but error was not rised')


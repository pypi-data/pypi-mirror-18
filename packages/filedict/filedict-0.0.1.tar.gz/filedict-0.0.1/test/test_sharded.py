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

from filedict import *


class Storage(BaseShardedStorage):
    max_records = 100
    key_types = ctypes.c_uint32,
    val_types = ctypes.c_uint32,


path = os.path.join(
    tempfile.gettempdir(),
    'filedict_{}'.format(random.randint(1000000, 9999999))
)


class SmokeTestCase(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_add_items(self):
        with Storage(path) as db:
            keys = set()
            vals = set()
            for i in xrange(500):
                key, val = random.randint(0, 100000), random.randint(0, 100000)
                key, val = (key,), (val,)
                keys.add(key)
                vals.add(val)
                db.add(key, val)

            for key, val in db.items():
                assert key in keys
                assert val in vals

    def test_add_values(self):
        with Storage(path) as db:
            vals = []
            key = 0,
            for i in xrange(150):
                val = random.randint(0, 100000),
                vals.append(val)
                db.add(key, val)
            _vals = list(db.values(key))
            assert len(_vals) == len(vals)
            assert not (set(_vals) - set(vals))
            assert not list(db.values((1,)))

    def test_len_del_defragmentation(self):
        with Storage(path) as db:
            k1, v1 = (1000000,), (1000000,)
            k2, v2 = (2000000,), (2000000,)
            for i in xrange(200):
                key, val = random.randint(0, 100000), random.randint(0, 100000)
                key, val = (key,), (val,)
                db.add(key, val)
                db.add(k1, v1)
                db.add(k2, v2)
            assert db.deleted_count == 0
            assert len(db) == 600
            assert db.del_value(k1, v1) == 200
            assert len(db) == 400
            assert db.deleted_count == 200
            assert db.del_key(k2) == 200
            assert len(db) == 200
            assert db.deleted_count == 400
            db.defragmentation()
            assert len(db) == 200
            assert db.deleted_count == 0

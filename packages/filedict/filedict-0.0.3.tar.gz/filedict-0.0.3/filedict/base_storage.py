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
import struct
import hashlib

import filelock

from .file_counter import FileCounter
from .storage_file import StorageFile


def storage_factory(storage_class, max_records, key_types, val_types):
    mr = max_records
    kt = key_types
    vt = val_types

    class DynamicStorage(storage_class):
        max_records = mr
        key_types = kt
        val_types = vt

    return DynamicStorage


class BaseStorageError(Exception):
    pass


class RequiredAttrNotExistsError(BaseStorageError):
    pass


class WriteInReadOnlyModeError(BaseStorageError):
    pass


class StorageIsFullError(BaseStorageError):
    pass


class CopyAlreadyExistsError(BaseStorageError):
    pass


class NotOpenedError(BaseStorageError):
    pass


class _BaseStorage(object):
    def _assert_required_attrs(self):
        if not hasattr(self, 'max_records'):
            raise RequiredAttrNotExistsError('self.max_records not specified!')
        if not hasattr(self, 'key_types'):
            raise RequiredAttrNotExistsError('self.key_types not specified!')
        if not hasattr(self, 'val_types'):
            raise RequiredAttrNotExistsError('self.val_types not specified!')

    def _assert_read_only(self):
        if self._read_only:
            raise WriteInReadOnlyModeError('Write in read only mode!')

    def _assert_not_opened(self):
        if not self._opened:
            raise NotOpenedError('Call open method first!')

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def copy(self, path, read_count=100):
        self._assert_not_opened()
        if os.path.exists(path):
            raise CopyAlreadyExistsError('Copy path already exists!')
        with self.__class__(path, read_count=read_count) as copy:
            for key, val in self.items():
                copy.add(key, val)

    def copy_to_storage(self, storage):
        self._assert_not_opened()
        with storage:
            for key, val in self.items():
                storage.add(key, val)


class BaseStorage(_BaseStorage):
    _REC = 'r'  # Record marker
    _DEL = 'd'  # Deleted record marker
    _LEN = 1  # Length of marker
    _LOCK_TIMEOUT = 10
    _EMPTY = 0
    _DELETED = 1

    def __init__(self, path, read_only=False, read_count=100):
        self._assert_required_attrs()
        self._read_count = read_count
        self._read_only = read_only
        self._lock = None
        self._opened = False
        self._key_format = ''.join([t._type_ for t in self.key_types])
        self._val_format = ''.join([t._type_ for t in self.val_types])
        self._key_size = struct.calcsize(self._key_format)
        self._val_size = struct.calcsize(self._val_format)
        self._rec_size = self._key_size + self._val_size + self._LEN
        self._path = path
        if not os.path.exists(path):
            os.makedirs(path)

    def _init_files(self):
        self._file = StorageFile(
            os.path.join(self._path, 'storage.bin'),
            self.max_records,
            self._rec_size
        )
        self._stat = FileCounter(os.path.join(self._path, 'statistics.json'))
        self._stat['max'] = self.max_records
        self._stat['live'] = self._stat['live']
        self._stat['del'] = self._stat['del']

    def open(self):
        if self._opened:
            return
        if not self._read_only:
            self._lock = filelock.FileLock(os.path.join(self._path, 'lock'))
            self._lock.acquire(timeout=self._LOCK_TIMEOUT)
        self._init_files()
        self._opened = True

    def close(self):
        if not self._opened:
            return
        self._file.close()
        if not self._read_only:
            self._stat.flush()
            self._lock.release()
        self._opened = False

    def hash(self, s):
        return int(hashlib.sha1(s).hexdigest(), 16)

    def _hash(self, s):
        return self.hash(s) % self.max_records

    def _key(self, key):
        return struct.pack(self._key_format, *key)

    def _val(self, val):
        return struct.pack(self._val_format, *val)

    def _seek(self, key):
        key = self._key(key)
        idx = self._hash(key)
        self._file.seek(idx)

    def _del(self, seek_back=True):
        self._file.write_raw(self._DEL, seek_back=seek_back)
        self._stat['del'] += 1
        self._stat['live'] -= 1

    def _next(self, n, circular=True):
        recs = self._file.read(n, circular=circular)
        for rec in recs:
            a, b = self._LEN, self._LEN + self._key_size
            marker, key, val = rec[:a], rec[a:b], rec[b:]
            if marker == self._DEL:
                yield self._DELETED, None
            elif marker != self._REC:
                yield self._EMPTY, None
            else:
                key = struct.unpack(self._key_format, key)
                val = struct.unpack(self._val_format, val)
                yield key, val

    def _iter(self, max_circles=1):
        count = 0
        while True:
            for item in self._next(self._read_count):
                yield item
                count += 1
                if count >= max_circles * self.max_records:
                    return

    def values(self, key):
        self._assert_not_opened()
        key = tuple(key)
        self._seek(key)
        for k, v in self._iter():
            if k == self._EMPTY:
                return
            elif k == key:
                yield v

    def add(self, key, val):
        self._assert_not_opened()
        self._assert_read_only()
        rec = self._REC + struct.pack(self._key_format, *key) + \
            struct.pack(self._val_format, *val)
        self._seek(key)
        idx = self._file.idx
        for i, (k, v) in enumerate(self._iter()):
            if k == self._EMPTY or k == self._DELETED:
                self._file.seek(idx + i)
                self._file.write((rec,))
                self._stat['live'] += 1
                if k == self._DELETED:
                    self._stat['del'] -= 1
                return
        raise StorageIsFullError('Storage is full!')

    def defragmentation(self):
        self._assert_not_opened()
        self._assert_read_only()
        path = self._path + '.defragmentation'
        self.copy(path)
        self._file.close()
        shutil.rmtree(self._path)
        shutil.move(path, self._path)
        self._init_files()

    def fix_statistis(self):
        self._assert_not_opened()
        self._assert_read_only()
        self._file.seek(0)
        self._stat['live'] = 0
        self._stat['del'] = 0
        for k, v in self._iter():
            if k == self._DELETED:
                self._stat['del'] += 1
            elif k != self._EMPTY:
                self._stat['live'] += 1

    def items(self):
        self._assert_not_opened()
        self._file.seek(0)
        for k, v in self._iter():
            if k == self._EMPTY or k == self._DELETED:
                continue
            yield k, v

    def _del_many(self, key, condition):
        self._seek(key)
        idx = self._file.idx
        count = 0
        for i, (k, v) in enumerate(self._iter()):
            if k == self._EMPTY:
                break
            if condition(k, v):
                _idx = self._file.idx
                self._file.seek(idx + i)
                self._del(seek_back=False)
                self._file.seek(_idx)
                count += 1
        return count

    def _update_stat(self):
        if self._read_only:
            self._stat = FileCounter(
                os.path.join(self._path, 'statistics.json')
            )

    def del_value(self, key, val):
        self._assert_not_opened()
        self._assert_read_only()
        key = tuple(key)
        val = tuple(val)

        def condition(k, v):
            return k == key and v == val
        return self._del_many(key, condition)

    def del_key(self, key):
        self._assert_not_opened()
        self._assert_read_only()
        key = tuple(key)

        def condition(k, v):
            return k == key
        return self._del_many(key, condition)

    def __len__(self):
        self._assert_not_opened()
        self._update_stat()
        return self._stat['live']

    @property
    def deleted_count(self):
        self._assert_not_opened()
        self._update_stat()
        return self._stat['del']

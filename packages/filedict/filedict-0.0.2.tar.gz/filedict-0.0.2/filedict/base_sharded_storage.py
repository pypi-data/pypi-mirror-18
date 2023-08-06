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

from .base_storage import storage_factory, _BaseStorage, BaseStorage


class BaseShardedStorage(_BaseStorage):
    shard_name_width = 5
    max_shard_fulness = 0.9

    def __init__(self, path, read_only=False, read_count=100):
        self._assert_required_attrs()
        self._shards = []
        self._storage_class = storage_factory(
            BaseStorage,
            self.max_records,
            self.key_types,
            self.val_types
        )
        if not os.path.exists(path):
            os.makedirs(path)
        for name in os.listdir(path):
            if len(name) != self.shard_name_width:
                continue
            if not name.isdigit():
                continue
            _path = os.path.join(path, name)
            self._shards.append((int(name), self._storage_class(
                _path,
                read_only=read_only,
                read_count=read_count
            )))
        self._shards.sort()
        if not self._shards:
            self._shards.append((0, self._storage_class(
                os.path.join(path, '0' * self.shard_name_width),
                read_only=read_only,
                read_count=read_count
            )))
        self._path = path
        self._read_only = read_only
        self._read_count = read_count
        self._opened = False

    def open(self):
        if self._opened:
            return
        for idx, shard in self._shards:
            shard.open()
        self._opened = True

    def close(self):
        if not self._opened:
            return
        for idx, shard in self._shards:
            shard.close()
        self._opened = False

    def values(self, key):
        self._assert_not_opened()
        for idx, shard in self._shards:
            for item in shard.values(key):
                yield item

    def add(self, key, val):
        self._assert_not_opened()
        idx, shard = self._shards[-1]
        if len(shard) > self.max_shard_fulness * self.max_records:
            self._shards.append((idx + 1, self._storage_class(
                os.path.join(
                    self._path,
                    '%0{}d'.format(self.shard_name_width) % (idx + 1)
                ),
                read_only=self._read_only,
                read_count=self._read_count
            )))
            idx, shard = self._shards[-1]
            shard.open()
        return shard.add(key, val)

    def defragmentation(self):
        self._assert_not_opened()
        for idx, shard in self._shards:
            shard.defragmentation()

    def fix_statistis(self):
        self._assert_not_opened()
        for idx, shard in self._shards:
            shard.fix_statistis()

    def items(self):
        self._assert_not_opened()
        for idx, shard in self._shards:
            for item in shard.items():
                yield item

    def del_value(self, key, val):
        self._assert_not_opened()
        count = 0
        for idx, shard in self._shards:
            count += shard.del_value(key, val)
        return count

    def del_key(self, key):
        self._assert_not_opened()
        count = 0
        for idx, shard in self._shards:
            count += shard.del_key(key)
        return count

    def __len__(self):
        self._assert_not_opened()
        count = 0
        for idx, shard in self._shards:
            count += len(shard)
        return count

    @property
    def deleted_count(self):
        self._assert_not_opened()
        count = 0
        for idx, shard in self._shards:
            count += shard.deleted_count
        return count

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


class StorageFileError(Exception):
    pass


class WrongFileSizeError(StorageFileError):
    pass


class UnableToSeekError(StorageFileError):
    pass


class UnableToReadError(StorageFileError):
    pass


class UnableToWriteError(StorageFileError):
    pass


class UnableToWriteRawError(StorageFileError):
    pass


class StorageFile(object):
    def __init__(self, path, count, size):
        self._count = count
        self._size = size
        self._filesize = count * size
        self._path = os.path.abspath(path)
        if not os.path.exists(self._path):
            with open(self._path, 'wb') as fd:
                fd.truncate(self._filesize)
        if os.path.getsize(self._path) != self._filesize:
            raise WrongFileSizeError('Wrong filesize!')
        self._fd = open(self._path, 'rb+')
        self.idx = 0

    def close(self):
        self._fd.close()

    def seek(self, idx, relative=False):
        if relative:
            idx += self.idx
        idx %= self._count
        if idx >= self._count:
            raise UnableToSeekError('Unable to seek to index {}!'.format(idx))
        self._fd.seek(idx * self._size)
        self.idx = idx

    def read(self, count, circular=False):
        if count <= 0:
            raise UnableToReadError('Can read only >0 items!')
        sz = self._size
        buf = self._fd.read(sz * count)
        m = len(buf) / sz
        n = min(count, self._count - self.idx)
        if m != n:
            raise UnableToReadError('The idx property is not synchronized!')
        self.idx += n
        result = [buf[i:i + sz] for i in range(0, len(buf), sz)]
        if n < count and circular:
            self._fd.seek(0)
            self.idx = 0
            result.extend(self.read(count - n, circular=True))
        return result

    def write(self, items):
        n = len(items)
        if self.idx + n > self._count:
            raise UnableToWriteError('Too many items to write!')
        buf = ''.join(items)
        if len(buf) != self._size * n:
            raise UnableToWriteError('Wrong items in write method!')
        self._fd.write(buf)
        self.idx += n

    def write_raw(self, s, seek_back=True):
        if self.idx * self._size + len(s) > self._filesize:
            raise UnableToWriteRawError('Too long string to write inplace!')
        self._fd.write(s)
        if seek_back:
            self._fd.seek(-len(s), whence=os.SEEK_CUR)

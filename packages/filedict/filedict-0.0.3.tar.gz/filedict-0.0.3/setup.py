"""
filedict
--------

Fast & simple key-value storage.

Description:
  - This storage is something like Redis/Memcache, but in-file. It's not so fast as in-memory cache, but it's still quite fast and also can store huge amount of data.

Features:
  - Simple in-file hash table.
  - Can store billions of records providing really fast access.
  - Use disk space effectively.
  - Use a little bit RAM.
  - Support both add & del operations.
  - Support defragmentation, copy operation.
  - No limits to readers number.
  - Support multiple values for single key.
  - Get value for given key only in 1 seek + 1 read (in best case, if keys are quite unique).
  - Supports local sharding.

Limitations:
  - Only python2, only linux for now.
  - Max number of records is constant for any database. So it can be choosen only once.
  - Supports only fixed data schema.
  - Can store only integers & floats.
  - Very slow in case of huge amount of duplicate keys.
  - Only one writer allowed.
  - No transactions, no ACID support.
  - If your data can be placed in RAM, use Redis/Memcache instead!
  - Not distributed.

"""
from setuptools import setup, find_packages

setup(
    name='filedict',
    version='0.0.3',
    author='David Kuryakin',
    author_email='dkuryakin@gmail.com',
    url='https://bitbucket.org/dkuryakin/filedict',
    download_url = 'https://bitbucket.org/dkuryakin/filedict/get/master.tar.gz',
    license='unlicense',
    description='Fast & simple key-value storage.',
    keywords=['storage', 'hash table', 'key value', 'database'],
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    test_suite = 'filedict.test',
    packages=['filedict', 'filedict.test'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'filelock>=2.0.7'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Database Engines/Servers'
    ],
)

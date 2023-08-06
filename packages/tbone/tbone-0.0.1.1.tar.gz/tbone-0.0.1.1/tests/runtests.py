#!/usr/bin/env python
# encoding: utf-8

import sys
import tornado.testing
from tornado.options import define, options
import unittest
from pymongo import Connection


sys.path.append('tbone')

settings = {
    'db': {
        'name': 'tbone',
        'reconnect_tries': 5,
        'reconnect_timeout': 2
    }
}


TEST_MODULES = [
    'tests.models'
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


if __name__ == '__main__':
    # create database
    connection = Connection()
    print('\ncreating database ... \n')
    db = connection['test_{}'.format(options['db_name'])]
    tornado.testing.main(verbosity=2, exit=False)
    print('\nDeleting database\n')
    connection.drop_database('test_{}'.format(options['db_name']))
    print('\nDone\n')


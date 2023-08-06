#! /usr/env/bin python
# -*- coding: utf-8 -*-

"""psql.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import pytest

from strumenti import psql


# Test table_create
table_create = {'default': ({'name': 'test', 'schema': ['value, TEXT']},
                            'CREATE TABLE test (value, TEXT);'),
                'serial': ({'name': 'test', 'schema': ['value, TEXT'],
                            'serial': True},
                           ('CREATE TABLE test (id SERIAL UNIQUE NOT NULL '
                            'PRIMARY KEY, value, TEXT);')),
                'unique': ({'name': 'test', 'schema': ['value, TEXT'],
                            'serial': True, 'unique': ['value']},
                           ('CREATE TABLE test (id SERIAL UNIQUE NOT NULL '
                            'PRIMARY KEY, value, TEXT, UNIQUE (value));')),
                'multi': ({'name': 'test', 'schema': ['value1, TEXT',
                                                      'value2, DATE']},
                          'CREATE TABLE test (value1, TEXT, value2, DATE);'),
                }


@pytest.mark.parametrize('kwargs, expected',
                         list(table_create.values()),
                         ids=list(table_create.keys()))
def test__table_create(kwargs, expected):
    assert psql.table_create(**kwargs) == expected

# Test table_drop
table_drop = {'default': ('test', 'test'),
              }


@pytest.mark.parametrize('name, expected',
                         list(table_drop.values()),
                         ids=list(table_drop.keys()))
def test__table_drop(name, expected):
    assert (psql.table_drop(name) ==
            'DROP TABLE if EXISTS {} CASCADE;'.format(expected))


# Test table_insert
table_insert = {'str field': ({'name': 'test', 'field_names': 'one'},
                              ('one', '%s')),
                'list field': ({'name': 'test',
                                'field_names': ['one', 'two']},
                               ('one, two', '%s,%s')),
                }


@pytest.mark.parametrize('kwargs, expected',
                         list(table_insert.values()),
                         ids=list(table_insert.keys()))
def test__table_insert(kwargs, expected):
    assert (' '.join(psql.table_insert(**kwargs).split()) ==
            'INSERT INTO test ({}) VALUES ({});'.format(*expected))


# Test table_select
table_select = {'default': ({'table_name': 'test'}, ('*', 'test', '')),
                'return field': ({'table_name': 'test', 'return_field': 'col'},
                                 ('col', 'test', '')),
                'search_field': ({'table_name': 'test', 'search_field': 'col'},
                                 ('*', 'test', 'WHERE col=%s')),
                }


@pytest.mark.parametrize('kwargs, expected',
                         list(table_select.values()),
                         ids=list(table_select.keys()))
def test__table_select(kwargs, expected):
    cmd = 'SELECT {} FROM {} {};'.format(*expected)
    assert psql.table_select(**kwargs) == cmd

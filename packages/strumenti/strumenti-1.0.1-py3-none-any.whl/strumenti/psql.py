#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""PostgreSQL Module

Utilities for interfacing with PostgreSQL databases.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

from typing import List, Union

import psycopg2


def connection(db_name: str, user: str,
               password: str) -> psycopg2.extensions.cursor:
    """Connect to PostgreSQL database and establish a cursor.

    :param str db_name: database name
    :param str user: database user name
    :param str password: database user password
    :returns: cursor to PostgreSQL database
    :rtype: psycopg2.extensions.cursor
    """
    conn = psycopg2.connect(database=db_name, user=user, password=password)
    return conn.cursor()


def table_create(name: str, schema: List[str], serial: bool=False,
                 unique: Union[List[str], None]=None) -> str:
    """Return command to create a table in a PostgreSQL database.

    :param str name: name of table
    :param list schema: schema of table provided in name data type pairs \
        ['n_1, dt_1', 'n_2, dt_2']
    :param bool serial: a serialized index will be created for the table \
        and used as the primary key if True
    :param list unique: field names that define a unique record for the table
    :return: command to create a table
    :rtype: str
    """
    base_cmd = 'CREATE TABLE {name} ('.format(name=name)

    if serial:
        serial_cmd = 'id SERIAL UNIQUE NOT NULL PRIMARY KEY, '
    else:
        serial_cmd = ''

    schema_cmd = ', '.join(schema)

    if unique:
        unique_cmd = ', UNIQUE ({fields})'.format(fields=', '.join(unique))
    else:
        unique_cmd = ''

    return '{base}{serial}{schema}{unique});'.format(base=base_cmd,
                                                     serial=serial_cmd,
                                                     schema=schema_cmd,
                                                     unique=unique_cmd)


def table_drop(name: str) -> str:
    """Return command to drop a table from a PostgreSQL database.

    :param str name: name of table to drop
    :returns: command to remove table from database
    :rtype: str
    """
    return 'DROP TABLE if EXISTS {name} CASCADE;'.format(name=name)


def table_insert(name: str, field_names: Union[str, List[str]]) -> str:
    """Return command to add a record into a PostgreSQL database.


    :param str name: name of table to append
    :param field_names: names of fields
    :type: str or list
    :return: command to append records to a table
    :rtype: str

    Example:

    import psql

    cur = psql.connection('db', 'user', 'password')
    [cur.execute(psql.table_insert('table', 'field'), (x, )) for x in values]
    """
    if isinstance(field_names, str):
        field_names = [field_names]

    length = len(field_names)
    if length > 1:
        values = ','.join(['%s'] * length)
    else:
        values = '%s'

    return '''INSERT INTO {table_name} ({fields})
              VALUES ({values});'''.format(table_name=name,
                                           fields=', '.join(field_names),
                                           values=values)


def table_select(table_name: str, return_field: str='*',
                 search_field: Union[str, None]=None) -> str:
    """Return values from a Postgres table with a given search value.

    :param str table_name: name of table to search
    :param str return_field: field to return from table query (default: * \
        will return all table fields)
    :param str search_field: field to search for value in table (default: \
    None will return all table values)
    :returns: value corresponding to requested field
    :rtype: str

    Example:

    import psql

    cur = psql.connection('db', 'user', 'password')
    [cur.execute(psql.table_select('table', search_field='idx'), (x, )) \
     for x in values]
    """
    base_cmd = 'SELECT {} FROM {}'.format(return_field, table_name)

    if search_field:
        search_cmd = 'WHERE {}=%s'.format(search_field)
    else:
        search_cmd = ''

    return '{} {};'.format(base_cmd, search_cmd)

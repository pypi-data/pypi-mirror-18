#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""system.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import logging
import os
import os.path as osp
import shutil
import subprocess

import pytest
import numpy as np

from strumenti.tests.fixtures import \
    ChromalogLogCapture
from strumenti import system


lines = ['a\tb\tc\td\n', '\n', '1\t2\t3\t4\n', '5\t6\t7\t8\n']


# Test check_list
check_list = {'string': ('test', ['test']),
              'tuple': (('test', 'tuple'), ['test', 'tuple']),
              'list': (['test', 'list'], ['test', 'list']),
              }


@pytest.mark.parametrize('variable, expected',
                         list(check_list.values()),
                         ids=list(check_list.keys()))
def test__check_list(variable, expected):
    assert system.check_list(variable) == expected


# Test get_header
get_header = {'defaults': ({'path': 'test.txt', 'header_row': 0},
                           ['a', 'b', 'c', 'd']),
              'row 2': ({'path': 'test.txt', 'header_row': 2},
                        ['1', '2', '3', '4']),
              'row 2 str': ({'path': 'test.txt', 'header_row': '2'},
                            ['1', '2', '3', '4']),
              }


@pytest.fixture()
def fixture_get_header(tmpdir):
    tmpdir.chdir()
    with open('test.txt', 'w') as f:
        f.write(''.join(lines))

    with open('test_no_header.txt', 'w') as f:
        f.write(''.join(lines[2:]))


@pytest.mark.usefixtures('fixture_get_header')
@pytest.mark.parametrize('kwargs, expected',
                         list(get_header.values()),
                         ids=list(get_header.keys()))
def test__get_header(kwargs, expected):
    assert system.get_header(**kwargs) == expected


# Test flatten
flatten = {'lists ints floats': ([[1, 2, 3], [4, 5, 6], [7., 8., 9.]],
                                 [1, 2, 3, 4, 5, 6, 7, 8, 9]),
           'lists str': ([['this'], ['is'], ['a'], ['test']],
                         ['this', 'is', 'a', 'test']),
           'list int str': ([[1, 2, 3], 4, 'test'], [1, 2, 3, 4, 'test']),
           'lists empty': ([[1, 2, 3], [], [7, 8, 9]], [1, 2, 3, 7, 8, 9]),
           'tuples floats': ([(1, 2, 3), (4, 5, 6), (7, 8, 9)],
                             [1, 2, 3, 4, 5, 6, 7, 8, 9]),
           }


@pytest.mark.parametrize('matrix, expected',
                         list(flatten.values()),
                         ids=list(flatten.keys()))
def test__flatten(matrix, expected):
    assert system.flatten(matrix) == expected


def test__flatten_empty():
    with pytest.raises(TypeError):
        system.flatten()


# Test logger_setup
output = (('test', 'DEBUG', 'debug'),
          ('test', 'INFO', 'info'),
          ('test', 'WARNING', 'warning'),
          ('test', 'ERROR', 'error'),
          ('test', 'CRITICAL', 'critical'))
logger_setup = {'debug': ({'name': 'test', 'master_level': logging.DEBUG},
                          output),
                'info': ({'name': 'test', 'master_level': logging.INFO},
                         output[1:]),
                'warning': ({'name': 'test', 'master_level': logging.WARNING},
                            output[2:]),
                'error': ({'name': 'test', 'master_level': logging.ERROR},
                          output[3:]),
                'critical': ({'name': 'test',
                              'master_level': logging.CRITICAL},
                             output[-1:]),
                'file': ({'log_file': 'test.log', 'name': 'test_file',
                          'master_level': logging.CRITICAL},
                         (('test_file', 'CRITICAL', 'critical'),))
                }


@pytest.mark.parametrize('kwargs, expected',
                         list(logger_setup.values()),
                         ids=list(logger_setup.keys()))
def test__logger_setup(tmpdir, kwargs, expected):
    tmpdir.chdir()
    with ChromalogLogCapture() as log_cap:
        logger = system.logger_setup(**kwargs)
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')
    log_cap.filter_records()
    log_cap.check(*expected)

    if 'log_file' in kwargs.keys():
        assert osp.isfile('test.log')


# Test load_file
load_file = {'lines': ({'path': 'test.txt'},
                       ['line one\n', 'line two\n', 'line three\n']),
             'str': ({'path': 'test.txt', 'all_lines': False},
                     'line one\nline two\nline three\n'),
             'first n lines': ({'path': 'test.txt', 'all_lines': False,
                                'first_n_lines': 2},
                               ['line one\n', 'line two\n']),
             }


@pytest.fixture(scope='session')
def load_file_setup():
    file_name = 'test.txt'
    with open(file_name, 'w') as f:
        f.write('line one\n')
        f.write('line two\n')
        f.write('line three\n')
    return file_name


@pytest.mark.usefixtures('load_file_setup')
@pytest.mark.parametrize('kwargs, expected',
                         list(load_file.values()),
                         ids=list(load_file.keys()))
def test__load_file(kwargs, expected):
    actual = system.load_file(**kwargs)
    assert actual == expected


# Test load_record
load_record = {'header': ({'path': 'test.txt', 'header_row': 0,
                           'skip_rows': 2},
                          'a', np.array([1.0, 5.0]),
                          'd', np.array([4.0, 8.0])),
               'header some cols': ({'path': 'test.txt', 'header_row': 0,
                                     'skip_rows': 2, 'cols': (0, 3)},
                                    'a', np.array([1.0, 5.0]),
                                    'd', np.array([4.0, 8.0])),
               'header formats': ({'path': 'test.txt', 'header_row': 0,
                                   'skip_rows': 2,
                                   'formats': ('f8', 'i4', 'f8', 'i4')},
                                  'a', np.array([1.0, 5.0]),
                                  'd', np.array([4, 8])),
               'no header some cols': ({'path': 'test_no_header.txt',
                                        'cols': (0, 3)},
                                       '0', np.array([1.0, 5.0]),
                                       '3', np.array([4.0, 8.0])),
               'no header formats': ({'path': 'test_no_header.txt',
                                      'names': ('one', 'two', 'three',
                                                'four')},
                                     'one', np.array([1.0, 5.0]),
                                     'four', np.array([4.0, 8.0])),
               }


@pytest.fixture()
def load_record_setup():
    with open('test.txt', 'w') as f:
        f.write(''.join(lines))

    with open('test_no_header.txt', 'w') as f:
        f.write(''.join(lines[2:]))


@pytest.mark.usefixtures('load_record_setup')
@pytest.mark.parametrize(('kwargs, a_key, a_expect, d_key, d_expect'),
                         list(load_record.values()),
                         ids=list(load_record.keys()))
def test__load_records(kwargs, a_key, a_expect, d_key, d_expect):
    output = system.load_records(**kwargs)
    assert np.all(output[a_key] == a_expect)
    assert np.all(output[d_key] == d_expect)


# Test preserve_cwd
@pytest.fixture()
def preserve_cwd_setup(request):
    original_dir = os.getcwd()
    working_dir = osp.join(original_dir, 'junk')
    file_name = 'junk.txt'

    os.makedirs(working_dir, exist_ok=True)

    def teardown():
        shutil.rmtree(working_dir)
    request.addfinalizer(teardown)
    return {'original_dir': original_dir, 'working_dir': working_dir,
            'file_name': file_name}


def test__preserve_cwd(preserve_cwd_setup):

    @system.preserve_cwd(preserve_cwd_setup['working_dir'])
    def test():
        with open(preserve_cwd_setup['file_name'], 'w') as f:
            f.close()

    test()
    assert osp.isfile(osp.join(preserve_cwd_setup['working_dir'],
                               preserve_cwd_setup['file_name']))
    assert os.getcwd() == preserve_cwd_setup['original_dir']


# Test status
def test__status(capsys):

    @system.status()
    def print_num():
        print('1, 2, 3')

    print_num()
    out, err = capsys.readouterr()
    assert out.split()[:-1] == ['Execute:', 'print_num', '1,', '2,', '3',
                                'Completed:', 'print_num', '(runtime:']


# Test unzip
@pytest.fixture(scope='function')
def unzip_setup(request):
    file_name = 'junk.txt'
    with open(file_name, 'w') as f:
        f.write('Test file')
    subprocess.call(['gzip', file_name])

    def teardown():
        os.remove(file_name)
    request.addfinalizer(teardown)
    return file_name


def test__unzip(unzip_setup):
    system.unzip_file('{}.gz'.format(unzip_setup))
    with open(unzip_setup, 'r') as f:
        text = f.read()
    assert 'Test file' == text


# Test walk_dir
class TestWalkDir:

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        tmpdir.chdir()

        self.main_dir = osp.join(os.getcwd(), 'test_walk_dir')
        self.extra_dir = osp.join(self.main_dir, 'extra')

        os.makedirs(self.extra_dir, exist_ok=True)

        @system.preserve_cwd(self.main_dir)
        def make_files_1():
            with open('main.png', 'w') as f:
                f.write('.png file in main directory.')
            with open('main.jpeg', 'w') as f:
                f.write('.jpeg file in main directory.')

        @system.preserve_cwd(self.extra_dir)
        def make_files_2():
            with open('extra.png', 'w') as f:
                f.write('.png file in extra directory.')
            with open('extra.inp', 'w') as f:
                f.write('.inp file in extra directory.')

        os.chdir(self.main_dir)
        make_files_1()
        make_files_2()

    def test__no_files_to_find(self):
        assert system.walk_dir('.txt') == []

    def test__find_main_dir_only(self):
        assert system.walk_dir('.jpeg') == [osp.join(self.main_dir,
                                                     'main.jpeg')]

    def test__find_extra_dir_only(self):
        assert (system.walk_dir('.inp') ==
                [osp.join(self.main_dir, self.extra_dir, 'extra.inp')])

    def test__find_both_dirs(self):
        assert (system.walk_dir('.png') ==
                [osp.join(self.main_dir, self.extra_dir, 'extra.png'),
                 osp.join(self.main_dir, 'main.png')])


# Test zip_file
@pytest.fixture(scope='function')
def zip_setup(tmpdir):
    tmpdir.chdir()
    file_name = 'junk.txt'
    with open(file_name, 'w') as f:
        f.write('Test file')

    return file_name


def test__zip_file(zip_setup):
    system.zip_file(zip_setup)
    subprocess.call(['gunzip', '{}.gz'.format(zip_setup)])
    with open(zip_setup, 'r') as f:
        text = f.read()
    assert 'Test file' == text

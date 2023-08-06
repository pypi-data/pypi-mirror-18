#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""notify.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import pytest

from strumenti import notify

# Test astrix_line
astrix_line = {'qty = float': (5.8, '*****\n'),
               'qty = int': (10, '**********\n'),
               'qty = str': ('10', '**********\n'),
               'qty = defaults': (80, '*' * 80 + '\n'),
               }


@pytest.mark.parametrize('qty, expected',
                         list(astrix_line.values()),
                         ids=list(astrix_line.keys()))
def test__astrix_line(qty, expected):
    assert notify.astrix_line(qty) == expected


# Test center
center = {'one word': ({'statement': 'one', 'fill': '=', 'width': 7},
                       '\n= one ='),
          'two words': ({'statement': 'one two', 'fill': '=', 'width': 11},
                        '\n= one two =')
          }


@pytest.mark.parametrize('kwargs, expected',
                         list(center.values()),
                         ids=list(center.keys()))
def test__center(kwargs, expected):
    assert notify.center(**kwargs) == expected


def test__center_empty():
    with pytest.raises(TypeError):
        notify.center()


# Test header
header = {'module': ('test', '*' * 80 + '\n' * 3 + 'test\n'),
          }


@pytest.mark.parametrize('stmt, expected',
                         list(header.values()),
                         ids=list(header.keys()))
def test_header(stmt, expected):
    assert notify.header(stmt) == expected


def test__header_empty():
    with pytest.raises(TypeError):
        notify.header()


# Test footer
footer = {'module': ('test', '\n' * 2 + 'test\n' + '*' * 80 + '\n'),
          }


@pytest.mark.parametrize('stmt, expected',
                         list(footer.values()),
                         ids=list(footer.keys()))
def test__footer(stmt, expected):
    assert notify.footer(stmt) == expected


def test__footer_empty():
    with pytest.raises(TypeError):
        notify.footer()


# Test section_break
section_break = {'qty = defaults': (2, '\n' * 2),
                 'qty = string': ('10', '\n' * 10),
                 'qty = float': (10.0, '\n' * 10),
                 'qty = int': (10, '\n' * 10),
                 }


@pytest.mark.parametrize('qty, expected',
                         list(section_break.values()),
                         ids=list(section_break.keys()))
def test__section_break(qty, expected):
    assert notify.section_break(qty) == expected


# Test status
status = {'one word': ({'statement': 'one', 'fill': '-', 'width': 7},
                       '- One -'),
          'two words': ({'statement': 'one two', 'fill': '-', 'width': 11},
                        '- One Two -'),
          }


@pytest.mark.parametrize('kwargs, expected',
                         list(status.values()),
                         ids=list(status.keys()))
def test__status(kwargs, expected):
    assert notify.status(**kwargs).strip() == expected


def test__status_empty():
    with pytest.raises(TypeError):
        notify.status()


# Test warn
warn = {'1 word': ({'statement': 'one'},
                   '\n' + '!' * 27 + ' ONE ' + '!' * 28),
        '2 word': ({'statement': 'one two'},
                   ('\n' + '!' * 25 + ' ONE TWO ' +
                    '!' * 26)),
        }


@pytest.mark.parametrize('kwargs, expected',
                         list(warn.values()),
                         ids=list(warn.keys()))
def test__warn(kwargs, expected):
    assert notify.warn(**kwargs) == expected


def test__warn_empty():
    with pytest.raises(TypeError):
        notify.warn()

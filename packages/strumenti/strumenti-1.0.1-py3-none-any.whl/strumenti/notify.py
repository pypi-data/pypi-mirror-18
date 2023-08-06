#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Notify Module

Functions for notifying the user are contained in this module.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""


def astrix_line(qty: int=80) -> str:
    """Return break line of astrix characters.

    :param int qty: number of * characters to be returned
    :returns: * characters and a line break
    :rtype: str
    """
    return '*' * int(qty) + '\n'


def center(statement: str, fill: str='=', width: int=60) -> str:
    """Return statement centered by spaces and fill characters.

    :param str statement: statement to be returned
    :param str fill: fill character to be used (default: =)
    :param int width: total width of output string (default: 60)
    :returns: statement centered on line surrounded by fill characters
    :rtype: str
    """
    stmt_str = statement.center(len(statement) + 2)
    return '\n' + stmt_str.center(width, fill)


def header(statement: str) -> str:
    """Return a line of asterisks two blank lines and the header statement.

    :param str statement: header statement
    :returns: formatted header statement
    :rtype: str
    """
    return ''.join((astrix_line(), section_break(), statement, '\n'))


def footer(statement: str) -> str:
    """Return two blank lines the footer statement then a row of asterisks.

    :param str statement: footer statement
    :returns: formatted footer statement
    :rtype: str
    """
    return ''.join((section_break(), statement, '\n', astrix_line()))


def section_break(qty: int=2) -> str:
    """Return multiple line break characters.

    :param int qty: number of line break characters (default: 2)
    :returns: multiple new line characters
    :rtype: str
    """
    return '\n' * int(qty)


def status(statement: str, fill: str='-', width: int=40) -> str:
    """Return intermediary statements.

    :param str statement: statement to be returned
    :param str fill: fill character to be used (default: -)
    :param int width: total width of output string (default: 40)
    :returns: formatted status statement
    :rtype: str
    """
    return center(statement.title(), fill=fill, width=width)


def warn(statement: str, fill: str='!') -> str:
    """Return blinking statement formatted in all caps in the color red.

    :param str statement: warning statement
    :param str fill: fill character to be used (default: !)
    :returns: formatted warning statement
    :rtype: str
    """
    stmt = statement.upper()
    return center(stmt, fill=fill)

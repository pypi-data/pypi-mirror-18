#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Modules contains functions for converting coordinate systems.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import sys
from typing import List, Union

import numpy as np

from strumenti import notify


def element_dimension(array: np.ndarray,
                      values: Union[int, List[int]]) -> int:
    """Return the element dimension for array if dimension matches values.

    :param ndarray array: numpy array to test
    :param values: value or values of desired element dimension
    :type: int or list of ints
    :returns: element dimension of array
    :rtype: int
    :raises: IndexError or ValueError

    >>> element_dimension(np.array([[1, 2, 3], [4, 5, 6]]), [2, 3])
    3

    >>> element_dimension(np.array([[1, 2, 3], [4, 5, 6]]), 3)
    3
    """
    if isinstance(values, int):
        values = [values]

    try:
        dim = array.shape[1]
        if dim not in values:
            raise ValueError
    except (IndexError, ValueError):
        str_values = ', '.join([str(x) for x in values])
        notify.warn('ARRAY DIMENSIONS MUST BE: {}').format(str_values)
        sys.exit()

    return dim


def cart2pol(pts: np.ndarray, degrees: bool=False) -> np.ndarray:
    """Convert Cartesian coordinates to polar or cylindrical coordinates.

    :param ndarray pts: array of Cartesian points (x, y) or (x, y, z)
    :param bool degrees: if true results will be presented in degrees \
        (default: False)
    :returns: [radial distance **rho**, azimuthal angle **theta**, (*vertical \
        distance* **z**)]
    :rtype: ndarray

    >>> cart2pol(np.array([[0, 1], [-2, 0]]), degrees=True)
    array([[   1.,   90.],
           [   2.,  180.]])

    >>> cart2pol(np.array([[0.5, -0.5, 4]]), degrees=True)
    array([[  0.70710678, -45.        ,   4.        ]])
    """
    dim = element_dimension(pts, [2, 3])

    rho = np.linalg.norm(pts[:, 0:2], axis=1)
    theta = np.arctan2(pts[:, 1], pts[:, 0])

    if degrees:
        theta = np.degrees(theta)

    if dim == 2:
        return np.c_[rho, theta]
    else:
        return np.c_[rho, theta, pts[:, 2]]


def cart2sphere(pts: np.ndarray, degrees: bool=False) -> np.ndarray:
    """Convert Cartesian coordinates to spherical coordinates.

    :param ndarray pts: array of Cartesian points (x, y, z)
    :param bool degrees: if true results will be presented in degrees \
        (default: False)
    :returns: [radial distance **r**, azimuthal angle **theta**, polar angle
        **phi**]
    :rtype: ndarray

    >>> cart2sphere(np.array([[1, 0, 0], [1, 1, 1]]), degrees=True)
    array([[  1.        ,   0.        ,  90.        ],
           [  1.73205081,  45.        ,  54.73561032]])
    """
    element_dimension(pts, 3)

    r = np.linalg.norm(pts, axis=1)

    pol = cart2pol(pts, degrees)
    rho = pol[:, 0]
    theta = pol[:, 1]
    z = pol[:, 2]

    phi = np.pi / 2 - np.arctan2(z, rho)

    if degrees:
        phi = np.degrees(phi)

    return np.c_[r, theta, phi]


def pol2cart(pts: np.ndarray, degrees: bool=False) -> np.ndarray:
    """Convert polar or cylindrical coordinates to Cartesian coordinates.

    :param ndarray pts: array of polar points (rho, theta) or cylindrical \
        points (rho, theta, phi)
    :param bool degrees: if true results will be presented in degrees \
        (default: False)
    :returns: [x, y, (*z*)]
    :rtype: ndarray

    >>> pol2cart(np.array([[2**0.5, 45], [1, 90]]), degrees=True)
    array([[  1.00000000e+00,   1.00000000e+00],
           [  6.12323400e-17,   1.00000000e+00]])

    >>> pol2cart(np.array([[2**0.5, 45, 1], [1, 90, 2]]), degrees=True)
    array([[  1.00000000e+00,   1.00000000e+00,   1.00000000e+00],
           [  6.12323400e-17,   1.00000000e+00,   2.00000000e+00]])
    """
    dim = element_dimension(pts, [2, 3])

    if degrees:
        pts = pts.astype(float)
        pts[:, 1] = np.radians(pts[:, 1])

    x = pts[:, 0] * np.cos(pts[:, 1])
    y = pts[:, 0] * np.sin(pts[:, 1])

    if dim == 2:
        return np.c_[x, y]
    else:
        return np.c_[x, y, pts[:, 2]]


def sphere2cart(pts: np.ndarray, degrees: bool=False) -> np.ndarray:
    """Convert spherical coordinates to Cartesian coordinates.

    :param ndarray pts: array of spherical coordinates
    :param bool degrees: if true results will be presented in degrees \
        (default: False)
    :returns: [x, y, z]
    :rtype: ndarray

    >>> sphere2cart(np.array([[1, 0, 90], [1, 90, 90]]), degrees=True)
    array([[  1.00000000e+00,   0.00000000e+00,   6.12323400e-17],
           [  6.12323400e-17,   1.00000000e+00,   6.12323400e-17]])
    """
    element_dimension(pts, 3)

    if degrees:
        pts = pts.astype(float)
        pts[:, 1:3] = np.radians(pts[:, 1:3])

    r = pts[:, 0]
    theta = pts[:, 1]
    phi = pts[:, 2]
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    return np.c_[x, y, z]

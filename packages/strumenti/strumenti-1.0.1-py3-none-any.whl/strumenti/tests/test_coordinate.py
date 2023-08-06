#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Module with unit tests for coordinate.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import numpy as np
import pytest

from strumenti import coordinate


cart2d_single = np.array([[3, 4]])
cart2d_multi = np. array([[3, 4], [6, 7]])
cart3d_single = np.array([[3, 4, 5]])
cart3d_multi = np.array([[3, 4, 5], [6, 7, 8]])

pol_single_radian = np.array([[3, np.pi / 6]])
pol_single_degree = np.array([[3, 30]])
pol_multi_radian = np.array([[3, np.pi / 6], [6, np.pi / 3]])
pol_multi_degree = np.array([[3, 30], [6, 60]])

cyl_single_radian = np.c_[pol_single_radian, [5]]
cyl_single_degree = np.c_[pol_single_degree, [5]]
cyl_multi_radian = np.c_[pol_multi_radian, [5, 8]]
cyl_multi_degree = np.c_[pol_multi_degree, [5, 8]]

sphere_single_3d_radian = np.array([[3, np.pi / 6, np.pi / 9]])
sphere_single_3d_degree = np.array([[3, 30, 20]])
sphere_multi_3d_radian = np.array([[3, np.pi / 6, np.pi / 9],
                                   [6, np.pi / 3, np.pi / 4]])
sphere_multi_3d_degree = np.array([[3, 30, 20], [6, 60, 45]])

empty = np.arange(0)


# Test element_dimension
element_dimension = {'values = int': (cart2d_multi, 2, 2),
                     'values = list': (cart2d_multi, [2, 3], 2),
                     }


@pytest.mark.parametrize('array, dim, expected',
                         list(element_dimension.values()),
                         ids=list(element_dimension.keys()))
def test__element_dimension(array, dim, expected):
    assert coordinate.element_dimension(array, dim) == expected


def test__element_dimension_empty():
    with pytest.raises(SystemExit):
        coordinate.element_dimension(empty, 2)


def test__element_dimension_wrong_values():
    with pytest.raises(SystemExit):
        coordinate.element_dimension(cart3d_multi, 2)


# Test cart2pol
cart2pol = {'2D single': ({'pts': cart2d_single}, [[5, 0.9272952]]),
            '2D single deg': ({'pts': cart2d_single, 'degrees': True},
                              [[5, 53.1301023]]),
            '2D multi': ({'pts': cart2d_multi},
                         [[5, 0.9272952], [9.2195444, 0.8621700]]),
            '2D multi deg': ({'pts': cart2d_multi, 'degrees': True},
                             [[5, 53.1301023], [9.2195444, 49.3987053]]),
            '3D single': ({'pts': cart3d_single}, [[5, 0.9272952, 5]]),
            '3D single deg': ({'pts': cart3d_single, 'degrees': True},
                              [[5, 53.1301023, 5]]),
            '3D multi': ({'pts': cart3d_multi},
                         [[5, 0.9272952, 5], [9.2195444, 0.8621700, 8]]),
            '3D multi deg': ({'pts': cart3d_multi, 'degrees': True},
                             [[5, 53.1301023, 5], [9.2195444, 49.3987053, 8]]),
            }


@pytest.mark.parametrize('kwargs, expected',
                         list(cart2pol.values()),
                         ids=list(cart2pol.keys()))
def test__cart2pol(kwargs, expected):
    assert np.allclose(coordinate.cart2pol(**kwargs), expected)


def test__cart2pol_empty():
    with pytest.raises(SystemExit):
        coordinate.cart2pol(empty)


# Test cart2sphere
cart2sphere = {'3D single': ({'pts': cart3d_single},
                             [[7.0710678, 0.9272952, 0.7853981]]),
               '3D single deg': ({'pts': cart3d_single, 'degrees': True},
                                 [[7.0710678, 53.1301023, 45]]),
               '3D multi': ({'pts': cart3d_multi},
                            [[7.0710678, 0.9272952, 0.7853981],
                             [12.2065556, 0.8621700, 0.8561033]]),
               '3D multi deg': ({'pts': cart3d_multi, 'degrees': True},
                                [[7.0710678, 53.1301023, 45],
                                 [12.2065556, 49.3987053, 49.0511101]]),
               }


@pytest.mark.parametrize('kwargs, expected',
                         list(cart2sphere.values()),
                         ids=list(cart2sphere.keys()))
def test__cart2sphere(kwargs, expected):
    assert np.allclose(coordinate.cart2sphere(**kwargs), expected)


def test__cart2sphere_empty():
    with pytest.raises(SystemExit):
        coordinate.cart2sphere(empty)


# Test pol2cart
pol2cart = {'polar 3D single': ({'pts': pol_single_radian},
                                [[2.5980762, 1.5]]),
            'polar 3D signle deg': ({'pts': pol_single_degree,
                                     'degrees': True},
                                    [[2.5980762, 1.5]]),
            'polar 3D multi': ({'pts': pol_multi_radian},
                               [[2.5980762, 1.5], [3, 5.1961524]]),
            'polar 3D multi deg': ({'pts': pol_multi_degree, 'degrees': True},
                                   [[2.5980762, 1.5], [3, 5.1961524]]),
            'cylindrical 3D single': ({'pts': cyl_single_radian},
                                      [[2.5980762, 1.5, 5]]),
            'cylindrical 3D single deg': ({'pts': cyl_single_degree,
                                           'degrees': True},
                                          [[2.5980762, 1.5, 5]]),
            'cylindrical 3D multi': ({'pts': cyl_multi_radian},
                                     [[2.5980762, 1.5, 5], [3, 5.1961524, 8]]),
            'cylindrical 3D multi deg': ({'pts': cyl_multi_degree,
                                          'degrees': True},
                                         [[2.5980762, 1.5, 5],
                                          [3, 5.1961524, 8]]),
            }


@pytest.mark.parametrize('kwargs, expected',
                         list(pol2cart.values()),
                         ids=list(pol2cart.keys()))
def test_pol2cart(kwargs, expected):
    assert np.allclose(coordinate.pol2cart(**kwargs), expected)


def test__pol2cart_empty():
    with pytest.raises(SystemExit):
        coordinate.pol2cart(empty)


# Test sphere2cart
sphere2cart = {'3D single': ({'pts': sphere_single_3d_radian},
                             [[0.8885943, 0.5130302, 2.8190778]]),
               '3D single deg': ({'pts': sphere_single_3d_degree,
                                  'degrees': True},
                                 [[0.8885943, 0.5130302, 2.8190778]]),
               '3D multi': ({'pts': sphere_multi_3d_radian},
                            [[0.8885943, 0.5130302, 2.8190778],
                             [2.1213203, 3.6742346, 4.2426406]]),
               '3D multi deg': ({'pts': sphere_multi_3d_degree,
                                 'degrees': True},
                                [[0.8885943, 0.5130302, 2.8190778],
                                 [2.1213203, 3.6742346, 4.2426406]]),
               }


@pytest.mark.parametrize('kwargs, expected',
                         list(sphere2cart.values()),
                         ids=list(sphere2cart.keys()))
def test__sphere2cart(kwargs, expected):
    assert np.allclose(coordinate.sphere2cart(**kwargs), expected)


def test__sphere2cart_empty():
    with pytest.raises(SystemExit):
        coordinate.sphere2cart(empty)

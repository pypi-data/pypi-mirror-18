#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Plotting Module

Functions for performing tasks related to matplotlib pyplot library.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import os.path as osp
from typing import Union

import matplotlib.pyplot as plt
import numpy as np


def axis_title(title: str, units: Union[str, None]=None) -> str:
    """Create string for axis title with units italicized.

    :param str title: title of axis
    :param str units: units of axis (default: None)
    :returns: formatted axis title
    :rtype: str
    """
    title = title.title()
    if units:
        return '{} ({})'.format(title, r'$\mathit{{{}}}$'.format(units))
    else:
        return '{}'.format(title)


class Derivative:
    """Plot data, 1st derivative and 2nd derivative using central difference.

    :param ndarray x: data points for x-axis
    :param ndarray y: data points for y-axis

    Attributes:

        - **dx**: *ndarray* derivative of x-axis data points
        - **dy**: *ndarray* derivative of y-axis data points
        - **ddy**: *ndarray* 2nd derivative of y-axis data points
        - **plot_name**: *str* if non None value is supplied plot file will be \
            saved
        - **label_size**: *int* axis label font size
        - **title_size**: *int* title font size
        - **title**: *str* plot title
        - **x**: *ndarray* x-axis data points
        - **x_label**: *str* x-axis label
        - **y**: *ndarray* y-axis data points
        - **y_label**: *str* y-axis label
    """
    def __init__(self, x_points: np.ndarray, y_points: np.ndarray):
        self.x = x_points
        self.y = y_points
        self.dx = np.gradient(self.x)
        self.dy = np.divide(np.gradient(self.y), self.dx)
        self.ddy = np.divide(np.gradient(self.dy), self.dx)

        self.label_size = 16
        self.title_size = 20
        self.plot_name = None
        self.title = 'Data\n'
        self.x_label = 'X'
        self.y_label = 'Y'

    def plot(self):
        """Generate plot of base data and derivatives."""
        fig1, ax1 = plt.subplots(1, 1, facecolor='white', figsize=(16, 9))
        fig1.canvas.set_window_title('Data Plot')

        ax1.plot(self.x, self.y, '-b^', markersize=8, label='data')
        ax1.plot(self.x[1:-1], self.dy[1:-1], '-.ro', markersize=5,
                 label=r'$\mathbf{\frac{\delta y}{\delta x}}$')
        ax1.plot(self.x[2:-2], self.ddy[2:-2], '--md', markersize=5,
                 label=r'$\mathbf{\frac{\delta^2 y}{\delta x^2}}$')

        ax1.set_title(self.title, fontsize=self.title_size, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=20)
        ax1.set_xlabel(self.x_label, fontsize=self.label_size,
                       fontweight='bold')
        ax1.set_ylabel(self.y_label, fontsize=self.label_size,
                       fontweight='bold')
        plt.grid(True)

        save_plot(name=self.plot_name)


def save_plot(name: str=None, **kwargs):
    """Save or display a matplotlib figure.

    :param str name: name of image file (default: None)
    :param kwargs: key word arguments for pyplot.savefig function
    """
    if name:
        name = osp.realpath(name)
        plt.savefig(name, **kwargs)
    else:
        plt.show()

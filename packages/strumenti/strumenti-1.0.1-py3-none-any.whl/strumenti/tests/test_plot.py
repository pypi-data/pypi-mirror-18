#! /usr/bin/env python

"""plot.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import os.path as osp

import pytest
import matplotlib.pyplot as plt

from strumenti import plot


# Test axis_title
axis_title = {'latex chars': ({'title': 'test', 'units': 'm^2/s_5'},
                              'Test ($\mathit{m^2/s_5}$)'),
              'no units': ({'title': 'test'}, 'Test'),
              }


@pytest.mark.parametrize('kwargs, expected',
                         list(axis_title.values()),
                         ids=list(axis_title.keys()))
def test__axis_title(kwargs, expected):
    assert plot.axis_title(**kwargs) == expected


def test__axis_title_empty_arguments():
    with pytest.raises(TypeError):
        plot.axis_title()


# Test save_plot
file_name = 'test_image.png'
save_plot = {'no save plot': ({'name': None}, False),
             'save plot': ({'name': file_name}, True),
             'additional args': ({'name': file_name, 'edgecolor': 'b',
                                  'transparent': True}, True)
             }


def plot_setup():
    fig = plt.figure(figsize=(15, 10), facecolor='white')
    fig.suptitle('Test Figure', fontsize='25', fontweight='bold')
    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
    ax.scatter([0, 1, 2, 3], [0, 10, 20, 30], color='black', marker='o')


@pytest.mark.parametrize('kwargs, file',
                         list(save_plot.values()),
                         ids=list(save_plot.keys()))
def test__save_plot(tmpdir, kwargs, file):
    tmpdir.chdir()
    plot_setup()

    plt.ion()
    plot.save_plot(**kwargs)
    if file:
        assert osp.exists(file_name)
    else:
        assert not osp.exists(file_name)

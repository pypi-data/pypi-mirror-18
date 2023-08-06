#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution, DistributionNotFound
import os.path as osp

from . import coordinate
from . import notify
from . import packages
from . import plot
from . import psql
from . import system


try:
    _dist = get_distribution('strumenti')
    dist_loc = osp.normcase(_dist.location)
    here = osp.normcase(__file__)
    if not here.startswith(osp.join(dist_loc, 'strumenti')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version

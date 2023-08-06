#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Fixtures

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

from chromalog.mark.objects import Mark
import testfixtures as tf


class ChromalogLogCapture(tf.LogCapture):
    """Class will remove color markings from chromalog logger entries.

    ..info:: The Chromalog package facilitates colored logging to the \
        screen and removes the color tags when printed to a file. \
        During unit testing the color tags are captured from stderror, which
        complicates verify logging statements. \
        This class provides an additional method to the base class \
        testfixtures.LogCapture, which extracts the string from the \
        chromalog object for the logger name and level.
    """
    def __init__(self):
        super().__init__()

    def filter_records(self):
        """Remove chromalog color markings from LogCapture attributes."""
        for (idx, record) in enumerate(self.records):
            if isinstance(record.name, Mark):
                self.records[idx].name = record.name.obj
            if isinstance(record.levelname, Mark):
                self.records[idx].levelname = record.levelname.obj

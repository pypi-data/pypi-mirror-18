# coding=utf-8
# Filename: hdf5.py
# pylint: disable=C0103,R0903
# vim:set ts=4 sts=4 sw=4 et:
"""
Read and write KM3NeT-formatted HDF5 files.
"""
from __future__ import division, absolute_import, print_function

from collections import defaultdict, OrderedDict
import os.path

import numpy as np
import pandas as pd
import tables as tb

import km3pipe as kp
from km3pipe import Pump, Module
from km3pipe.dataclasses import ArrayTaco, deserialise_map
from km3pipe.logger import logging
from km3pipe.tools import camelise, decamelise, insert_prefix_to_dtype, split

log = logging.getLogger(__name__)  # pylint: disable=C0103

__author__ = "Tamas Gal and Moritz Lotze"
__copyright__ = "Copyright 2016, Tamas Gal and the KM3NeT collaboration."
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Tamas Gal and Moritz Lotze"
__email__ = "tgal@km3net.de"
__status__ = "Development"

FORMAT_VERSION = np.string_('2.0')
MINIMUM_FORMAT_VERSION = np.string_('2.0')


class HDF5Sink(Module):
    """Write KM3NeT-formatted HDF5 files, event-by-event.

    The data can be a numpy structured array, a pandas DataFrame,
    or a km3pipe dataclass object with a `serialise()` method.

    The name of the corresponding H5 table is the decamelised
    blob-key, so values which are stored in the blob under `FooBar`
    will be written to `/foo_bar` in the HDF5 file.

    To store at a different location in the file, the data needs a
    `.h5loc` attribute:

    >>> my_arr.h5loc = '/somewhere'

    Parameters
    ----------
    filename: str, optional (default: 'dump.h5')
        Where to store the events.
    """
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.filename = self.get('filename') or 'dump.h5'

        # magic 10000: this is the default of the "expectedrows" arg
        # from the tables.File.create_table() function
        # at least according to the docs
        # might be able to set to `None`, I don't know...
        self.n_rows_expected = self.get('n_rows_expected') or 10000

        self.index = 1
        self.h5file = tb.open_file(self.filename, mode="w", title="KM3NeT")
        self.filters = tb.Filters(complevel=5, shuffle=True,
                                  fletcher32=True, complib='zlib')
        self._tables = OrderedDict()

    def _to_array(self, data):
        if np.isscalar(data):
            return np.asarray(data).reshape((1,))
        if len(data) <= 0:
            return
        try:
            return data.to_records()
        except AttributeError:
            pass
        try:
            return data.serialise()
        except AttributeError:
            pass
        return data

    def _write_array(self, where, arr, title=''):
        level = len(where.split('/'))

        if where not in self._tables:
            dtype = arr.dtype
            loc, tabname = os.path.split(where)
            tab = self.h5file.create_table(
                loc, tabname, description=dtype, title=title,
                filters=self.filters, createparents=True,
                expectedrows=self.n_rows_expected,
            )
            if(level < 4):
                self._tables[where] = tab
        else:
            tab = self._tables[where]

        tab.append(arr)

        if(level < 4):
            tab.flush()

    def process(self, blob):
        for key, entry in sorted(blob.items()):
            serialisable_attributes = ('dtype', 'serialise', 'to_records')
            if any(hasattr(entry, a) for a in serialisable_attributes):
                try:
                    h5loc = entry.h5loc
                except AttributeError:
                    h5loc = '/'
                try:
                    tabname = entry.tabname
                except AttributeError:
                    tabname = decamelise(key)

                where = os.path.join(h5loc, tabname)
                entry = self._to_array(entry)
                if entry is None:
                    continue
                if entry.dtype.names is None:
                    dt = np.dtype((entry.dtype, [(key, entry.dtype)]))
                    entry = entry.view(dt)
                    h5loc = '/misc'
                self._write_array(where, entry, title=key)

        if not self.index % 1000:
            for tab in self._tables.values():
                tab.flush()

        self.index += 1
        return blob

    def finish(self):
        self.h5file.root._v_attrs.km3pipe = np.string_(kp.__version__)
        self.h5file.root._v_attrs.pytables = np.string_(tb.__version__)
        self.h5file.root._v_attrs.format_version = np.string_(FORMAT_VERSION)
        print("Creating index tables. This may take a few minutes...")
        for tab in self._tables.itervalues():
            if 'frame_id' in tab.colnames:
                tab.cols.frame_id.create_index()
            if 'slice_id' in tab.colnames:
                tab.cols.slice_id.create_index()
            if 'dom_id' in tab.colnames:
                tab.cols.dom_id.create_index()
            if 'event_id' in tab.colnames:
                tab.cols.event_id.create_index()
            tab.flush()
        self.h5file.close()


class HDF5Pump(Pump):
    """Read KM3NeT-formatted HDF5 files, event-by-event.

        Parameters
        ----------
        filename: str
        From where to read events.
        """
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.filename = self.get('filename')
        if os.path.isfile(self.filename):
            self.h5_file = tb.File(self.filename)
            if not self.get("skip_version_check"):
                self._check_version()
        else:
            raise IOError("No such file or directory: '{0}'"
                          .format(self.filename))
        self.index = None
        self._reset_index()

        try:
            event_info = self.h5_file.get_node('/', 'event_info')
            self.event_ids = event_info.cols.event_id[:]
        except tb.NoSuchNodeError:
            log.critical("No /event_info table found.")
            raise SystemExit

        self._n_events = len(self.event_ids)

    def _check_version(self):
        try:
            version = np.string_(self.h5_file.root._v_attrs.format_version)
        except AttributeError:
            log.error("Could not determine HDF5 format version, you may "
                      "encounter unexpected errors! Good luck...")
            return
        if split(version, int, np.string_('.')) < split(MINIMUM_FORMAT_VERSION, int, np.string_('.')):
            raise SystemExit("HDF5 format version {0} or newer required!\n"
                             "'{1}' has HDF5 format version {2}."
                             .format(MINIMUM_FORMAT_VERSION,
                                     self.filename,
                                     version))

    def process(self, blob):
        try:
            blob = self.get_blob(self.index)
        except KeyError:
            self._reset_index()
            raise StopIteration
        self.index += 1
        return blob

    def get_blob(self, index):
        if self.index >= self._n_events:
            self._reset_index()
            raise StopIteration
        event_id = self.event_ids[index]
        blob = {}
        for tab in self.h5_file.walk_nodes(classname="Table"):
            loc, tabname = os.path.split(tab._v_pathname)
            tabname = camelise(tabname)
            try:
                dc = deserialise_map[tabname]
            except KeyError:
                dc = ArrayTaco
            arr = tab.read_where('event_id == %d' % event_id)
            blob[tabname] = dc.deserialise(arr, h5loc=loc, event_id=event_id)
        return blob

    def finish(self):
        """Clean everything up"""
        self.h5_file.close()

    def _reset_index(self):
        """Reset index to default value"""
        self.index = 0

    def __len__(self):
        return self._n_events

    def __iter__(self):
        return self

    def next(self):
        """Python 2/3 compatibility for iterators"""
        return self.__next__()

    def __next__(self):
        if self.index >= self._n_events:
            self._reset_index()
            raise StopIteration
        blob = self.get_blob(self.index)
        self.index += 1
        return blob

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get_blob(index)
        elif isinstance(index, slice):
            return self._slice_generator(index)
        else:
            raise TypeError("index must be int or slice")

    def _slice_generator(self, index):
        """A simple slice generator for iterations"""
        start, stop, step = index.indices(len(self))
        for i in range(start, stop, step):
            yield self.get_blob(i)



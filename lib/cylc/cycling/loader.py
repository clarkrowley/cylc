#!/usr/bin/env python

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2016 NIWA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Tasks spawn a sequence of POINTS (P) separated by INTERVALS (I).
Each task may have multiple sequences, e.g. 12-hourly and 6-hourly.
"""

from . import integer
from . import iso8601
from isodatetime.data import Calendar


ISO8601_CYCLING_TYPE = 'iso8601'
INTEGER_CYCLING_TYPE = 'integer'


POINTS = {INTEGER_CYCLING_TYPE: integer.IntegerPoint,
          ISO8601_CYCLING_TYPE: iso8601.ISO8601Point}

POINT_RELATIVE_GETTERS = {
    INTEGER_CYCLING_TYPE: integer.get_point_relative,
    ISO8601_CYCLING_TYPE: iso8601.get_point_relative
}

INTERVALS = {INTEGER_CYCLING_TYPE: integer.IntegerInterval,
             ISO8601_CYCLING_TYPE: iso8601.ISO8601Interval}

SEQUENCES = {INTEGER_CYCLING_TYPE: integer.IntegerSequence,
             ISO8601_CYCLING_TYPE: iso8601.ISO8601Sequence}

INIT_FUNCTIONS = {INTEGER_CYCLING_TYPE: integer.init_from_cfg,
                  ISO8601_CYCLING_TYPE: iso8601.init_from_cfg}


class DefaultCycler(object):

    """Store the default TYPE for Cyclers."""

    TYPE = None


def get_point(*args, **kwargs):
    """Return a cylc.cycling.PointBase-derived object from a string."""
    if args[0] is None:
        return None
    cycling_type = kwargs.pop("cycling_type", DefaultCycler.TYPE)
    return get_point_cls(cycling_type=cycling_type)(*args, **kwargs)


def get_point_cls(cycling_type=None):
    """Return the cylc.cycling.PointBase-derived class we're using."""
    if cycling_type is None:
        cycling_type = DefaultCycler.TYPE
    return POINTS[cycling_type]


def get_point_relative(*args, **kwargs):
    """Return a point from an offset expression and a base point."""
    cycling_type = kwargs.pop("cycling_type", DefaultCycler.TYPE)
    return POINT_RELATIVE_GETTERS[cycling_type](*args, **kwargs)


def get_interval(*args, **kwargs):
    """Return a cylc.cycling.IntervalBase-derived object from a string."""
    if args[0] is None:
        return None
    cycling_type = kwargs.pop("cycling_type", DefaultCycler.TYPE)
    return get_interval_cls(cycling_type=cycling_type)(*args, **kwargs)


def get_interval_cls(cycling_type=None):
    """Return the cylc.cycling.IntervalBase-derived class we're using."""
    if cycling_type is None:
        cycling_type = DefaultCycler.TYPE
    return INTERVALS[cycling_type]


def get_sequence(*args, **kwargs):
    """Return a cylc.cycling.SequenceBase-derived object from a string."""
    if args[0] is None:
        return None
    cycling_type = kwargs.pop("cycling_type", DefaultCycler.TYPE)
    return get_sequence_cls(cycling_type=cycling_type)(*args, **kwargs)


def get_sequence_cls(cycling_type=None):
    """Return the cylc.cycling.SequenceBase-derived class we're using."""
    if cycling_type is None:
        cycling_type = DefaultCycler.TYPE
    return SEQUENCES[cycling_type]


def init_cyclers(cfg):
    """Initialise cycling specifics using the suite configuration (cfg)."""
    DefaultCycler.TYPE = cfg['scheduling']['cycling mode']
    if DefaultCycler.TYPE in Calendar.MODES:
        DefaultCycler.TYPE = ISO8601_CYCLING_TYPE
    INIT_FUNCTIONS[DefaultCycler.TYPE](cfg)


def standardise_point_string(point_string, cycling_type=None):
    """Return a standardised version of point_string."""
    if point_string is None:
        return None
    point = get_point(point_string, cycling_type=cycling_type)
    if point is not None:
        point.standardise()
        point_string = str(point)
    return point_string

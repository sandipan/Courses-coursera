#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# graph_tool -- a general graph manipulation python module
#
# Copyright (C) 2006-2017 Tiago de Paula Peixoto <tiago@skewed.de>
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

from __future__ import division, absolute_import, print_function
import sys
if sys.version_info < (3,):
    range = xrange

import scipy.special
from numpy import *

from .. import PropertyMap

from .. dl_import import dl_import
dl_import("from . import libgraph_tool_inference as libinference")

class DictState(dict):
    """Dictionary with (key,value) pairs accessible via attributes."""
    def __init__(self, d):
        self.update(d)
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, val):
        self[attr] = val

def dmask(d, ks):
    """Copy dictionary ``d`` and remove key list ``ks``."""
    d = d.copy()
    for k in ks:
        if k in d:
            del d[k]
    return d

def check_verbose(verbose):
    if isinstance(verbose, tuple):
        return verbose[0] != False
    return verbose != False


def verbose_pad(verbose):
    if isinstance(verbose, tuple):
        return verbose_pad(verbose[1])
    if verbose == True:
        return ""
    return verbose

def verbose_push(verbose, push):
    if check_verbose(verbose):
        if isinstance(verbose, tuple):
            return (verbose[0] - 1, verbose_push(verbose[1], push))
        if isinstance(verbose, bool):
            return push
        return verbose + push
    return False

def lbinom(n, k):
    """Return log of binom(n, k)."""
    return (scipy.special.gammaln(float(n + 1)) -
            scipy.special.gammaln(float(n - k + 1)) -
            scipy.special.gammaln(float(k + 1)))

def lbinom_careful(n, k):
    return libinference.lbinom_careful(n, k)

def lbinom_fast(n, k):
    return libinference.lbinom_fast(n, k)

def partition_entropy(B, N, nr=None, allow_empty=True):
    if nr is None:
        S = N * log(B) + log1p(-(1 - 1./B) ** N)
    else:
        if allow_empty:
            S = lbinom(B + N - 1, N)
        else:
            S = lbinom(N - 1, B - 1)
        S += (scipy.special.gammaln(N + 1) -
              scipy.special.gammaln(nr + 1).sum())
    return S

def pmap(prop, value_map):
    """Maps all the values of `prop` to the values given by `value_map`, which
    is indexed by the values of `prop`."""
    if isinstance(prop, PropertyMap):
        a = prop.fa
    else:
        a = prop
    if isinstance(value_map, PropertyMap):
        value_map = value_map.fa
    if a.max() >= len(value_map):
        raise ValueError("value map is not large enough!" +
                         " max val: %s, map size: %s" % (a.max(),
                                                         len(value_map)))
    if a.dtype != value_map.dtype:
        value_map = array(value_map, dtype=a.dtype)
    if a.dtype == "int64":
        libinference.vector_map64(a, value_map)
    else:
        libinference.vector_map(a, value_map)
    if isinstance(prop, PropertyMap):
        prop.fa = a

def reverse_map(prop, value_map):
    """Modify `value_map` such that the positions indexed by the values in `prop`
    correspond to their index in `prop`."""
    if isinstance(prop, PropertyMap):
        prop = prop.fa
    if isinstance(value_map, PropertyMap):
        a = value_map.fa
    else:
        a = value_map
    if prop.max() >= len(a):
        raise ValueError("value map is not large enough!" +
                         " max val: %s, map size: %s" % (prop.max(), len(a)))
    if prop.dtype != a.dtype:
        prop = array(prop, dtype=a.dtype)
    if a.dtype == "int64":
        libinference.vector_rmap64(prop, a)
    else:
        libinference.vector_rmap(prop, a)
    if isinstance(value_map, PropertyMap):
        value_map.fa = a

def continuous_map(prop):
    """Remap the values of ``prop`` in the continuous range :math:`[0, N-1]`."""
    if isinstance(prop, PropertyMap):
        a = prop.fa
    else:
        a = prop
    if a.max() < len(a):
        rmap = -ones(len(a), dtype=a.dtype)
        if a.dtype == "int64":
            libinference.vector_map64(a, rmap)
        else:
            libinference.vector_map(a, rmap)
    else:
        if a.dtype == "int64":
            libinference.vector_continuous_map64(a)
        else:
            libinference.vector_continuous_map(a)
    if isinstance(prop, PropertyMap):
        prop.fa = a

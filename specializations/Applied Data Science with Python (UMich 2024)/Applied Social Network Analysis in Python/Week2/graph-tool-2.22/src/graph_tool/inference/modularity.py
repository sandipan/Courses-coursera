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

from .. import _prop, perfect_prop_hash

from .. dl_import import dl_import
dl_import("from . import libgraph_tool_inference as libinference")

def modularity(g, b, weight=None):
    r"""
    Calculate Newman's modularity of a network partition.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be used.
    b : :class:`~graph_tool.PropertyMap`
        Vertex property map with the community partition.
    weight : :class:`~graph_tool.PropertyMap` (optional, default: None)
        Edge property map with the optional edge weights.

    Returns
    -------
    Q : float
        Newman's modularity.

    Notes
    -----

    Given a specific graph partition specified by `prop`, Newman's modularity
    [newman-modularity-2006]_ is defined as:

    .. math::

          Q = \frac{1}{2E} \sum_r e_{rr}- \frac{e_r^2}{2E}

    where :math:`e_{rs}` is the number of edges which fall between
    vertices in communities s and r, or twice that number if :math:`r = s`, and
    :math:`e_r = \sum_s e_{rs}`.

    If weights are provided, the matrix :math:`e_{rs}` corresponds to the sum
    of edge weights instead of number of edges, and the value of :math:`E`
    becomes the total sum of edge weights.

    Examples
    --------
    >>> g = gt.collection.data["football"]
    >>> gt.modularity(g, g.vp.value_tsevans)
    0.5744393497...

    References
    ----------
    .. [newman-modularity-2006] M. E. J. Newman, "Modularity and community
       structure in networks", Proc. Natl. Acad. Sci. USA 103, 8577-8582 (2006),
       :doi:`10.1073/pnas.0601602103`, :arxiv:`physics/0602124`
    """

    if b.value_type() not in ["bool", "int16_t", "int32_t", "int64_t",
                              "unsigned long"]:
        b = perfect_prop_hash([b])[0]
    Q = libinference.modularity(g._Graph__graph,
                                _prop("e", g, weight),
                                _prop("v", g, b))
    return Q

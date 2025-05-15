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

from .. import _degree, _prop, Graph, GraphView, libcore, _get_rng, PropertyMap, \
    conv_pickle_state, Vector_size_t, Vector_double, group_vector_property
from .. generation import condensation_graph
from .. stats import label_self_loops
from .. spectral import adjacency
import random
from numpy import *
import numpy
import copy
import collections

from . blockmodel import *
from . util import *

from .. dl_import import dl_import
dl_import("from . import libgraph_tool_inference as libinference")


class EMBlockState(object):
    r"""The parametric, undirected stochastic block model state of a given graph.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be modelled.
    B : ``int``
        Number of blocks (or vertex groups).
    init_state : :class:`~graph_tool.inference.BlockState` (optional, default: ``None``)
        Optional block state used for initialization.

    Notes
    -----

    This class is intended to be used with :func:`em_infer()` to perform
    expectation maximization with belief propagation. See
    [decelle_asymptotic_2011]_ for more details.

    References
    ----------

    .. [decelle_asymptotic_2011] Aurelien Decelle, Florent Krzakala, Cristopher
       Moore, and Lenka Zdeborová, "Asymptotic analysis of the stochastic block
       model for modular networks and its algorithmic applications",
       Phys. Rev. E 84, 066106 (2011), :doi:`10.1103/PhysRevE.84.066106`,
       :arxiv:`1109.3041` """

    def __init__(self, g, B, init_state=None):
        self.g = g
        self.N = g.num_vertices()
        self.B = B
        self.wr = random.random(B)
        self.wr /= self.wr.sum()

        ak = 2 * g.num_edges() / g.num_vertices()
        self.prs = random.random((B, B))
        for r in range(B):
            for s in range(r, B):
                self.prs[r,s] = self.prs[s,r] = random.random()

        self.em_s = g.new_edge_property("vector<double>")
        self.em_t = g.new_edge_property("vector<double>")
        self.vm = g.new_vertex_property("vector<double>")
        self.Z = g.new_edge_property("double")

        self.max_E = self.g._get_edge_index_range()
        self.oprs = self.prs
        self.owr = self.wr
        self._state = libinference.make_em_block_state(self, _get_rng())
        del self.oprs
        del self.owr

        # fix average degree
        self.prs[:,:] /= self.get_ak() / ak

        if init_state is not None:
            # init marginals and messages
            for v in g.vertices():
                r = init_state.b[v]
                self.vm[v].a = 1e-6
                self.vm[v][r] = 1
                self.vm[v].a /= self.vm[v].a.sum()
            for e in g.edges():
                u, v = e
                if u > v:
                    u, v = v, u
                self.em_s[e] = self.vm[u]
                self.em_t[e] = self.vm[v]

            #init parameters
            self.wr[:] = init_state.wr.a
            self.wr[:] /= self.wr.sum()

            # m includes _twice_ the amount of edges in the diagonal
            m = init_state.get_matrix()
            for r in range(self.B):
                for s in range(r, self.B):
                    self.prs[r, s] = self.N * m[r, s] / (init_state.wr[r] * init_state.wr[s])
                    self.prs[s, r] = self.prs[r, s]

    def __getstate__(self):
        state = [self.g, self.B, self.vm, self.em_s, self.em_t, self.wr,
                 self.prs]
        return state

    def __setstate__(self, state):
        conv_pickle_state(state)
        g, B, vm, em_s, em_t, wr, prs = state
        self.__init__(g, B)
        g.copy_property(vm, self.vm)
        g.copy_property(em_s, self.em_s)
        g.copy_property(em_t, self.em_t)
        self.wr[:] = wr
        self.prs[:,:] = prs

    def get_vertex_marginals(self):
        """Return the vertex marginals."""
        return self.vm

    def get_group_sizes(self):
        """Return the group sizes."""
        return self.wr

    def get_matrix(self):
        """Return probability matrix."""
        return self.prs

    def get_MAP(self):
        """Return the maximum a posteriori (MAP) estimate of the node partition."""
        b = self.g.new_vertex_property("int")
        self._state.get_MAP(_prop("v", self.g, b))
        return b

    def get_fe(self):
        """Return the Bethe free energy."""
        return self._state.bethe_fe()

    def get_ak(self):
        """Return the model's average degree."""
        ak = 0
        for r in range(self.B):
            for s in range(self.B):
                ak += self.prs[r][s] * self.wr[r] * self.wr[s]
        return ak

    def e_iter(self, max_iter=1000, epsilon=1e-3, verbose=False):
        """Perform 'expectation' iterations, using belief propagation, where the vertex
        marginals and edge messages are updated, until convergence according to
        ``epsilon`` or the maximum number of iterations given by
        ``max_iter``. If ``verbose == True``, convergence information is
        displayed.

        The last update delta is returned.
        """
        return self._state.bp_iter(epsilon, max_iter, verbose, _get_rng())

    def m_iter(self):
        """Perform a single 'maximization' iteration, where the group sizes and
        connection probability matrix are updated.

        The update delta is returned.
        """
        return self._state.learn_iter()

    def learn(state, epsilon=1e-3):
        """Perform 'maximization' iterations until convergence according to ``epsilon``.

        The last update delta is returned.
        """
        delta = epsilon + 1
        while delta > epsilon:
            delta = self.m_iter()
        return delta

    def draw(self, **kwargs):
        r"""Convenience wrapper to :func:`~graph_tool.draw.graph_draw` that
        draws the state of the graph as colors on the vertices and edges."""

        b = self.get_MAP()
        bv = self.g.new_vertex_property("vector<int32_t>", val=range(self.B))
        gradient = self.g.new_ep("double")
        gradient = group_vector_property([gradient])
        from graph_tool.draw import graph_draw
        return graph_draw(self.g,
                          vertex_fill_color=kwargs.get("vertex_fill_color", b),
                          vertex_shape=kwargs.get("vertex_shape", "pie"),
                          vertex_pie_colors=kwargs.get("vertex_pie_colors", bv),
                          vertex_pie_fractions=kwargs.get("vertex_pie_fractions",
                                                          self.vm),
                          edge_gradient=kwargs.get("edge_gradient", gradient),
                          **dmask(kwargs, ["vertex_shape", "vertex_pie_colors",
                                           "vertex_pie_fractions",
                                           "vertex_fill_color",
                                           "edge_gradient"]))


def em_infer(state, max_iter=1000, max_e_iter=1, epsilon=1e-3,
             learn_first=False, verbose=False):
    """Infer the model parameters and latent variables using the
    expectation-maximization (EM) algorithm with initial state given by
    ``state``.

    Parameters
    ----------
    state : model state
        State object, e.g. of type :class:`graph_tool.inference.EMBlockState`.
    max_iter : ``int`` (optional, default: ``1000``)
        Maximum number of iterations.
    max_e_iter : ``int`` (optional, default: ``1``)
        Maximum number of 'expectation' iterations inside the main loop.
    epsilon : ``float`` (optional, default: ``1e-3``)
        Convergence criterion.
    learn_first : ``bool`` (optional, default: ``False``)
        If ``True``, the maximization (a.k.a parameter learning) is converged
        before the main loop is run.
    verbose : ``bool`` (optional, default: ``True``)
        If ``True``, convergence information is displayed.

    Returns
    -------

    delta : ``float``
        The last update delta.
    niter : ``int``
        The total number of iterations.

    Examples
    --------
    .. testsetup:: em_infer

       gt.seed_rng(42)
       np.random.seed(42)

    .. doctest:: em_infer

       >>> g = gt.collection.data["polbooks"]
       >>> state = gt.EMBlockState(g, B=3)
       >>> delta, niter = gt.em_infer(state)
       >>> state.draw(pos=g.vp["pos"], output="polbooks_EM_B3.pdf")
       <...>

    .. testcleanup:: em_infer

       state.draw(pos=g.vp["pos"], output="polbooks_EM_B3.png")

    .. figure:: polbooks_EM_B3.*
       :align: center

       "Soft" block partition of a political books network with :math:`B=3`.

    References
    ----------

    .. [wiki-EM] "Expectation–maximization algorithm",
       https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm

    """

    if learn_first:
        state.learn(state, epsilon)

    niter = 0
    delta = epsilon + 1
    while delta > epsilon:
        delta = state.e_iter(max_iter=max_e_iter, epsilon=epsilon,
                             verbose=verbose)
        delta += state.m_iter()
        niter += 1
        if niter > max_iter and max_iter > 0:
            break
        if verbose:
            print(niter, delta)
    return delta, niter
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.s

"""
``graph_tool.generation`` - Random graph generation
---------------------------------------------------

Summary
+++++++

.. autosummary::
   :nosignatures:

   random_graph
   random_rewire
   generate_sbm
   predecessor_tree
   line_graph
   graph_union
   triangulation
   lattice
   geometric_graph
   price_network
   complete_graph
   circular_graph
   condensation_graph

Contents
++++++++
"""

from __future__ import division, absolute_import, print_function
import sys
if sys.version_info < (3,):
    range = xrange

from .. dl_import import dl_import
dl_import("from . import libgraph_tool_generation")

from .. import Graph, GraphView, _check_prop_scalar, _prop, _limit_args, \
    _gt_type, _get_rng, _c_str, libcore
from .. stats import label_parallel_edges, label_self_loops
import inspect
import types
import numpy
import numpy.random

__all__ = ["random_graph", "random_rewire", "generate_sbm", "predecessor_tree",
           "line_graph", "graph_union", "triangulation", "lattice",
           "geometric_graph", "price_network", "complete_graph",
           "circular_graph", "condensation_graph"]


def random_graph(N, deg_sampler, directed=True,
                 parallel_edges=False, self_loops=False, block_membership=None,
                 block_type="int", degree_block=False,
                 random=True, verbose=False, **kwargs):
    r"""
    Generate a random graph, with a given degree distribution and (optionally)
    vertex-vertex correlation.

    The graph will be randomized via the :func:`~graph_tool.generation.random_rewire`
    function, and any remaining parameters will be passed to that function.
    Please read its documentation for all the options regarding the different
    statistical models which can be chosen.

    Parameters
    ----------
    N : int
        Number of vertices in the graph.
    deg_sampler : function
        A degree sampler function which is called without arguments, and returns
        a tuple of ints representing the in and out-degree of a given vertex (or
        a single int for undirected graphs, representing the out-degree). This
        function is called once per vertex, but may be called more times, if the
        degree sequence cannot be used to build a graph.

        Optionally, you can also pass a function which receives one or two
        arguments. If ``block_membership is None``, the single argument passed
        will be the index of the vertex which will receive the degree.  If
        ``block_membership is not None``, the first value passed will be the vertex
        index, and the second will be the block value of the vertex.
    directed : bool (optional, default: ``True``)
        Whether the generated graph should be directed.
    parallel_edges : bool (optional, default: ``False``)
        If ``True``, parallel edges are allowed.
    self_loops : bool (optional, default: ``False``)
        If ``True``, self-loops are allowed.
    block_membership : list or :class:`~numpy.ndarray` or function (optional, default: ``None``)
        If supplied, the graph will be sampled from a stochastic blockmodel
        ensemble, and this parameter specifies the block membership of the
        vertices, which will be passed to the
        :func:`~graph_tool.generation.random_rewire` function.

        If the value is a list or a :class:`~numpy.ndarray`, it must have
        ``len(block_membership) == N``, and the values will define to which
        block each vertex belongs.

        If this value is a function, it will be used to sample the block
        types. It must be callable either with no arguments or with a single
        argument which will be the vertex index. In either case it must return
        a type compatible with the ``block_type`` parameter.

        See the documentation for the ``vertex_corr`` parameter of the
        :func:`~graph_tool.generation.random_rewire` function which specifies
        the correlation matrix.
    block_type : string (optional, default: ``"int"``)
        Value type of block labels. Valid only if ``block_membership is not None``.
    degree_block : bool (optional, default: ``False``)
        If ``True``, the degree of each vertex will be appended to block labels
        when constructing the blockmodel, such that the resulting block type
        will be a pair :math:`(r, k)`, where :math:`r` is the original block
        label.
    random : bool (optional, default: ``True``)
        If ``True``, the returned graph is randomized. Otherwise a deterministic
        placement of the edges will be used.
    verbose : bool (optional, default: ``False``)
        If ``True``, verbose information is displayed.

    Returns
    -------
    random_graph : :class:`~graph_tool.Graph`
        The generated graph.
    blocks : :class:`~graph_tool.PropertyMap`
        A vertex property map with the block values. This is only returned if
        ``block_membership is not None``.

    See Also
    --------
    random_rewire: in-place graph shuffling

    Notes
    -----
    The algorithm makes sure the degree sequence is graphical (i.e. realizable)
    and keeps re-sampling the degrees if is not. With a valid degree sequence,
    the edges are placed deterministically, and later the graph is shuffled with
    the :func:`~graph_tool.generation.random_rewire` function, with all
    remaining parameters passed to it.

    The complexity is :math:`O(V + E)` if parallel edges are allowed, and
    :math:`O(V + E \times\text{n-iter})` if parallel edges are not allowed.


    .. note ::

        If ``parallel_edges == False`` this algorithm only guarantees that the
        returned graph will be a random sample from the desired ensemble if
        ``n_iter`` is sufficiently large. The algorithm implements an
        efficient Markov chain based on edge swaps, with a mixing time which
        depends on the degree distribution and correlations desired. If degree
        correlations are provided, the mixing time tends to be larger.

    Examples
    --------

    .. testcode::
       :hide:

       import numpy.random
       from pylab import *
       np.random.seed(43)
       gt.seed_rng(42)

    This is a degree sampler which uses rejection sampling to sample from the
    distribution :math:`P(k)\propto 1/k`, up to a maximum.

    >>> def sample_k(max):
    ...     accept = False
    ...     while not accept:
    ...         k = np.random.randint(1,max+1)
    ...         accept = np.random.random() < 1.0/k
    ...     return k
    ...

    The following generates a random undirected graph with degree distribution
    :math:`P(k)\propto 1/k` (with k_max=40) and an *assortative* degree
    correlation of the form:

    .. math::

        P(i,k) \propto \frac{1}{1+|i-k|}

    >>> g = gt.random_graph(1000, lambda: sample_k(40), model="probabilistic-configuration",
    ...                     edge_probs=lambda i, k: 1.0 / (1 + abs(i - k)), directed=False,
    ...                     n_iter=100)

    The following samples an in,out-degree pair from the joint distribution:

    .. math::

        p(j,k) = \frac{1}{2}\frac{e^{-m_1}m_1^j}{j!}\frac{e^{-m_1}m_1^k}{k!} +
                 \frac{1}{2}\frac{e^{-m_2}m_2^j}{j!}\frac{e^{-m_2}m_2^k}{k!}

    with :math:`m_1 = 4` and :math:`m_2 = 20`.

    >>> def deg_sample():
    ...    if random() > 0.5:
    ...        return np.random.poisson(4), np.random.poisson(4)
    ...    else:
    ...        return np.random.poisson(20), np.random.poisson(20)
    ...

    The following generates a random directed graph with this distribution, and
    plots the combined degree correlation.

    >>> g = gt.random_graph(20000, deg_sample)
    >>>
    >>> hist = gt.combined_corr_hist(g, "in", "out")
    >>>
    >>> figure()
    <...>
    >>> imshow(hist[0].T, interpolation="nearest", origin="lower")
    <...>
    >>> colorbar()
    <...>
    >>> xlabel("in-degree")
    <...>
    >>> ylabel("out-degree")
    <...>
    >>> tight_layout()
    >>> savefig("combined-deg-hist.pdf")

    .. testcode::
       :hide:

       savefig("combined-deg-hist.png")

    .. figure:: combined-deg-hist.*
        :align: center

        Combined degree histogram.

    A correlated directed graph can be build as follows. Consider the following
    degree correlation:

    .. math::

         P(j',k'|j,k)=\frac{e^{-k}k^{j'}}{j'!}
         \frac{e^{-(20-j)}(20-j)^{k'}}{k'!}

    i.e., the in->out correlation is "disassortative", the out->in correlation
    is "assortative", and everything else is uncorrelated.
    We will use a flat degree distribution in the range [1,20).

    >>> p = scipy.stats.poisson
    >>> g = gt.random_graph(20000, lambda: (sample_k(19), sample_k(19)),
    ...                     model="probabilistic-configuration",
    ...                     edge_probs=lambda a,b: (p.pmf(a[0], b[1]) *
    ...                                             p.pmf(a[1], 20 - b[0])),
    ...                     n_iter=100)

    Lets plot the average degree correlations to check.

    >>> figure()
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "in", "in")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...         label=r"$\left<\text{in}\right>$ vs in")
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "in", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...         label=r"$\left<\text{out}\right>$ vs in")
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "out", "in")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{in}\right>$ vs out")
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "out", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{out}\right>$ vs out")
    <...>
    >>> legend(loc="lower right", borderaxespad=0., framealpha=0.8)
    <...>
    >>> xlabel("Source degree")
    <...>
    >>> ylabel("Average target degree")
    <...>
    >>> tight_layout()
    >>> savefig("deg-corr-dir.pdf")

    .. testcode::
       :hide:

       savefig("deg-corr-dir.png")

    .. figure:: deg-corr-dir.*
        :align: center

        Average nearest neighbour correlations.


    **Stochastic blockmodels**


    The following example shows how a stochastic blockmodel
    [holland-stochastic-1983]_ [karrer-stochastic-2011]_ can be generated. We
    will consider a system of 10 blocks, which form communities. The connection
    probability will be given by

    >>> def prob(a, b):
    ...    if a == b:
    ...        return 0.999
    ...    else:
    ...        return 0.001

    The blockmodel can be generated as follows.

    >>> g, bm = gt.random_graph(2000, lambda: poisson(10), directed=False,
    ...                         model="blockmodel",
    ...                         block_membership=lambda: randint(10),
    ...                         edge_probs=prob)
    >>> gt.graph_draw(g, vertex_fill_color=bm, edge_color="black", output="blockmodel.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, vertex_fill_color=bm, edge_color="black", output="blockmodel.png")

    .. figure:: blockmodel.*
        :align: center

        Simple blockmodel with 10 blocks.


    References
    ----------
    .. [metropolis-equations-1953]  Metropolis, N.; Rosenbluth, A.W.;
       Rosenbluth, M.N.; Teller, A.H.; Teller, E. "Equations of State
       Calculations by Fast Computing Machines". Journal of Chemical Physics 21
       (6): 1087-1092 (1953). :doi:`10.1063/1.1699114`
    .. [hastings-monte-carlo-1970] Hastings, W.K. "Monte Carlo Sampling Methods
       Using Markov Chains and Their Applications". Biometrika 57 (1): 97-109 (1970).
       :doi:`10.1093/biomet/57.1.97`
    .. [holland-stochastic-1983] Paul W. Holland, Kathryn Blackmond Laskey, and
       Samuel Leinhardt, "Stochastic blockmodels: First steps," Social Networks
       5, no. 2: 109-13 (1983) :doi:`10.1016/0378-8733(83)90021-7`
    .. [karrer-stochastic-2011] Brian Karrer and M. E. J. Newman, "Stochastic
       blockmodels and community structure in networks," Physical Review E 83,
       no. 1: 016107 (2011) :doi:`10.1103/PhysRevE.83.016107` :arxiv:`1008.3926`
    """

    g = Graph()

    if (type(block_membership) is types.FunctionType or
        type(block_membership) is types.LambdaType):
        btype = block_type
        bm = []
        if len(inspect.getargspec(block_membership)[0]) == 0:
            for i in range(N):
                bm.append(block_membership())
        else:
            for i in range(N):
                bm.append(block_membership(i))
        block_membership = bm
    elif block_membership is not None:
        btype = _gt_type(block_membership[0])

    if len(inspect.getargspec(deg_sampler)[0]) > 0:
        if block_membership is not None:
            sampler = lambda i: deg_sampler(i, block_membership[i])
        else:
            sampler = deg_sampler
    else:
        sampler = lambda i: deg_sampler()

    if not directed:
        def sampler_wrap(*args):
            k = sampler(*args)
            try:
                return int(k)
            except:
                raise ValueError("degree value not understood: " + str(k))
    else:
        def sampler_wrap(*args):
            k = sampler(*args)
            try:
                return int(k[0]), int(k[1])
            except:
                raise ValueError("(in,out)-degree value pair not understood: " +
                                 str(k))

    libgraph_tool_generation.gen_graph(g._Graph__graph, N, sampler_wrap,
                                       not parallel_edges,
                                       not self_loops, not directed,
                                       _get_rng(), verbose, True)
    g.set_directed(directed)

    if degree_block:
        if btype in ["object", "string"] or "vector" in btype:
            btype = "object"
        elif btype in ["int", "int32_t", "bool"]:
            btype = "vector<int32_t>"
        elif btype in ["long", "int64_t"]:
            btype = "vector<int64_t>"
        elif btype in ["double"]:
            btype = "vector<double>"
        elif btype in ["long double"]:
            btype = "vector<long double>"

    if block_membership is not None:
        bm = g.new_vertex_property(btype)
        if btype in ["object", "string"] or "vector" in btype:
            for v in g.vertices():
                if not degree_block:
                    bm[v] = block_membership[int(v)]
                else:
                    if g.is_directed():
                        bm[v] = (block_membership[int(v)], v.in_degree(),
                                 v.out_degree())
                    else:
                        bm[v] = (block_membership[int(v)], v.out_degree())
        else:
            try:
                bm.a = block_membership
            except ValueError:
                bm = g.new_vertex_property("object")
                for v in g.vertices():
                    bm[v] = block_membership[int(v)]
    else:
        bm = None

    if random:
        g.set_fast_edge_removal(True)
        random_rewire(g, parallel_edges=parallel_edges,
                      self_loops=self_loops, verbose=verbose,
                      block_membership=bm, **kwargs)
        g.set_fast_edge_removal(False)

    if bm is None:
        return g
    else:
        return g, bm


@_limit_args({"model": ["erdos", "configuration", "constrained-configuration",
                        "probabilistic-configuration", "blockmodel-degree",
                        "blockmodel"]})
def random_rewire(g, model="configuration", n_iter=1, edge_sweep=True,
                  parallel_edges=False, self_loops=False, edge_probs=None,
                  block_membership=None, alias=True, cache_probs=True,
                  persist=False, pin=None, ret_fail=False, verbose=False):
    r"""Shuffle the graph in-place, following a variety of possible statistical
    models, chosen via the parameter ``model``.


    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be shuffled. The graph will be modified.
    model : string (optional, default: ``"configuration"``)
        The following statistical models can be chosen, which determine how the
        edges are rewired.

        ``erdos``
           The edges will be rewired entirely randomly, and the resulting graph
           will correspond to the :math:`G(N,E)` Erdős–Rényi model.
        ``configuration``
           The edges will be rewired randomly, but the degree sequence of the
           graph will remain unmodified.
        ``constrained-configuration``
           The edges will be rewired randomly, but both the degree sequence of
           the graph and the *vertex-vertex (in,out)-degree correlations* will
           remain exactly preserved. If the ``block_membership`` parameter is
           passed, the block variables at the endpoints of the edges will be
           preserved, instead of the degree-degree correlation.
        ``probabilistic-configuration``
           This is similar to ``constrained-configuration``, but the
           vertex-vertex correlations are not preserved, but are instead sampled
           from an arbitrary degree-based probabilistic model specified via the
           ``edge_probs`` parameter. The degree-sequence is preserved.
        ``blockmodel-degree``
           This is just like ``probabilistic-configuration``, but the values
           passed to the ``edge_probs`` function will correspond to the block
           membership values specified by the ``block_membership`` parameter.
        ``blockmodel``
           This is just like ``blockmodel-degree``, but the degree sequence *is
           not* preserved during rewiring.
    n_iter : int (optional, default: ``1``)
        Number of iterations. If ``edge_sweep == True``, each iteration
        corresponds to an entire "sweep" over all edges. Otherwise this
        corresponds to the total number of edges which are randomly chosen for a
        swap attempt (which may repeat).
    edge_sweep : bool (optional, default: ``True``)
        If ``True``, each iteration will perform an entire "sweep" over the
        edges, where each edge is visited once in random order, and a edge swap
        is attempted.
    parallel_edges : bool (optional, default: ``False``)
        If ``True``, parallel edges are allowed.
    self_loops : bool (optional, default: ``False``)
        If ``True``, self-loops are allowed.
    edge_probs : function or sequence of triples (optional, default: ``None``)
        A function which determines the edge probabilities in the graph. In
        general it should have the following signature:

        .. code::

            def prob(r, s):
                ...
                return p

        where the return value should be a non-negative scalar.

        Alternatively, this parameter can be a list of triples of the form ``(r,
        s, p)``, with the same meaning as the ``r``, ``s`` and ``p`` values
        above. If a given ``(r, s)`` combination is not present in this list,
        the corresponding value of ``p`` is assumed to be zero. If the same
        ``(r, s)`` combination appears more than once, their ``p`` values will
        be summed together. This is useful when the correlation matrix is
        sparse, i.e. most entries are zero.

        If ``model == probabilistic-configuration`` the parameters ``r`` and
        ``s`` correspond respectively to the (in, out)-degree pair of the source
        vertex of an edge, and the (in,out)-degree pair of the target of the
        same edge (for undirected graphs, both parameters are scalars
        instead). The value of ``p`` should be a number proportional to the
        probability of such an edge existing in the generated graph.

        If ``model == blockmodel-degree`` or ``model == blockmodel``, the ``r``
        and ``s`` values passed to the function will be the block values of the
        respective vertices, as specified via the ``block_membership``
        parameter. The value of ``p`` should be a number proportional to the
        probability of such an edge existing in the generated graph.
    block_membership : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        If supplied, the graph will be rewired to conform to a blockmodel
        ensemble. The value must be a vertex property map which defines the
        block of each vertex.
    alias : bool (optional, default: ``True``)
        If ``True``, and ``model`` is any of ``probabilistic-configuration``,
        ``blockmodel-degree``, or ``blockmodel``, the alias method will be used
        to sample the candidate edges. In the case of ``blockmodel``, if
        ``parallel_edges == True`` and ``self_loops == True`` this makes the
        sampling of the edges direct (not rejection based), so that ``n_iter ==
        1`` is enough to get an uncorrelated sample.
    cache_probs : bool (optional, default: ``True``)
        If ``True``, the probabilities returned by the ``edge_probs`` parameter
        will be cached internally. This is crucial for good performance, since
        in this case the supplied python function is called only a few times,
        and not at every attempted edge rewire move. However, in the case were
        the different parameter combinations to the probability function is very
        large, the memory and time requirements to keep the cache may not be
        worthwhile.
    persist : bool (optional, default: ``False``)
        If ``True``, an edge swap which is rejected will be attempted again
        until it succeeds. This may improve the quality of the shuffling for
        some probabilistic models, and should be sufficiently fast for sparse
        graphs, but otherwise it may result in many repeated attempts for
        certain corner-cases in which edges are difficult to swap.
    pin : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        Edge property map which, if provided, specifies which edges are allowed
        to be rewired. Edges for which the property value is ``1`` (or ``True``)
        will be left unmodified in the graph.
    verbose : bool (optional, default: ``False``)
        If ``True``, verbose information is displayed.


    Returns
    -------
    rejection_count : int
        Number of rejected edge moves (due to parallel edges or self-loops, or
        the probabilistic model used).

    See Also
    --------
    random_graph: random graph generation

    Notes
    -----
    This algorithm iterates through all the edges in the network and tries to
    swap its target or source with the target or source of another edge. The
    selected canditate swaps are chosen according to the ``model`` parameter.

    .. note::

        If ``parallel_edges = False``, parallel edges are not placed during
        rewiring. In this case, the returned graph will be a uncorrelated sample
        from the desired ensemble only if ``n_iter`` is sufficiently large. The
        algorithm implements an efficient Markov chain based on edge swaps, with
        a mixing time which depends on the degree distribution and correlations
        desired. If degree probabilistic correlations are provided, the mixing
        time tends to be larger.

        If ``model`` is either "probabilistic-configuration", "blockmodel" or
        "blockmodel-degree", the Markov chain still needs to be mixed, even if
        parallel edges and self-loops are allowed. In this case the Markov chain
        is implemented using the Metropolis-Hastings
        [metropolis-equations-1953]_ [hastings-monte-carlo-1970]_
        acceptance/rejection algorithm. It will eventually converge to the
        desired probabilities for sufficiently large values of ``n_iter``.


    Each edge is tentatively swapped once per iteration, so the overall
    complexity is :math:`O(V + E \times \text{n-iter})`. If ``edge_sweep ==
    False``, the complexity becomes :math:`O(V + E + \text{n-iter})`.

    Examples
    --------

    Some small graphs for visualization.

    .. testcode::
       :hide:

       from numpy.random import random, seed
       from pylab import *
       seed(43)
       gt.seed_rng(42)

    >>> g, pos = gt.triangulation(np.random.random((1000,2)))
    >>> pos = gt.arf_layout(g)
    >>> gt.graph_draw(g, pos=pos, output="rewire_orig.pdf", output_size=(300, 300))
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output="rewire_orig.png", output_size=(300, 300))

    >>> ret = gt.random_rewire(g, "constrained-configuration")
    >>> pos = gt.arf_layout(g)
    >>> gt.graph_draw(g, pos=pos, output="rewire_corr.pdf", output_size=(300, 300))
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output="rewire_corr.png", output_size=(300, 300))

    >>> ret = gt.random_rewire(g)
    >>> pos = gt.arf_layout(g)
    >>> gt.graph_draw(g, pos=pos, output="rewire_uncorr.pdf", output_size=(300, 300))
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output="rewire_uncorr.png", output_size=(300, 300))

    >>> ret = gt.random_rewire(g, "erdos")
    >>> pos = gt.arf_layout(g)
    >>> gt.graph_draw(g, pos=pos, output="rewire_erdos.pdf", output_size=(300, 300))
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output="rewire_erdos.png", output_size=(300, 300))

    Some `ridiculograms <http://www.youtube.com/watch?v=YS-asmU3p_4>`_ :

    .. image:: rewire_orig.*
    .. image:: rewire_corr.*
    .. image:: rewire_uncorr.*
    .. image:: rewire_erdos.*

    **From left to right**: Original graph; Shuffled graph, with degree correlations;
    Shuffled graph, without degree correlations; Shuffled graph, with random degrees.

    We can try with larger graphs to get better statistics, as follows.

    >>> figure()
    <...>
    >>> g = gt.random_graph(30000, lambda: sample_k(20), model="probabilistic-configuration",
    ...                     edge_probs=lambda i, j: exp(abs(i-j)), directed=False,
    ...                     n_iter=100)
    >>> corr = gt.avg_neighbour_corr(g, "out", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-", label="Original")
    <...>
    >>> ret = gt.random_rewire(g, "constrained-configuration")
    >>> corr = gt.avg_neighbour_corr(g, "out", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="*", label="Correlated")
    <...>
    >>> ret = gt.random_rewire(g)
    >>> corr = gt.avg_neighbour_corr(g, "out", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-", label="Uncorrelated")
    <...>
    >>> ret = gt.random_rewire(g, "erdos")
    >>> corr = gt.avg_neighbour_corr(g, "out", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-", label=r"Erd\H{o}s")
    <...>
    >>> xlabel("$k$")
    <...>
    >>> ylabel(r"$\left<k_{nn}\right>$")
    <...>
    >>> legend(loc="best")
    <...>
    >>> tight_layout()
    >>> savefig("shuffled-stats.pdf")

    .. testcode::
       :hide:

       savefig("shuffled-stats.png")


    .. figure:: shuffled-stats.*
        :align: center

        Average degree correlations for the different shuffled and non-shuffled
        graphs. The shuffled graph with correlations displays exactly the same
        correlation as the original graph.

    Now let's do it for a directed graph. See
    :func:`~graph_tool.generation.random_graph` for more details.

    >>> p = scipy.stats.poisson
    >>> g = gt.random_graph(20000, lambda: (sample_k(19), sample_k(19)),
    ...                     model="probabilistic-configuration",
    ...                     edge_probs=lambda a, b: (p.pmf(a[0], b[1]) * p.pmf(a[1], 20 - b[0])),
    ...                     n_iter=100)
    >>> figure()
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "in", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{o}\right>$ vs i")
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "out", "in")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{i}\right>$ vs o")
    <...>
    >>> ret = gt.random_rewire(g, "constrained-configuration")
    >>> corr = gt.avg_neighbour_corr(g, "in", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{o}\right>$ vs i, corr.")
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "out", "in")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{i}\right>$ vs o, corr.")
    <...>
    >>> ret = gt.random_rewire(g, "configuration")
    >>> corr = gt.avg_neighbour_corr(g, "in", "out")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{o}\right>$ vs i, uncorr.")
    <...>
    >>> corr = gt.avg_neighbour_corr(g, "out", "in")
    >>> errorbar(corr[2][:-1], corr[0], yerr=corr[1], fmt="o-",
    ...          label=r"$\left<\text{i}\right>$ vs o, uncorr.")
    <...>
    >>> legend(loc="lower right", borderaxespad=0., framealpha=0.8)
    <...>
    >>> xlabel("Source degree")
    <...>
    >>> ylabel("Average target degree")
    <...>
    >>> tight_layout()
    >>> savefig("shuffled-deg-corr-dir.pdf")

    .. testcode::
       :hide:

       savefig("shuffled-deg-corr-dir.png")

    .. figure:: shuffled-deg-corr-dir.*
        :align: center

        Average degree correlations for the different shuffled and non-shuffled
        directed graphs. The shuffled graph with correlations displays exactly
        the same correlation as the original graph.

    References
    ----------
    .. [metropolis-equations-1953]  Metropolis, N.; Rosenbluth, A.W.;
       Rosenbluth, M.N.; Teller, A.H.; Teller, E. "Equations of State
       Calculations by Fast Computing Machines". Journal of Chemical Physics 21
       (6): 1087-1092 (1953). :doi:`10.1063/1.1699114`
    .. [hastings-monte-carlo-1970] Hastings, W.K. "Monte Carlo Sampling Methods
       Using Markov Chains and Their Applications". Biometrika 57 (1): 97-109 (1970).
       :doi:`10.1093/biomet/57.1.97`
    .. [holland-stochastic-1983] Paul W. Holland, Kathryn Blackmond Laskey, and
       Samuel Leinhardt, "Stochastic blockmodels: First steps," Social Networks
       5, no. 2: 109-13 (1983) :doi:`10.1016/0378-8733(83)90021-7`
    .. [karrer-stochastic-2011] Brian Karrer and M. E. J. Newman, "Stochastic
       blockmodels and community structure in networks," Physical Review E 83,
       no. 1: 016107 (2011) :doi:`10.1103/PhysRevE.83.016107` :arxiv:`1008.3926`

    """

    if (edge_probs is not None and not g.is_directed()) and "blockmodel" not in model:
        corr = lambda i, j: edge_probs(i[1], j[1])
    else:
        corr = edge_probs

    if model not in ["probabilistic-configuration", "blockmodel",
                     "blockmodel-degree"]:
        g = GraphView(g, reversed=False)
    elif edge_probs is None:
        raise ValueError("A function must be supplied as the 'edge_probs' parameter")

    if model == "blockmodel-degree" and alias and edge_sweep:
        edge_sweep = False
        n_iter *= g.num_edges()

    traditional = True
    if model == "blockmodel-degree":
        model = "blockmodel"
        traditional = False

    if pin is None:
        pin = g.new_edge_property("bool")

    if pin.value_type() != "bool":
        pin = pin.copy(value_type="bool")

    pcount = libgraph_tool_generation.random_rewire(g._Graph__graph,
                                                    _c_str(model),
                                                    n_iter, not edge_sweep,
                                                    self_loops, parallel_edges,
                                                    alias, traditional, persist,
                                                    corr,
                                                    _prop("e", g, pin),
                                                    _prop("v", g, block_membership),
                                                    cache_probs,
                                                    _get_rng(), verbose)
    return pcount

def generate_sbm(b, probs, out_degs=None, in_degs=None, directed=False):
    r"""Generate a random graph by sampling from the Poisson stochastic block model.

    Parameters
    ----------
    b : iterable or :class:`numpy.ndarray`
        Group membership for each node.
    probs : two-dimensional :class:`numpy.ndarray` or :class:`scipy.sparse.spmatrix`
        Matrix with edge propensities between groups. The value ``probs[r,s]``
        corresponds to the average number of edges between groups ``r`` and
        ``s`` (or twice the average number if ``r == s`` and the graph is
        undirected).
    out_degs : iterable or :class:`numpy.ndarray` (optional, default: ``None``)
        Out-degree propensity for each node. If not provided, a constant value
        will be used. Note that the values will be normalized inside each group,
        if they are not already so.
    in_degs : iterable or :class:`numpy.ndarray` (optional, default: ``None``)
        In-degree propensity for each node. If not provided, a constant value
        will be used. Note that the values will be normalized inside each group,
        if they are not already so.
    directed : ``bool`` (optional, default: ``False``)
        Whether the graph is directed.

    Returns
    -------
    g : :class:`~graph_tool.Graph`
        The generated graph.

    See Also
    --------
    random_graph: random graph generation

    Notes
    -----

    The graphs are generated with probability

    .. math::

        P({\boldsymbol A}|{\boldsymbol \lambda},{\boldsymbol \theta},{\boldsymbol b})
            = \prod_{i<j}\frac{e^{-\lambda_{b_ib_j}\theta_i\theta_j}(\lambda_{b_ib_j}\theta_i\theta_j)^{A_{ij}}}{A_{ij}!}
              \times\prod_i\frac{e^{-\lambda_{b_ib_i}\theta_i^2/2}(\lambda_{b_ib_i}\theta_i^2/2)^{A_{ij}/2}}{(A_{ij}/2)!},

    where :math:`\lambda_{rs}` is the edge propensity between groups :math:`r`
    and :math:`s`, and :math:`\theta_i` is the propensity of node i to receive
    edges, which is proportional to its expected degree. Note that in the
    algorithm it is assumed that the node propensities are normalized for each
    group,

    .. math::

        \sum_i\theta_i\delta_{b_i,r} = 1,

    such that the value :math:`\lambda_{rs}` will correspond to the average
    number of edges between groups :math:`r` and :math:`s` (or twice that if
    :math:`r = s`). If the supplied values of :math:`\theta_i` are not
    normalized as above, they will be normalized prior to the generation of the
    graph.

    For directed graphs, the probability is analogous, with :math:`\lambda_{rs}`
    being in general asymmetric:

    .. math::

        P({\boldsymbol A}|{\boldsymbol \lambda},{\boldsymbol \theta},{\boldsymbol b})
            = \prod_{ij}\frac{e^{-\lambda_{b_ib_j}\theta^+_i\theta^-_j}(\lambda_{b_ib_j}\theta^+_i\theta^-_j)^{A_{ij}}}{A_{ij}!}.

    Again, the same normalization is assumed:

    .. math::

        \sum_i\theta_i^+\delta_{b_i,r} = \sum_i\theta_i^-\delta_{b_i,r} = 1,

    such that the value :math:`\lambda_{rs}` will correspond to the average
    number of directed edges between groups :math:`r` and :math:`s`.

    The graph is generated in time :math:`O(V + E + B)`, where :math:`B` is the
    number of groups.

    Examples
    --------

    >>> g = gt.collection.data["polblogs"]
    >>> g = gt.GraphView(g, vfilt=gt.label_largest_component(g))
    >>> g = gt.Graph(g, prune=True)
    >>> state = gt.minimize_blockmodel_dl(g)
    >>> u = gt.generate_sbm(state.b.a, gt.adjacency(state.get_bg(),
    ...                                             state.get_ers()),
    ...                     g.degree_property_map("out").a,
    ...                     g.degree_property_map("in").a, directed=True)
    >>> gt.graph_draw(g, g.vp.pos, output="polblogs-sbm.png")
    <...>
    >>> gt.graph_draw(u, g.vp.pos, output="polblogs-sbm-generated.png")
    <...>

    .. image:: polblogs-sbm.*
        :width: 40%
    .. image:: polblogs-sbm-generated.*
        :width: 40%

    *Left:* Political blogs network. *Right:* Sample from the degree-corrected
    SBM fitted to the original network.

    References
    ----------
    .. [karrer-stochastic-2011] Brian Karrer and M. E. J. Newman, "Stochastic
       blockmodels and community structure in networks," Physical Review E 83,
       no. 1: 016107 (2011) :doi:`10.1103/PhysRevE.83.016107` :arxiv:`1008.3926`

    """

    g = Graph()
    g.add_vertex(len(b))
    b = g.new_vp("int", b)

    if not directed:
        if out_degs is None:
            out_degs = in_degs = g.new_vp("double", 1)
        else:
            out_degs = in_degs = g.new_vp("double", out_degs)
    else:
        if out_degs is None:
            out_degs = g.new_vp("double", 1)
        else:
            out_degs = g.new_vp("double", out_degs)
        if in_degs is None:
            in_degs = g.new_vp("double", 1)
        else:
            in_degs = g.new_vp("double", in_degs)

    r, s = probs.nonzero()
    if not directed:
        idx = r <= s
        r = r[idx]
        s = s[idx]
    p = numpy.squeeze(numpy.array(probs[r, s]))

    if len(p.shape) == 0: # B == 1 special case
        p = numpy.array([p])

    g.set_directed(directed)

    libgraph_tool_generation.gen_sbm(g._Graph__graph,
                                     _prop("v", g, b),
                                     numpy.array(r, dtype="int64"),
                                     numpy.array(s, dtype="int64"),
                                     numpy.array(p, dtype="double"),
                                     _prop("v", g, in_degs),
                                     _prop("v", g, out_degs),
                                     _get_rng())
    return g

def predecessor_tree(g, pred_map):
    """Return a graph from a list of predecessors given by the ``pred_map`` vertex property."""

    _check_prop_scalar(pred_map, "pred_map")
    pg = Graph()
    libgraph_tool_generation.predecessor_graph(g._Graph__graph,
                                               pg._Graph__graph,
                                               _prop("v", g, pred_map))
    return pg


def line_graph(g):
    """Return the line graph of the given graph `g`.

    Notes
    -----
    Given an undirected graph G, its line graph L(G) is a graph such that

        * each vertex of L(G) represents an edge of G; and
        * two vertices of L(G) are adjacent if and only if their corresponding
          edges share a common endpoint ("are adjacent") in G.

    For a directed graph, the second criterion becomes:

       * Two vertices representing directed edges from u to v and from w to x in
         G are connected by an edge from uv to wx in the line digraph when v =
         w.


    Examples
    --------

    >>> g = gt.collection.data["lesmis"]
    >>> lg, vmap = gt.line_graph(g)
    >>> pos = gt.graph_draw(lg, output_size=(300, 300), output="lesmis-lg.pdf")

    .. testcode::
       :hide:

       gt.graph_draw(lg, pos=pos, output_size=(300, 300), output="lesmis-lg.png")



    .. figure:: lesmis-lg.png
       :align: center

       Line graph of the coappearance of characters in Victor Hugo's novel "Les
       Misérables".

    References
    ----------
    .. [line-wiki] http://en.wikipedia.org/wiki/Line_graph

    """
    lg = Graph(directed=g.is_directed())

    vertex_map = lg.new_vertex_property("int64_t")

    libgraph_tool_generation.line_graph(g._Graph__graph,
                                        lg._Graph__graph,
                                        _prop("v", lg, vertex_map))
    return lg, vertex_map


def graph_union(g1, g2, intersection=None, props=None, include=False,
                internal_props=False):
    """Return the union of graphs ``g1`` and ``g2``, composed of all edges and
    vertices of ``g1`` and ``g2``, without overlap (if ``intersection ==
    None``).

    Parameters
    ----------
    g1 : :class:`~graph_tool.Graph`
       First graph in the union.
    g2 : :class:`~graph_tool.Graph`
       Second graph in the union.
    intersection : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
       Vertex property map owned by `g2` which maps each of its vertices
       to vertex indexes belonging to `g1`. Negative values mean no mapping
       exists, and thus both vertices in `g1` and `g2` will be present in the
       union graph.
    props : list of tuples of :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
       Each element in this list must be a tuple of two PropertyMap objects. The
       first element must be a property of `g1`, and the second of `g2`. If either
       value is ``None``, an empty map is created. The values of the property
       maps are propagated into the union graph, and returned.
    include : bool (optional, default: ``False``)
       If ``True``, graph `g2` is inserted into `g1` which is modified. If false, a
       new graph is created, and both graphs remain unmodified.
    internal_props : bool (optional, default: ``False``)
       If ``True``, all internal property maps are propagated, in addition
       to ``props``.

    Returns
    -------
    ug : :class:`~graph_tool.Graph`
        The union graph
    props : list of :class:`~graph_tool.PropertyMap` objects
        List of propagated properties.  This is only returned if `props` is not
        empty.

    Examples
    --------

    .. testcode::
       :hide:

       from numpy.random import random, seed
       from pylab import *
       seed(42)
       gt.seed_rng(42)

    >>> g = gt.triangulation(random((300,2)))[0]
    >>> ug = gt.graph_union(g, g)
    >>> uug = gt.graph_union(g, ug)
    >>> pos = gt.sfdp_layout(g)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="graph_original.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="graph_original.png")

    >>> pos = gt.sfdp_layout(ug)
    >>> gt.graph_draw(ug, pos=pos, output_size=(300,300), output="graph_union.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(ug, pos=pos, output_size=(300,300), output="graph_union.png")

    >>> pos = gt.sfdp_layout(uug)
    >>> gt.graph_draw(uug, pos=pos, output_size=(300,300), output="graph_union2.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(uug, pos=pos, output_size=(300,300), output="graph_union2.png")


    .. image:: graph_original.*
    .. image:: graph_union.*
    .. image:: graph_union2.*

    """
    pnames = None
    if props is None:
        props = []
    if internal_props:
        pnames = []
        for (k, name), p1 in g1.properties.items():
            if k == 'g':
                continue
            p2 = g2.properties.get((k, name), None)
            props.append((p1, p2))
            pnames.append(name)
        for (k, name), p2 in g2.properties.items():
            if k == 'g' or (k, name) in g1.properties:
                continue
            props.append((None, p2))
            pnames.append(name)
        gprops = [[(name, g1.properties[('g', name)]) for name in g1.graph_properties.keys()],
                  [(name, g2.properties[('g', name)]) for name in g2.graph_properties.keys()]]
    if not include:
        g1 = GraphView(g1, skip_properties=True)
        p1s = []
        for i, (p1, p2) in enumerate(props):
            if p1 is None:
                continue
            if p1.key_type() == "v":
                g1.vp[str(i)] = p1
            elif p1.key_type() == "e":
                g1.ep[str(i)] = p1

        g1 = Graph(g1, prune=True)

        for i, (p1, p2) in enumerate(props):
            if p1 is None:
                continue
            if str(i) in g1.vp:
                props[i] = (g1.vp[str(i)], p2)
                del g1.vp[str(i)]
            else:
                props[i] = (g1.ep[str(i)], p2)
                del g1.ep[str(i)]
    else:
        emask, emask_flip = g1.get_edge_filter()
        emask_flipped = False
        if emask is not None and not emask_flip:
            emask.a = numpy.logical_not(emask.a)
            g1.set_edge_filter(emask, True)
            emask_flipped = True

        vmask, vmask_flip = g1.get_vertex_filter()
        vmask_flipped = False
        if vmask is not None and not vmask_flip:
            vmask.a = numpy.logical_not(vmask.a)
            g1.set_vertex_filter(vmask, True)
            vmask_flipped = True

    if intersection is None:
        intersection = g2.new_vertex_property("int64_t", -1)
    else:
        intersection = intersection.copy("int64_t")

    u1 = GraphView(g1, directed=True, skip_properties=True)
    u2 = GraphView(g2, directed=True, skip_properties=True)

    vmap, emap = libgraph_tool_generation.graph_union(u1._Graph__graph,
                                                      u2._Graph__graph,
                                                      _prop("v", g1,
                                                            intersection))

    if include:
        emask, emask_flip = g1.get_edge_filter()
        if emask is not None and emask_flipped:
            emask.a = numpy.logical_not(emask.a)
            g1.set_edge_filter(emask, False)

        vmask, vmask_flip = g1.get_vertex_filter()
        if vmask is not None and vmask_flipped:
            vmask.a = numpy.logical_not(vmask.a)
            g1.set_vertex_filter(vmask, False)

    n_props = []
    for p1, p2 in props:
        if p1 is None:
            p1 = g1.new_property(p2.key_type(), p2.value_type())
        if p2 is None:
            p2 = g2.new_property(p1.key_type(), p1.value_type())
        if not include:
            p1 = g1.copy_property(p1)
        if p2.value_type() != p1.value_type():
            p2 = g2.copy_property(p2, value_type=p1.value_type())
        if p1.key_type() == 'v':
            libgraph_tool_generation.\
                  vertex_property_union(u1._Graph__graph, u2._Graph__graph,
                                        vmap, emap,
                                        _prop(p1.key_type(), g1, p1),
                                        _prop(p2.key_type(), g2, p2))
        else:
            libgraph_tool_generation.\
                  edge_property_union(u1._Graph__graph, u2._Graph__graph,
                                      vmap, emap,
                                      _prop(p1.key_type(), g1, p1),
                                      _prop(p2.key_type(), g2, p2))
        n_props.append(p1)

    if pnames is not None:
        for name, p in zip(pnames, n_props):
            g1.properties[(p.key_type(), name)] = p
        if not include:
            for name, p in gprops[0]:
                g1.graph_properties[name] = g1.own_property(p.copy())
        for name, p in gprops[1]:
            if name not in g1.graph_properties:
                g1.graph_properties[name] = g1.own_property(p.copy())
        n_props = []

    if len(n_props) > 0:
        return g1, n_props
    else:
        return g1


@_limit_args({"type": ["simple", "delaunay"]})
def triangulation(points, type="simple", periodic=False):
    r"""
    Generate a 2D or 3D triangulation graph from a given point set.

    Parameters
    ----------
    points : :class:`~numpy.ndarray`
        Point set for the triangulation. It may be either a N x d array, where N
        is the number of points, and d is the space dimension (either 2 or 3).
    type : string (optional, default: ``'simple'``)
        Type of triangulation. May be either 'simple' or 'delaunay'.
    periodic : bool (optional, default: ``False``)
        If ``True``, periodic boundary conditions will be used. This is
        parameter is valid only for type="delaunay", and is otherwise ignored.

    Returns
    -------
    triangulation_graph : :class:`~graph_tool.Graph`
        The generated graph.
    pos : :class:`~graph_tool.PropertyMap`
        Vertex property map with the Cartesian coordinates.

    See Also
    --------
    random_graph: random graph generation

    Notes
    -----

    A triangulation [cgal-triang]_ is a division of the convex hull of a point
    set into triangles, using only that set as triangle vertices.

    In simple triangulations (`type="simple"`), the insertion of a point is done
    by locating a face that contains the point, and splitting this face into
    three new faces (the order of insertion is therefore important). If the
    point falls outside the convex hull, the triangulation is restored by
    flips. Apart from the location, insertion takes a time O(1). This bound is
    only an amortized bound for points located outside the convex hull.

    Delaunay triangulations (`type="delaunay"`) have the specific empty sphere
    property, that is, the circumscribing sphere of each cell of such a
    triangulation does not contain any other vertex of the triangulation in its
    interior. These triangulations are uniquely defined except in degenerate
    cases where five points are co-spherical. Note however that the CGAL
    implementation computes a unique triangulation even in these cases.

    Examples
    --------
    .. testcode::
       :hide:

       from numpy.random import random, seed
       from pylab import *
       seed(42)
       gt.seed_rng(42)
    >>> points = random((500, 2)) * 4
    >>> g, pos = gt.triangulation(points)
    >>> weight = g.new_edge_property("double") # Edge weights corresponding to
    ...                                        # Euclidean distances
    >>> for e in g.edges():
    ...    weight[e] = sqrt(sum((array(pos[e.source()]) -
    ...                          array(pos[e.target()]))**2))
    >>> b = gt.betweenness(g, weight=weight)
    >>> b[1].a *= 100
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), vertex_fill_color=b[0],
    ...               edge_pen_width=b[1], output="triang.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), vertex_fill_color=b[0],
                     edge_pen_width=b[1], output="triang.png")

    >>> g, pos = gt.triangulation(points, type="delaunay")
    >>> weight = g.new_edge_property("double")
    >>> for e in g.edges():
    ...    weight[e] = sqrt(sum((array(pos[e.source()]) -
    ...                          array(pos[e.target()]))**2))
    >>> b = gt.betweenness(g, weight=weight)
    >>> b[1].a *= 120
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), vertex_fill_color=b[0],
    ...               edge_pen_width=b[1], output="triang-delaunay.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), vertex_fill_color=b[0],
                     edge_pen_width=b[1], output="triang-delaunay.png")


    2D triangulation of random points:

    .. image:: triang.*
    .. image:: triang-delaunay.*

    *Left:* Simple triangulation. *Right:* Delaunay triangulation. The vertex
    colors and the edge thickness correspond to the weighted betweenness
    centrality.

    References
    ----------
    .. [cgal-triang] http://www.cgal.org/Manual/last/doc_html/cgal_manual/Triangulation_3/Chapter_main.html

    """

    if points.shape[1] not in [2, 3]:
        raise ValueError("points array must have shape N x d, with d either 2 or 3.")
    # copy points to ensure continuity and correct data type
    points = numpy.array(points, dtype='float64')
    if points.shape[1] == 2:
        npoints = numpy.zeros((points.shape[0], 3))
        npoints[:,:2] = points
        points = npoints
    g = Graph(directed=False)
    pos = g.new_vertex_property("vector<double>")
    libgraph_tool_generation.triangulation(g._Graph__graph, points,
                                           _prop("v", g, pos), _c_str(type),
                                           periodic)
    return g, pos


def lattice(shape, periodic=False):
    r"""
    Generate a N-dimensional square lattice.

    Parameters
    ----------
    shape : list or :class:`~numpy.ndarray`
        List of sizes in each dimension.
    periodic : bool (optional, default: ``False``)
        If ``True``, periodic boundary conditions will be used.

    Returns
    -------
    lattice_graph : :class:`~graph_tool.Graph`
        The generated graph.

    See Also
    --------
    triangulation: 2D or 3D triangulation
    random_graph: random graph generation

    Examples
    --------
    .. testcode::
       :hide:

       gt.seed_rng(42)

    >>> g = gt.lattice([10,10])
    >>> pos = gt.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="lattice.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="lattice.png")

    >>> g = gt.lattice([10,20], periodic=True)
    >>> pos = gt.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="lattice_periodic.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="lattice_periodic.png")

    >>> g = gt.lattice([10,10,10])
    >>> pos = gt.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="lattice_3d.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="lattice_3d.png")


    .. image:: lattice.*
    .. image:: lattice_periodic.*
    .. image:: lattice_3d.*

    *Left:* 10x10 2D lattice. *Middle:* 10x20 2D periodic lattice (torus).
    *Right:* 10x10x10 3D lattice.

    References
    ----------
    .. [lattice] http://en.wikipedia.org/wiki/Square_lattice

    """

    g = Graph(directed=False)
    libgraph_tool_generation.lattice(g._Graph__graph, shape, periodic)
    return g

def complete_graph(N, self_loops=False, directed=False):
    r"""
    Generate complete graph.

    Parameters
    ----------
    N : ``int``
        Number of vertices.
    self_loops : bool (optional, default: ``False``)
        If ``True``, self-loops are included.
    directed : bool (optional, default: ``False``)
        If ``True``, a directed graph is generated.

    Returns
    -------
    complete_graph : :class:`~graph_tool.Graph`
        A complete graph.

    Examples
    --------

    >>> g = gt.complete_graph(30)
    >>> pos = gt.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="complete.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="complete.png")


    .. figure:: complete.*

       A complete graph with :math:`N=30` vertices.

    References
    ----------
    .. [complete] http://en.wikipedia.org/wiki/Complete_graph

    """

    g = Graph(directed=directed)
    libgraph_tool_generation.complete(g._Graph__graph, N, directed, self_loops)
    return g

def circular_graph(N, k=1, self_loops=False, directed=False):
    r"""
    Generate a circular graph.

    Parameters
    ----------
    N : ``int``
        Number of vertices.
    k : ``int`` (optional, default: ``True``)
        Number of nearest neighbours to be connected.
    self_loops : bool (optional, default: ``False``)
        If ``True``, self-loops are included.
    directed : bool (optional, default: ``False``)
        If ``True``, a directed graph is generated.

    Returns
    -------
    circular_graph : :class:`~graph_tool.Graph`
        A circular graph.

    Examples
    --------

    >>> g = gt.circular_graph(30, 2)
    >>> pos = gt.sfdp_layout(g, cooling_step=0.95)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="circular.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="circular.png")

    .. figure:: circular.*

       A circular graph with :math:`N=30` vertices, and :math:`k=2`.

    """

    g = Graph(directed=directed)
    libgraph_tool_generation.circular(g._Graph__graph, N, k, directed, self_loops)
    return g


def geometric_graph(points, radius, ranges=None):
    r"""
    Generate a geometric network form a set of N-dimensional points.

    Parameters
    ----------
    points : list or :class:`~numpy.ndarray`
        List of points. This must be a two-dimensional array, where the rows are
        coordinates in a N-dimensional space.
    radius : float
        Pairs of points with an euclidean distance lower than this parameters
        will be connected.
    ranges : list or :class:`~numpy.ndarray` (optional, default: ``None``)
        If provided, periodic boundary conditions will be assumed, and the
        values of this parameter it will be used as the ranges in all
        dimensions. It must be a two-dimensional array, where each row will
        cointain the lower and upper bound of each dimension.

    Returns
    -------
    geometric_graph : :class:`~graph_tool.Graph`
        The generated graph.
    pos : :class:`~graph_tool.PropertyMap`
        A vertex property map with the position of each vertex.

    Notes
    -----
    A geometric graph [geometric-graph]_ is generated by connecting points
    embedded in a N-dimensional euclidean space which are at a distance equal to
    or smaller than a given radius.

    See Also
    --------
    triangulation: 2D or 3D triangulation
    random_graph: random graph generation
    lattice : N-dimensional square lattice

    Examples
    --------
    .. testcode::
       :hide:

       from numpy.random import random, seed
       from pylab import *
       seed(42)
       gt.seed_rng(42)

    >>> points = random((500, 2)) * 4
    >>> g, pos = gt.geometric_graph(points, 0.3)
    >>> gt.graph_draw(g, pos=pos, output_size=(300,300), output="geometric.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="geometric.png")

    >>> g, pos = gt.geometric_graph(points, 0.3, [(0,4), (0,4)])
    >>> pos = gt.graph_draw(g, output_size=(300,300), output="geometric_periodic.pdf")

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, output_size=(300,300), output="geometric_periodic.png")


    .. image:: geometric.*
    .. image:: geometric_periodic.*

    *Left:* Geometric network with random points. *Right:* Same network, but
     with periodic boundary conditions.

    References
    ----------
    .. [geometric-graph] Jesper Dall and Michael Christensen, "Random geometric
       graphs", Phys. Rev. E 66, 016121 (2002), :doi:`10.1103/PhysRevE.66.016121`

    """

    g = Graph(directed=False)
    pos = g.new_vertex_property("vector<double>")
    if type(points) != numpy.ndarray:
        points = numpy.array(points)
    if len(points.shape) < 2:
        raise ValueError("points list must be a two-dimensional array!")
    if ranges is not None:
        periodic = True
        if type(ranges) != numpy.ndarray:
            ranges = numpy.array(ranges, dtype="float")
        else:
            ranges = array(ranges, dtype="float")
    else:
        periodic = False
        ranges = ()

    libgraph_tool_generation.geometric(g._Graph__graph, points, float(radius),
                                       ranges, periodic,
                                       _prop("v", g, pos))
    return g, pos


def price_network(N, m=1, c=None, gamma=1, directed=True, seed_graph=None):
    r"""A generalized version of Price's -- or Barabási-Albert if undirected -- preferential attachment network model.

    Parameters
    ----------
    N : int
        Size of the network.
    m : int (optional, default: ``1``)
        Out-degree of newly added vertices.
    c : float (optional, default: ``1 if directed == True else 0``)
        Constant factor added to the probability of a vertex receiving an edge
        (see notes below).
    gamma : float (optional, default: ``1``)
        Preferential attachment power (see notes below).
    directed : bool (optional, default: ``True``)
        If ``True``, a Price network is generated. If ``False``, a
        Barabási-Albert network is generated.
    seed_graph : :class:`~graph_tool.Graph` (optional, default: ``None``)
        If provided, this graph will be used as the starting point of the
        algorithm.

    Returns
    -------
    price_graph : :class:`~graph_tool.Graph`
        The generated graph.

    Notes
    -----

    The (generalized) [price]_ network is either a directed or undirected graph
    (the latter is called a Barabási-Albert network), generated dynamically by
    at each step adding a new vertex, and connecting it to :math:`m` other
    vertices, chosen with probability :math:`\pi` defined as:

    .. math::

        \pi \propto k^\gamma + c

    where :math:`k` is the in-degree of the vertex (or simply the degree in the
    undirected case). If :math:`\gamma=1`, the tail of resulting in-degree
    distribution of the directed case is given by

    .. math::

        P_{k_\text{in}} \sim k_\text{in}^{-(2 + c/m)},

    or for the undirected case

    .. math::

        P_{k} \sim k^{-(3 + c/m)}.

    However, if :math:`\gamma \ne 1`, the in-degree distribution is not
    scale-free (see [dorogovtsev-evolution]_ for details).

    Note that if `seed_graph` is not given, the algorithm will *always* start
    with one node if :math:`c > 0`, or with two nodes with a link between them
    otherwise. If :math:`m > 1`, the degree of the newly added vertices will be
    vary dynamically as :math:`m'(t) = \min(m, V(t))`, where :math:`V(t)` is the
    number of vertices added so far. If this behaviour is undesired, a proper
    seed graph with :math:`V \ge m` vertices must be provided.

    This algorithm runs in :math:`O(V\log V)` time.

    See Also
    --------
    triangulation: 2D or 3D triangulation
    random_graph: random graph generation
    lattice : N-dimensional square lattice
    geometric_graph : N-dimensional geometric network

    Examples
    --------
    .. testcode::
       :hide:

       gt.seed_rng(42)

    >>> g = gt.price_network(20000)
    >>> gt.graph_draw(g, pos=gt.sfdp_layout(g, cooling_step=0.99),
    ...               vertex_fill_color=g.vertex_index, vertex_size=2,
    ...               edge_pen_width=1, output="price-network.png")
    <...>
    >>> g = gt.price_network(20000, c=0.1)
    >>> gt.graph_draw(g, pos=gt.sfdp_layout(g, cooling_step=0.99),
    ...               vertex_fill_color=g.vertex_index, vertex_size=2,
    ...               edge_pen_width=1, output="price-network-broader.png")
    <...>

    .. figure:: price-network.png
        :align: center

        Price network with :math:`N=2\times 10^4` nodes and :math:`c=1`.  The colors
        represent the order in which vertices were added.

    .. figure:: price-network-broader.png
        :align: center

        Price network with :math:`N=2\times 10^4` nodes and :math:`c=0.1`.  The colors
        represent the order in which vertices were added.


    References
    ----------

    .. [yule] Yule, G. U. "A Mathematical Theory of Evolution, based on the
       Conclusions of Dr. J. C. Willis, F.R.S.". Philosophical Transactions of
       the Royal Society of London, Ser. B 213: 21-87, 1925,
       :doi:`10.1098/rstb.1925.0002`
    .. [price] Derek De Solla Price, "A general theory of bibliometric and other
       cumulative advantage processes", Journal of the American Society for
       Information Science, Volume 27, Issue 5, pages 292-306, September 1976,
       :doi:`10.1002/asi.4630270505`
    .. [barabasi-albert] Barabási, A.-L., and Albert, R., "Emergence of
       scaling in random networks", Science, 286, 509, 1999,
       :doi:`10.1126/science.286.5439.509`
    .. [dorogovtsev-evolution] S. N. Dorogovtsev and J. F. F. Mendes, "Evolution
       of networks", Advances in Physics, 2002, Vol. 51, No. 4, 1079-1187,
       :doi:`10.1080/00018730110112519`
    """

    if c is None:
        c = 1 if directed else 0

    if seed_graph is None:
        g = Graph(directed=directed)
        if c > 0:
            g.add_vertex()
        else:
            g.add_vertex(2)
            g.add_edge(g.vertex(1), g.vertex(0))
        N -= g.num_vertices()
    else:
        g = seed_graph
    libgraph_tool_generation.price(g._Graph__graph, N, gamma, c, m, _get_rng())
    return g

def condensation_graph(g, prop, vweight=None, eweight=None, avprops=None,
                       aeprops=None, self_loops=False, parallel_edges=False):
    r"""
    Obtain the condensation graph, where each vertex with the same 'prop' value
    is condensed in one vertex.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be modelled.
    prop : :class:`~graph_tool.PropertyMap`
        Vertex property map with the community partition.
    vweight : :class:`~graph_tool.PropertyMap` (optional, default: None)
        Vertex property map with the optional vertex weights.
    eweight : :class:`~graph_tool.PropertyMap` (optional, default: None)
        Edge property map with the optional edge weights.
    avprops : list of :class:`~graph_tool.PropertyMap` (optional, default: None)
        If provided, the sum of each property map in this list for
        each vertex in the condensed graph will be computed and returned.
    aeprops : list of :class:`~graph_tool.PropertyMap` (optional, default: None)
        If provided, the sum of each property map in this list for
        each edge in the condensed graph will be computed and returned.
    self_loops : ``bool`` (optional, default: ``False``)
        If ``True``, self-loops due to intra-block edges are also included in
        the condensation graph.
    parallel_edges : ``bool`` (optional, default: ``False``)
        If ``True``, parallel edges will be included in the condensation graph,
        such that the total number of edges will be the same as in the original
        graph.

    Returns
    -------
    condensation_graph : :class:`~graph_tool.Graph`
        The community network
    prop : :class:`~graph_tool.PropertyMap`
        The community values.
    vcount : :class:`~graph_tool.PropertyMap`
        A vertex property map with the vertex count for each community.
    ecount : :class:`~graph_tool.PropertyMap`
        An edge property map with the inter-community edge count for each edge.
    va : list of :class:`~graph_tool.PropertyMap`
        A list of vertex property maps with summed values of the properties
        passed via the ``avprops`` parameter.
    ea : list of :class:`~graph_tool.PropertyMap`
        A list of edge property maps with summed values of the properties
        passed via the ``avprops`` parameter.

    Notes
    -----
    Each vertex in the condensation graph represents one community in the
    original graph (vertices with the same 'prop' value), and the edges
    represent existent edges between vertices of the respective communities in
    the original graph.

    Examples
    --------

    .. testsetup:: condensation_graph

       gt.seed_rng(43)
       np.random.seed(42)

    Let's first obtain the best block partition with ``B=5``.

    .. doctest:: condensation_graph

       >>> g = gt.collection.data["polbooks"]
       >>> # fit a SBM with 5 groups
       >>> state = gt.BlockState(g, B=5, deg_corr=True)
       >>> gt.mcmc_equilibrate(state, wait=1000)
       (...)
       >>> b = state.get_blocks()
       >>> gt.graph_draw(g, pos=g.vp["pos"], vertex_fill_color=b, vertex_shape=b,
       ...               output="polbooks_blocks_B5.pdf")
       <...>

    Now we get the condensation graph:

    .. doctest:: condensation_graph

       >>> bg, bb, vcount, ecount, avp, aep = \
       ...     gt.condensation_graph(g, b, avprops=[g.vp["pos"]],
       ...                           self_loops=True)
       >>> pos = avp[0]
       >>> for v in bg.vertices():
       ...     pos[v].a /= vcount[v]
       >>> gt.graph_draw(bg, pos=avp[0], vertex_fill_color=bb, vertex_shape=bb,
       ...               vertex_size=gt.prop_to_size(vcount, mi=40, ma=100),
       ...               edge_pen_width=gt.prop_to_size(ecount, mi=2, ma=10),
       ...               output="polbooks_blocks_B5_cond.pdf")
       <...>

    .. testcleanup:: condensation_graph

       gt.graph_draw(g, pos=g.vp["pos"], vertex_fill_color=b, vertex_shape=b,
                     output="polbooks_blocks_B5.png")
       gt.graph_draw(bg, pos=avp[0], vertex_fill_color=bb, vertex_shape=bb,
                     vertex_size=gt.prop_to_size(vcount, mi=40, ma=100),
                     edge_pen_width=gt.prop_to_size(ecount, mi=2, ma=10),
                     output="polbooks_blocks_B5_cond.png")

    .. figure:: polbooks_blocks_B5.*
       :align: center

       Block partition of a political books network with :math:`B=5`.

    .. figure:: polbooks_blocks_B5_cond.*
       :align: center

       Condensation graph of the obtained block partition.

    """
    gp = Graph(directed=g.is_directed())
    if vweight is None:
        vcount = gp.new_vertex_property("int32_t")
    else:
        vcount = gp.new_vertex_property(vweight.value_type())
    if eweight is None:
        ecount = gp.new_edge_property("int32_t")
    else:
        ecount = gp.new_edge_property(eweight.value_type())

    if prop is g.vertex_index:
        prop = prop.copy(value_type="int32_t")
    cprop = gp.new_vertex_property(prop.value_type())

    if avprops is None:
        avprops = []
    avp = []
    r_avp = []
    for p in avprops:
        if p is g.vertex_index:
            p = p.copy(value_type="int")
        if "string" in p.value_type():
            raise ValueError("Cannot compute sum of string properties!")
        temp = g.new_vertex_property(p.value_type())
        cp = gp.new_vertex_property(p.value_type())
        avp.append((_prop("v", g, p), _prop("v", g, temp), _prop("v", g, cp)))
        r_avp.append(cp)

    if aeprops is None:
        aeprops = []
    aep = []
    r_aep = []
    for p in aeprops:
        if p is g.edge_index:
            p = p.copy(value_type="int")
        if "string" in p.value_type():
            raise ValueError("Cannot compute sum of string properties!")
        temp = g.new_edge_property(p.value_type())
        cp = gp.new_edge_property(p.value_type())
        aep.append((_prop("e", g, p), _prop("e", g, temp), _prop("e", g, cp)))
        r_aep.append(cp)

    libgraph_tool_generation.community_network(g._Graph__graph,
                                               gp._Graph__graph,
                                               _prop("v", g, prop),
                                               _prop("v", gp, cprop),
                                               _prop("v", gp, vcount),
                                               _prop("e", gp, ecount),
                                               _prop("v", g, vweight),
                                               _prop("e", g, eweight),
                                               self_loops,
                                               parallel_edges)

    u = GraphView(g, directed=True, reversed=False)
    libgraph_tool_generation.community_network_vavg(u._Graph__graph,
                                                    gp._Graph__graph,
                                                    _prop("v", g, prop),
                                                    _prop("v", gp, cprop),
                                                    _prop("v", g, vweight),
                                                    avp)

    libgraph_tool_generation.community_network_eavg(g._Graph__graph,
                                                    gp._Graph__graph,
                                                    _prop("v", g, prop),
                                                    _prop("v", gp, cprop),
                                                    _prop("e", g, eweight),
                                                    aep, self_loops,
                                                    parallel_edges)
    return gp, cprop, vcount, ecount, r_avp, r_aep

class Sampler(libgraph_tool_generation.Sampler):
    def __init__(self, values, probs):
        libgraph_tool_generation.Sampler.__init__(self, values, probs)

    def sample(self):
        return libgraph_tool_generation.Sampler.sample(self, _get_rng())

class DynamicSampler(libgraph_tool_generation.DynamicSampler):
    def __init__(self, values=None, probs=None):
        if values is None:
            values = probs = []
        libgraph_tool_generation.DynamicSampler.__init__(self, values, probs)

    def sample(self):
        return libgraph_tool_generation.DynamicSampler.sample(self, _get_rng())
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

import numpy
from . util import *
from . mcmc import *
from . bisection import *
from . blockmodel import *
from . overlap_blockmodel import *
from . layered_blockmodel import *
from . nested_blockmodel import *

def default_args(mcmc_args={}, anneal_args={}, mcmc_equilibrate_args={},
                 shrink_args={}, mcmc_multilevel_args={}, overlap=False):
    mcmc_args = dict(dict(beta=numpy.inf, c=0, niter=5, allow_vacate=False,
                          entropy_args=dict(dl=True)), **mcmc_args)
    if overlap:
        mcmc_args = dict(mcmc_args, bundled=True)
    mcmc_equilibrate_args = dict(dict(wait=1, nbreaks=1, epsilon=1e-4,
                                      mcmc_args=mcmc_args),
                                 **dmask(mcmc_equilibrate_args,
                                         ["mcmc_args"]))
    shrink_entropy_args = dict(dict(mcmc_args["entropy_args"],
                                       dl=not overlap),
                               **shrink_args.get("entropy_args", {}))
    if not shrink_entropy_args.get("dense", False):
         shrink_entropy_args["multigraph"] = False
    shrink_args = dict(dict(entropy_args=shrink_entropy_args, niter=20),
                       **dmask(shrink_args, ["entropy_args"]))
    mcmc_multilevel_args = \
            dict(dict(r=1.3, anneal=False,
                      shrink_args=shrink_args,
                      mcmc_equilibrate_args=mcmc_equilibrate_args,
                      anneal_args=anneal_args),
                 **dmask(mcmc_multilevel_args,
                         ["shrink_args", "mcmc_equilibrate_args",
                          "anneal_args"]))
    return mcmc_multilevel_args


def get_states(g, B_min=None, B_max=None, b_min=None, b_max=None, deg_corr=True,
               overlap=False, nonoverlap_init=True, layers=False, clabel=None,
               state_args={}, mcmc_multilevel_args={}):

    if B_min is None:
        if clabel is None:
            B_min = 1
        else:
            B_min = len(set(clabel.fa))
            if b_min is None:
                b_min = clabel

    _B_max = g.num_vertices()
    if overlap and not nonoverlap_init:
        _B_max = 2 * g.num_edges()

    if B_max is None:
        B_max = _B_max
        if overlap and nonoverlap_init and b_max is None:
            b_max = g.vertex_index.copy("int")

    if layers:
        State = LayeredBlockState
        state_args = dict(state_args, overlap=overlap)
    elif overlap:
        State = OverlapBlockState
    else:
        State = BlockState

    if b_max is not None:
        max_state = State(g, b=b_max, deg_corr=deg_corr, clabel=clabel,
                          **dmask(state_args, ["B", "b", "deg_corr", "clabel"]))
    else:
        max_state = State(g, B=_B_max, deg_corr=deg_corr, clabel=clabel,
                          **dmask(state_args,["B", "b", "deg_corr", "clabel"]))

    if max_state.B > B_max:
        max_state = mcmc_multilevel(max_state, B=B_max, **mcmc_multilevel_args)

    if b_min is not None:
        min_state = State(g, B=B_min, b=b_min, deg_corr=deg_corr, clabel=clabel,
                          **dmask(state_args, ["B", "b", "deg_corr", "clabel"]))
    elif B_min == 1:
        min_state = State(g, B=1, deg_corr=deg_corr, clabel=clabel,
                          **dmask(state_args, ["B", "b", "deg_corr", "clabel"]))
    else:
        min_state = max_state.copy()

    if min_state.B > B_min:
        min_state = mcmc_multilevel(min_state, B=B_min, **mcmc_multilevel_args)

    return min_state, max_state


def minimize_blockmodel_dl(g, B_min=None, B_max=None, b_min=None, b_max=None,
                           deg_corr=True, overlap=False, nonoverlap_init=True,
                           layers=False, state_args={}, bisection_args={},
                           mcmc_args={}, anneal_args={},
                           mcmc_equilibrate_args={}, shrink_args={},
                           mcmc_multilevel_args={}, verbose=False):
    """Fit the stochastic block model.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        The graph.
    B_min : ``int`` (optional, default: ``None``)
        The minimum number of blocks.
    B_max : ``int`` (optional, default: ``None``)
        The maximum number of blocks.
    b_min : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        The partition to be used with the minimum number of blocks.
    b_max : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        The partition to be used with the maximum number of blocks.
    deg_corr : ``bool`` (optional, default: ``True``)
        If ``True``, the degree-corrected version of the model will be used.
    overlap : ``bool`` (optional, default: ``True``)
        If ``True``, the overlapping version of the model will be used.
    nonoverlap_init : ``bool`` (optional, default: ``True``)
        If ``True``, and ``overlap == True`` a non-overlapping initial state
        will be used.
    layers : ``bool`` (optional, default: ``False``)
        If ``True``, the layered version of the model will be used.
    state_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to appropriate state constructor (e.g.
        :class:`~graph_tool.inference.BlockState`,
        :class:`~graph_tool.inference.OverlapBlockState` or
        :class:`~graph_tool.inference.LayeredBlockState`)
    bisection_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.bisection_minimize`.
    mcmc_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :meth:`graph_tool.inference.BlockState.mcmc_sweep`,
        :meth:`graph_tool.inference.OverlapBlockState.mcmc_sweep` or
        :meth:`graph_tool.inference.LayeredBlockState.mcmc_sweep`.
    mcmc_equilibrate_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.mcmc_equilibrate`.
    shrink_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :meth:`graph_tool.inference.BlockState.shrink`,
        :meth:`graph_tool.inference.OverlapBlockState.shrink` or
        :meth:`graph_tool.inference.LayeredBlockState.shrink`.
    mcmc_multilevel_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.mcmc_multilevel`.
    verbose : ``bool`` or ``tuple`` (optional, default: ``False``)
        If ``True``, progress information will be shown. Optionally, this
        accepts arguments of the type ``tuple`` of the form ``(level, prefix)``
        where ``level`` is a positive integer that specifies the level of
        detail, and ``prefix`` is a string that is prepended to the all output
        messages.

    Returns
    -------
    min_state : :class:`~graph_tool.inference.BlockState` or  :class:`~graph_tool.inference.OverlapBlockState` or  :class:`~graph_tool.inference.LayeredBlockState`
        State with minimal description length.

    Notes
    -----

    This function is a convenience wrapper around
    :func:`~graph_tool.inference.bisection_minimize`.

    See [peixoto-efficient-2014]_ for details on the algorithm.

    This algorithm has a complexity of :math:`O(V \ln^2 V)`, where :math:`V` is
    the number of nodes in the network.

    Examples
    -----

    .. testsetup:: mdl

       gt.seed_rng(42)
       np.random.seed(42)

    .. doctest:: mdl

       >>> g = gt.collection.data["polbooks"]
       >>> state = gt.minimize_blockmodel_dl(g)
       >>> state.draw(pos=g.vp["pos"], vertex_shape=state.get_blocks(),
       ...            output="polbooks_blocks_mdl.pdf")
       <...>

    .. testcleanup:: mdl

       state.draw(pos=g.vp["pos"], vertex_shape=state.get_blocks(),
                  output="polbooks_blocks_mdl.png")

    .. figure:: polbooks_blocks_mdl.*
       :align: center

       Block partition of a political books network, which minimizes the
       description length of the network according to the degree-corrected
       stochastic blockmodel.


    .. testsetup:: mdl_overlap

       gt.seed_rng(42)
       np.random.seed(42)

    .. doctest:: mdl_overlap

       >>> g = gt.collection.data["polbooks"]
       >>> state = gt.minimize_blockmodel_dl(g, overlap=True)
       >>> state.draw(pos=g.vp["pos"], output="polbooks_overlap_blocks_mdl.pdf")
       <...>

    .. testcleanup:: mdl_overlap

       state.draw(pos=g.vp["pos"], output="polbooks_overlap_blocks_mdl.png")

    .. figure:: polbooks_overlap_blocks_mdl.*
       :align: center

       Overlapping partition of a political books network, which minimizes the
       description length of the network according to the overlapping
       degree-corrected stochastic blockmodel.


    References
    ----------
    .. [holland-stochastic-1983] Paul W. Holland, Kathryn Blackmond Laskey,
       Samuel Leinhardt, "Stochastic blockmodels: First steps",
       Carnegie-Mellon University, Pittsburgh, PA 15213, U.S.A.,
       :doi:`10.1016/0378-8733(83)90021-7`.
    .. [faust-blockmodels-1992] Katherine Faust, and Stanley
       Wasserman. "Blockmodels: Interpretation and Evaluation." Social Networks
       14, no. 1-2 (1992): 5-61, :doi:`10.1016/0378-8733(92)90013-W`.
    .. [karrer-stochastic-2011] Brian Karrer, and M. E. J. Newman. "Stochastic
       Blockmodels and Community Structure in Networks." Physical Review E 83,
       no. 1 (2011): 016107, :doi:`10.1103/PhysRevE.83.016107`.
    .. [peixoto-entropy-2012] Tiago P. Peixoto "Entropy of Stochastic Blockmodel
       Ensembles." Physical Review E 85, no. 5 (2012): 056122,
       :doi:`10.1103/PhysRevE.85.056122`, :arxiv:`1112.6028`.
    .. [peixoto-parsimonious-2013] Tiago P. Peixoto, "Parsimonious module
       inference in large networks", Phys. Rev. Lett. 110, 148701 (2013),
       :doi:`10.1103/PhysRevLett.110.148701`, :arxiv:`1212.4794`.
    .. [peixoto-efficient-2014] Tiago P. Peixoto, "Efficient Monte Carlo and greedy
       heuristic for the inference of stochastic block models", Phys. Rev. E 89,
       012804 (2014), :doi:`10.1103/PhysRevE.89.012804`, :arxiv:`1310.4378`.
    .. [peixoto-model-2016] Tiago P. Peixoto, "Model selection and hypothesis
       testing for large-scale network models with overlapping groups",
       Phys. Rev. X 5, 011033 (2016), :doi:`10.1103/PhysRevX.5.011033`,
       :arxiv:`1409.3059`.
    .. [peixoto-inferring-2016] Tiago P. Peixoto, "Inferring the mesoscale
       structure of layered, edge-valued and time-varying networks",
       Phys. Rev. E 92, 042807 (2015), :doi:`10.1103/PhysRevE.92.042807`,
       :arXiv:`1504.02381`.

    """

    b_cache = {} # keep a global cache

    mcmc_multilevel_args = \
        default_args(mcmc_args=mcmc_args,
                     anneal_args=anneal_args,
                     mcmc_equilibrate_args=mcmc_equilibrate_args,
                     shrink_args=shrink_args,
                     mcmc_multilevel_args=dict(mcmc_multilevel_args,
                                               b_cache=b_cache),
                     overlap=overlap)

    bisection_args = dict(dict(mcmc_multilevel_args=mcmc_multilevel_args,
                               random_bisection=False),
                          **bisection_args)

    clabel = state_args.get("clabel", None)
    if clabel is None:
        clabel = state_args.get("pclabel", None)

    min_state, max_state = get_states(g, B_min=B_min, B_max=B_max, b_min=b_min,
                                      b_max=b_max, deg_corr=deg_corr,
                                      overlap=overlap,
                                      nonoverlap_init=nonoverlap_init,
                                      layers=layers, clabel=clabel,
                                      state_args=state_args,
                                      mcmc_multilevel_args=mcmc_multilevel_args)

    if B_min is None:
        B_min = 1
    if B_max is None:
        B_max = numpy.inf

    Bs = list(b_cache.keys())
    for B in Bs:
        if B > B_max or B < B_min:
            del b_cache[B]

    state = bisection_minimize([min_state, max_state], verbose=verbose,
                               **bisection_args)

    return state

def minimize_nested_blockmodel_dl(g, B_min=None, B_max=None, b_min=None,
                                  b_max=None, Bs=None, bs=None, deg_corr=True,
                                  overlap=False, nonoverlap_init=True,
                                  layers=False, hierarchy_minimize_args={},
                                  state_args={}, bisection_args={},
                                  mcmc_args={}, anneal_args={},
                                  mcmc_equilibrate_args={}, shrink_args={},
                                  mcmc_multilevel_args={}, verbose=False):
    """Fit the nested stochastic block model.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        The graph.
    B_min : ``int`` (optional, default: ``None``)
        The minimum number of blocks.
    B_max : ``int`` (optional, default: ``None``)
        The maximum number of blocks.
    b_min : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        The partition to be used with the minimum number of blocks.
    b_max : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        The partition to be used with the maximum number of blocks.
    Bs : ``list`` of ints (optional, default: ``None``)
        If provided, it will correspond to the sizes of the initial hierarchy.
    bs : ``list`` of integer-valued :class:`numpy.ndarray` objects (optional, default: ``None``)
        If provided, it will correspond to the initial hierarchical partition.
    deg_corr : ``bool`` (optional, default: ``True``)
        If ``True``, the degree-corrected version of the model will be used.
    overlap : ``bool`` (optional, default: ``True``)
        If ``True``, the overlapping version of the model will be used.
    nonoverlap_init : ``bool`` (optional, default: ``True``)
        If ``True``, and ``overlap == True`` a non-overlapping initial state
        will be used.
    layers : ``bool`` (optional, default: ``False``)
        If ``True``, the layered version of the model will be used.
    hierarchy_minimize_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.hierarchy_minimize`.
    state_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to appropriate state constructor (e.g.
        :class:`~graph_tool.inference.BlockState`,
        :class:`~graph_tool.inference.OverlapBlockState` or
        :class:`~graph_tool.inference.LayeredBlockState`)
    bisection_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.bisection_minimize`.
    mcmc_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :meth:`graph_tool.inference.BlockState.mcmc_sweep`,
        :meth:`graph_tool.inference.OverlapBlockState.mcmc_sweep` or
        :meth:`graph_tool.inference.LayeredBlockState.mcmc_sweep`.
    mcmc_equilibrate_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.mcmc_equilibrate`.
    shrink_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :meth:`graph_tool.inference.BlockState.shrink`,
        :meth:`graph_tool.inference.OverlapBlockState.shrink` or
        :meth:`graph_tool.inference.LayeredBlockState.shrink`.
    mcmc_multilevel_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.mcmc_multilevel`.
    verbose : ``bool`` or ``tuple`` (optional, default: ``False``)
        If ``True``, progress information will be shown. Optionally, this
        accepts arguments of the type ``tuple`` of the form ``(level, prefix)``
        where ``level`` is a positive integer that specifies the level of
        detail, and ``prefix`` is a string that is prepended to the all output
        messages.

    Returns
    -------
    min_state : :class:`~graph_tool.inference.NestedBlockState`
        Nested state with minimal description length.

    Notes
    -----

    This function is a convenience wrapper around
    :func:`~graph_tool.inference.hierarchy_minimize`.

    See [peixoto-hierarchical-2014]_ for details on the algorithm.

    This algorithm has a complexity of :math:`O(V \ln^2 V)`, where :math:`V` is
    the number of nodes in the network.

    Examples
    --------
    .. testsetup:: nested_mdl

       gt.seed_rng(43)
       np.random.seed(43)

    .. doctest:: nested_mdl

       >>> g = gt.collection.data["power"]
       >>> state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)
       >>> state.draw(output="power_nested_mdl.pdf")
       (...)

    .. testcleanup:: nested_mdl

       state.draw(output="power_nested_mdl.png")

    .. figure:: power_nested_mdl.*
       :align: center

       Hierarchical Block partition of a power-grid network, which minimizes
       the description length of the network according to the nested
       (degree-corrected) stochastic blockmodel.


    .. doctest:: nested_mdl_overlap

       >>> g = gt.collection.data["celegansneural"]
       >>> state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True, overlap=True)
       >>> state.draw(output="celegans_nested_mdl_overlap.pdf")
       (...)

    .. testcleanup:: nested_mdl_overlap

       state.draw(output="celegans_nested_mdl_overlap.png")

    .. figure:: celegans_nested_mdl_overlap.*
       :align: center

       Overlapping block partition of the *C. elegans* neural network, which
       minimizes the description length of the network according to the nested
       overlapping degree-corrected stochastic blockmodel.

    References
    ----------

    .. [peixoto-hierarchical-2014] Tiago P. Peixoto, "Hierarchical block
       structures and high-resolution model selection in large networks ",
       Phys. Rev. X 4, 011047 (2014), :doi:`10.1103/PhysRevX.4.011047`,
       :arxiv:`1310.4377`.
    .. [peixoto-efficient-2014] Tiago P. Peixoto, "Efficient Monte Carlo and
       greedy heuristic for the inference of stochastic block models",
       Phys. Rev. E 89, 012804 (2014), :doi:`10.1103/PhysRevE.89.012804`,
       :arxiv:`1310.4378`.
    .. [peixoto-model-2016] Tiago P. Peixoto, "Model selection and hypothesis
       testing for large-scale network models with overlapping groups",
       Phys. Rev. X 5, 011033 (2016), :doi:`10.1103/PhysRevX.5.011033`,
       :arxiv:`1409.3059`.
    .. [peixoto-inferring-2016] Tiago P. Peixoto, "Inferring the mesoscale
       structure of layered, edge-valued and time-varying networks",
       Phys. Rev. E 92, 042807 (2015), :doi:`10.1103/PhysRevE.92.042807`,
       :arXiv:`1504.02381`.

    """

    mcmc_multilevel_args = \
            default_args(mcmc_args=mcmc_args,
                         anneal_args=anneal_args,
                         mcmc_equilibrate_args=mcmc_equilibrate_args,
                         shrink_args=shrink_args,
                         mcmc_multilevel_args=mcmc_multilevel_args,
                         overlap=overlap)

    if bs is None:
        clabel = state_args.get("clabel", None)
        if clabel is None:
            clabel = state_args.get("pclabel", None)
        min_state, max_state = get_states(g, B_min=B_min, B_max=B_max,
                                          b_min=b_min, b_max=b_max,
                                          deg_corr=deg_corr, overlap=overlap,
                                          nonoverlap_init=nonoverlap_init,
                                          layers=layers, clabel=clabel,
                                          state_args=dmask(state_args,
                                                           ["hstate_args",
                                                            "hentropy_args"]),
                                          mcmc_multilevel_args=mcmc_multilevel_args)
        if b_max is None:
            b_max = max_state.b.fa
        if b_min is None:
            b_min = min_state.b.fa
        if Bs is None:
            bs = [min_state.b.fa, zeros(min_state.b.fa.max() + 1, dtype="int")]
        else:
            bs = []
            bstate = max_state
            for B in Bs:
                bstate = mcmc_multilevel(bstate, B=B,
                                         verbose=verbose_push(verbose,
                                                              ("l = %d " %
                                                               len(bs))),
                                         **mcmc_multilevel_args)
                bs.append(bstate.b.a)
                bstate = bstate.get_block_state()

    if layers:
        state_args = dict(state_args, overlap=overlap)

    state = NestedBlockState(g, bs=bs,
                             base_type=type(min_state),
                             deg_corr=deg_corr,
                             **dmask(state_args, ["deg_corr"]))

    bisection_args = dict(dict(mcmc_multilevel_args=mcmc_multilevel_args,
                               random_bisection=False),
                          **bisection_args)

    hierarchy_minimize(state, B_max=B_max, B_min=B_min, b_max=b_max,
                       b_min=b_min, bisection_args=bisection_args,
                       verbose=verbose,
                       **dmask(hierarchy_minimize_args,
                               ["B_max", "B_min", "bisection_args", "verbose"]))

    return state
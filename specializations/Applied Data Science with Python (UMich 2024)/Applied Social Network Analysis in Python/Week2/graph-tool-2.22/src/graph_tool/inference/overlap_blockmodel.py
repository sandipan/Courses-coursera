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
    conv_pickle_state

import random
from numpy import *
import numpy
from collections import defaultdict

from .. import group_vector_property, ungroup_vector_property

from .. dl_import import dl_import
dl_import("from . import libgraph_tool_inference as libinference")

from . blockmodel import *
from . blockmodel import _bm_test

class OverlapBlockState(BlockState):
    r"""The overlapping stochastic block model state of a given graph.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be modelled.
    b : :class:`~graph_tool.PropertyMap` or :class:`numpy.ndarray` (optional, default: ``None``)
        Initial block labels on the vertices or half-edges. If not supplied, it
        will be randomly sampled.
        If the value passed is a vertex property map, it will be assumed to be a
        non-overlapping partition of the vertices. If it is an edge property
        map, it should contain a vector for each edge, with the block labels at
        each end point (sorted according to their vertex index, in the case of
        undirected graphs, otherwise from source to target). If the value is an
        :class:`numpy.ndarray`, it will be assumed to correspond directly to a
        partition of the list of half-edges.
    B : ``int`` (optional, default: ``None``)
        Number of blocks (or vertex groups). If not supplied it will be obtained
        from the parameter ``b``.
    recs : list of :class:`~graph_tool.PropertyMap` instances (optional, default: ``[]``)
        List of real or discrete-valued edge covariates.
    rec_types : list of edge covariate types (optional, default: ``[]``)
        List of types of edge covariates. The possible types are:
        ``"real-exponential"``, ``"real-normal"``, ``"discrete-geometric"``,
        ``"discrete-poisson"`` or ``"discrete-binomial"``.
    rec_params : list of ``dict`` (optional, default: ``[]``)
        Model hyperparameters for edge covariates. This should a list of
        ``dict`` instances. See :class:`~graph_tool.inference.BlockState` for
        more details.
    clabel : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        Constraint labels on the vertices. If supplied, vertices with different
        label values will not be clustered in the same group.
    deg_corr : ``bool`` (optional, default: ``True``)
        If ``True``, the degree-corrected version of the blockmodel ensemble will
        be assumed, otherwise the traditional variant will be used.
    allow_empty : ``bool`` (optional, default: ``True``)
        If ``True``, partition description length computed will allow for empty
        groups.
    max_BE : ``int`` (optional, default: ``1000``)
        If the number of blocks exceeds this number, a sparse representation of
        the block graph is used, which is slightly less efficient, but uses less
        memory,
    """

    def __init__(self, g, b=None, B=None, recs=[], rec_types=[], rec_params=[],
                 clabel=None, pclabel=None, deg_corr=True, allow_empty=True,
                 max_BE=1000, **kwargs):

        kwargs = kwargs.copy()

        # determine if there is a base graph, and overlapping structure
        self.base_g = kwargs.pop("base_g", None)

        # overlapping information
        node_index = kwargs.pop("node_index", None)
        node_in_degs = kwargs.pop("node_in_degs", None)
        node_out_degs = kwargs.pop("node_out_degs", None)
        half_edges = kwargs.pop("half_edges", None)
        eindex = kwargs.pop("eindex", None)

        if node_index is not None and self.base_g is None:
            raise ValueError("Must specify base graph if node_index is specified...")

        # create overlapping structure
        if node_index is None:
            # keep base graph
            self.base_g = g

            if len(recs) == 0:
                rec = self.base_g.new_ep("vector<double>")
            else:
                recs = [x.copy("double") for x in recs]
                rec = group_vector_property(recs)

            # substitute provided graph by its half-edge graph
            g, b, node_index, half_edges, eindex, rec = \
                                                half_edge_graph(g, b, B, rec)

        # create half edges set if absent
        if half_edges is None:
            half_edges = self.base_g.new_vertex_property("vector<int64_t>")
            libinference.get_nodeset_overlap(g._Graph__graph,
                                             _prop("v", g, node_index),
                                             _prop("v", self.base_g, half_edges))

        self.overlap = True
        self.node_index = node_index
        self.half_edges = half_edges
        self.eindex = eindex

        # configure the main graph and block model parameters
        self.g = g

        self.deg_corr = deg_corr

        self.is_edge_weighted = False
        self.is_vertex_weighted = False
        self.is_weighted = False

        if b is None:
            # create a random partition into B blocks.
            B = min(B, self.g.num_vertices())
            ba = random.randint(0, B, self.g.num_vertices())
            ba[:B] = arange(B)        # avoid empty blocks
            if B < self.g.num_vertices():
                random.shuffle(ba)
            b = g.new_vertex_property("int")
            b.fa = ba
            self.b = b
        else:
            # if a partition is available, we will incorporate it.
            # in the overlapping case
            # at this point, *b* must correspond to the partition of
            # *half-edges*
            if isinstance(b, numpy.ndarray):
                self.b = g.new_vertex_property("int")
                self.b.fa = b
            else:
                b = b.copy(value_type="int")
                b = g.own_property(b)
                self.b = b
            if B is None:
                B = int(self.b.fa.max()) + 1

        if self.b.fa.max() >= B:
            raise ValueError("Maximum value of b is larger or equal to B!")

        self.recs = recs
        if len(recs) == 0:
            self.rec = self.g.new_ep("vector<double>")
        else:
            recs = [x.copy("double") for x in recs]
            self.rec = group_vector_property(recs)
        self.drec = kwargs.pop("drec", None)
        if self.drec is None:
            if len(self.recs) == 0:
                self.drec = self.g.new_ep("vector<double>")
            else:
                drecs = [x.copy("double") for x in self.recs]
                for r in drecs:
                    r.fa **= 2
                self.drec = group_vector_property(drecs)
        else:
            self.drec = self.drec.copy()

        # Construct block-graph
        self.bg = get_block_graph(g, B, self.b, rec=self.rec, drec=self.drec)
        self.bg.set_fast_edge_removal()

        self.mrs = self.bg.ep["count"]
        self.wr = self.bg.vp["count"]

        del self.bg.ep["count"]
        del self.bg.vp["count"]

        self.mrp = self.bg.degree_property_map("out", weight=self.mrs)

        if g.is_directed():
            self.mrm = self.bg.degree_property_map("in", weight=self.mrs)
        else:
            self.mrm = self.mrp

        self.B = B

        self.candidate_blocks = Vector_size_t()
        self.candidate_blocks.extend(arange(self.B, dtype="int"))

        if pclabel is not None:
            if isinstance(pclabel, PropertyMap):
                self.pclabel = self.g.own_property(pclabel).copy("int")
            else:
                self.pclabel = self.g.new_vp("int")
                self.pclabel.fa = pclabel
        else:
            self.pclabel = self.g.new_vp("int")

        if clabel is not None:
            if isinstance(clabel, PropertyMap):
                self.clabel = self.g.own_property(clabel).copy("int")
            else:
                self.clabel = self.g.new_vp("int")
                self.clabel.fa = clabel
        elif self.pclabel.fa.max() > 0:
            self.clabel = self.pclabel
        else:
            self.clabel = self.g.new_vp("int")

        self.bclabel = self.get_bclabel()

        BlockState._init_recs(self, recs, rec_types, rec_params)

        self.max_BE = max_BE

        self.use_hash = self.B > self.max_BE

        self.allow_empty = allow_empty

        self._abg = self.bg._get_any()
        self._state = libinference.make_overlap_block_state(self, _get_rng())

        if deg_corr:
            init_q_cache(max(self.get_E(), self.get_N()) + 1)

        self._entropy_args = dict(adjacency=True, dl=True, partition_dl=True,
                                  degree_dl=True, degree_dl_kind="distributed",
                                  edges_dl=True, dense=False, multigraph=True,
                                  exact=True, recs=True)

        if len(kwargs) > 0:
            warnings.warn("unrecognized keyword arguments: " +
                          str(list(kwargs.keys())))

    def __repr__(self):
        return "<OverlapBlockState object with %d blocks,%s for graph %s, at 0x%x>" % \
            (self.B, " degree corrected," if self.deg_corr else "",
             str(self.base_g), id(self))

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        g = copy.deepcopy(self.g, memo)
        node_index = g.own_property(copy.deepcopy(self.node_index, memo))
        eindex = g.own_property(copy.deepcopy(self.eindex, memo))
        half_edges = base_g.own_property(copy.deepcopy(self.half_edges, memo))
        base_g = copy.deepcopy(self.base_g, memo)
        return self.copy(g=g, node_index=node_index, eindex=eindex,
                         half_edges=half_edges, base_g=base_g)

    def copy(self, g=None, b=None, B=None, deg_corr=None, clabel=None,
             pclabel=None, **kwargs):
        r"""Copies the block state. The parameters override the state properties, and
         have the same meaning as in the constructor. If ``overlap=False`` an
         instance of :class:`~graph_tool.community.BlockState` is returned. This
         is by default a shallow copy."""

        recs = ungroup_vector_property(self.rec, range(len(self.recs)))

        state = OverlapBlockState(self.g if g is None else g,
                                  b=self.b if b is None else b,
                                  B=(self.B if b is None else None) if B is None else B,
                                  clabel=self.clabel.fa if clabel is None else clabel,
                                  pclabel=self.pclabel if pclabel is None else pclabel,
                                  deg_corr=self.deg_corr if deg_corr is None else deg_corr,
                                  recs=kwargs.pop("recs", recs),
                                  drec=kwargs.pop("drec", self.drec),
                                  rec_types=kwargs.pop("rec_types", self.rec_types),
                                  rec_params=kwargs.pop("rec_params",
                                                        self.rec_params),
                                  half_edges=kwargs.get("half_edges", self.half_edges),
                                  node_index=kwargs.get("node_index", self.node_index),
                                  eindex=kwargs.get("eindex", self.eindex),
                                  max_BE=kwargs.get("max_BE", self.max_BE),
                                  base_g=kwargs.get("base_g", self.base_g),
                                  **dmask(kwargs, ["half_edges", "node_index",
                                                   "eindex", "base_g", "drec",
                                                   "max_BE"]))
        return state

    def __getstate__(self):
        state = dict(g=self.g,
                     b=self.b,
                     B=self.B,
                     clabel=array(self.clabel.fa),
                     deg_corr=self.deg_corr,
                     recs=ungroup_vector_property(self.rec,
                                                  range(len(self.recs))),
                     drec=self.drec,
                     rec_types=list(self.rec_types),
                     rec_params=self.rec_params,
                     half_edges=self.half_edges,
                     node_index=self.node_index,
                     eindex=self.eindex,
                     max_BE=self.max_BE,
                     base_g=self.base_g)
        return state

    def __setstate__(self, state):
        conv_pickle_state(state)
        self.__init__(**state)

    def get_block_state(self, b=None, vweight=False, deg_corr=False, **kwargs):
        r"""Returns a :class:`~graph_tool.community.BlockState` corresponding to the
        block graph. The parameters have the same meaning as the in the
        constructor."""

        bg = self.bg.copy()
        mrs = bg.own_property(self.mrs.copy())
        wr = bg.own_property(self.wr.copy())
        state = BlockState(bg, eweight=mrs,
                           vweight=wr if vweight else None,
                           b=bg.vertex_index.copy("int") if b is None else b,
                           deg_corr=deg_corr,
                           rec_types=kwargs.pop("rec_types",
                                                self.rec_types if vweight else []),
                           recs=kwargs.pop("recs",
                                           ungroup_vector_property(bg.ep.rec,
                                                                   range(len(self.rec_types)))
                                           if (vweight and len(self.rec_types) > 0)
                                           else []),
                           drec=kwargs.pop("drec",
                                           bg.ep.drec if (vweight is not None and
                                                          len(self.rec_types) > 0)
                                           else None),
                           rec_params=kwargs.pop("rec_params", self.rec_params),
                           allow_empty=kwargs.pop("allow_empty",
                                                  self.allow_empty),
                           max_BE=self.max_BE,
                           **kwargs)
        return state

    def get_E(self):
        r"Returns the total number of edges."
        return self.g.num_edges()

    def get_N(self):
        r"Returns the total number of nodes."
        return self.base_g.num_vertices()

    def get_B(self):
        r"Returns the total number of blocks."
        return self.bg.num_vertices()

    def get_nonempty_B(self):
        r"Returns the total number of nonempty blocks."
        return int((self.wr.a > 0).sum())

    def get_edge_blocks(self):
        r"""Returns an edge property map which contains the block labels pairs for each
        edge."""
        be = self.base_g.new_edge_property("vector<int>")
        self._state.get_be_overlap(self.base_g._Graph__graph,
                                    _prop("e", self.base_g, be))
        return be

    def get_overlap_blocks(self):
        r"""Returns the mixed membership of each vertex.

        Returns
        -------
        bv : :class:`~graph_tool.PropertyMap`
           A vector-valued vertex property map containing the block memberships
           of each node.
        bc_in : :class:`~graph_tool.PropertyMap`
           The labelled in-degrees of each node, i.e. how many in-edges belong
           to each group, in the same order as the ``bv`` property above.
        bc_out : :class:`~graph_tool.PropertyMap`
           The labelled out-degrees of each node, i.e. how many out-edges belong
           to each group, in the same order as the ``bv`` property above.
        bc_total : :class:`~graph_tool.PropertyMap`
           The labelled total degrees of each node, i.e. how many incident edges
           belong to each group, in the same order as the ``bv`` property above.

        """
        bv = self.base_g.new_vertex_property("vector<int>")
        bc_in = self.base_g.new_vertex_property("vector<int>")
        bc_out = self.base_g.new_vertex_property("vector<int>")
        bc_total = self.base_g.new_vertex_property("vector<int>")
        self._state.get_bv_overlap(self.base_g._Graph__graph,
                                    _prop("v", self.base_g, bv),
                                    _prop("v", self.base_g, bc_in),
                                    _prop("v", self.base_g, bc_out),
                                    _prop("v", self.base_g, bc_total))
        return bv, bc_in, bc_out, bc_total

    def get_nonoverlap_blocks(self):
        r"""Returns a scalar-valued vertex property map with the block mixture
        represented as a single number."""

        bv = self.get_overlap_blocks()[0]
        b = self.base_g.new_vertex_property("int")
        self._state.get_overlap_split(self.base_g._Graph__graph,
                                       _prop("v", self.base_g, bv),
                                       _prop("v", self.base_g, b))
        return b

    def get_majority_blocks(self):
        r"""Returns a scalar-valued vertex property map with the majority block
        membership of each node."""

        bv = self.get_overlap_blocks()
        bv, bc = bv[0], bv[-1]
        b = self.base_g.new_vertex_property("int")
        self._state.get_maj_overlap(self.base_g._Graph__graph,
                                     _prop("v", self.base_g, bv),
                                     _prop("v", self.base_g, bc),
                                     _prop("v", self.base_g, b))
        return b

    def entropy(self, adjacency=True, dl=True, partition_dl=True,
                degree_dl=True, degree_dl_kind="distributed", edges_dl=True,
                dense=False, multigraph=True, deg_entropy=True, recs=True,
                exact=True, **kwargs):
        r"""Calculate the entropy associated with the current block partition.

        Parameters
        ----------
        adjacency : ``bool`` (optional, default: ``True``)
            If ``True``, the adjacency term of the description length will be
            included.
        dl : ``bool`` (optional, default: ``True``)
            If ``True``, the description length for the parameters will be
            included.
        partition_dl : ``bool`` (optional, default: ``True``)
            If ``True``, and ``dl == True`` the partition description length
            will be included.
        degree_dl : ``bool`` (optional, default: ``True``)
            If ``True``, and ``dl == True`` the degree sequence description
            length will be included (for degree-corrected models).
        degree_dl_kind : ``str`` (optional, default: ``"distributed"``)
            This specifies the prior used for the degree sequence. It must be
            one of: ``"uniform"``, ``"distributed"`` (default) or ``"entropy"``.
        edges_dl : ``bool`` (optional, default: ``True``)
            If ``True``, and ``dl == True`` the edge matrix description length
            will be included.
        dense : ``bool`` (optional, default: ``False``)
            If ``True``, the "dense" variant of the entropy will be computed.
        multigraph : ``bool`` (optional, default: ``True``)
            If ``True``, the multigraph entropy will be used.
        deg_entropy : ``bool`` (optional, default: ``True``)
            If ``True``, the degree entropy term that is independent of the
            network partition will be included (for degree-corrected models).
        recs : ``bool`` (optional, default: ``True``)
            If ``True``, the likelihood for real or discrete-valued edge
            covariates is computed.
        exact : ``bool`` (optional, default: ``True``)
            If ``True``, the exact expressions will be used. Otherwise,
            Stirling's factorial approximation will be used for some terms.

        Notes
        -----

        The "entropy" of the state is minus the log-likelihood of the
        microcanonical SBM, that includes the generated graph
        :math:`\boldsymbol{A}` and the model parameters :math:`\boldsymbol{\theta}`,

        .. math::

           \mathcal{S} &= - \ln P(\boldsymbol{A},\boldsymbol{\theta}) \\
                       &= - \ln P(\boldsymbol{A}|\boldsymbol{\theta}) - \ln P(\boldsymbol{\theta}).

        This value is also called the `description length
        <https://en.wikipedia.org/wiki/Minimum_description_length>`_ of the data,
        and it corresponds to the amount of information required to describe it
        (in `nats <https://en.wikipedia.org/wiki/Nat_(unit)>`_).

        For the traditional blockmodel (``deg_corr == False``), the model
        parameters are :math:`\boldsymbol{\theta} = \{\boldsymbol{e},
        \boldsymbol{b}\}`, where :math:`\boldsymbol{e}` is the matrix of edge
        counts between blocks, and :math:`\boldsymbol{b}` is the `overlapping`
        partition of the nodes into blocks. For the degree-corrected blockmodel
        (``deg_corr == True``), we have an additional set of parameters, namely
        the `labelled` degree sequence :math:`\boldsymbol{k}`.

        The model likelihood :math:`P(\boldsymbol{A}|\theta)` is given
        analogously to the non-overlapping case, as described in
        :meth:`graph_tool.inference.BlockState.entropy`.

        If ``dl == True``, the description length :math:`\mathcal{L} = -\ln
        P(\boldsymbol{\theta})` of the model will be returned as well. The
        edge-count prior :math:`P(\boldsymbol{e})` is described in described in
        :func:`model_entropy`. For the overlapping partition
        :math:`P(\boldsymbol{b})`, we have

        .. math::

           -\ln P(\boldsymbol{b}) = \ln\left(\!\!{D \choose N}\!\!\right) + \sum_d \ln {\left(\!\!{{B\choose d}\choose n_d}\!\!\right)} + \ln N! - \sum_{\vec{b}}\ln n_{\vec{b}}!,

        where :math:`d \equiv |\vec{b}|_1 = \sum_rb_r` is the mixture
        size, :math:`n_d` is the number of nodes in a mixture of size :math:`d`,
        :math:`D` is the maximum value of :math:`d`, :math:`n_{\vec{b}}` is the
        number of nodes in mixture :math:`\vec{b}`.


        For the degree-corrected model we need to specify the prior
        :math:`P(\boldsymbol{k})` for the `labelled` degree sequence as well:

        .. math::

            -\ln P(\boldsymbol{k}) = \sum_r\ln\left(\!\!{m_r \choose e_r}\!\!\right) - \sum_{\vec{b}}\ln P(\boldsymbol{k}|{\vec{b}}),

        where :math:`m_r` is the number of non-empty mixtures which contain type
        :math:`r`, and :math:`P(\boldsymbol{k}|{\vec{b}})` is the likelihood of
        the labelled degree sequence inside mixture :math:`\vec{b}`. For this
        term we have three options:

        1. ``degree_dl_kind == "uniform"``

            .. math::

                P(\boldsymbol{k}|\vec{b}) = \prod_r\left(\!\!{n_{\vec{b}}\choose e^r_{\vec{b}}}\!\!\right)^{-1}.

        2. ``degree_dl_kind == "distributed"``

            .. math::

                P(\boldsymbol{k}|\vec{b}) = \prod_{\vec{b}}\frac{\prod_{\vec{k}}\eta_{\vec{k}}^{\vec{b}}!}{n_{\vec{b}}!} \prod_r q(e_{\vec{b}}^r, n_{\vec{b}})

            where :math:`n^{\vec{b}}_{\vec{k}}` is the number of nodes in
            mixture :math:`\vec{b}` with labelled degree :math:`\vec{k}`, and
            :math:`q(n,m)` is the number of `partitions
            <https://en.wikipedia.org/wiki/Partition_(number_theory)>`_ of
            integer :math:`n` into at most :math:`m` parts.

        3. ``degree_dl_kind == "entropy"``

            .. math::

                P(\boldsymbol{k}|\vec{b}) = \prod_{\vec{b}}\exp\left(-n_{\vec{b}}H(\boldsymbol{k}_{\vec{b}})\right)

            where :math:`H(\boldsymbol{k}_{\vec{b}}) =
            -\sum_{\vec{k}}p_{\vec{b}}(\vec{k})\ln p_{\vec{b}}(\vec{k})` is the
            entropy of the labelled degree distribution inside mixture
            :math:`\vec{b}`.

            Note that, differently from the other two choices, this represents
            only an approximation of the description length. It is meant to be
            used only for comparison purposes, and should be avoided in practice.


        For the directed case, the above expressions are duplicated for the in-
        and out-degrees.

        """

        return BlockState.entropy(self, adjacency=adjacency, dl=dl,
                                  partition_dl=partition_dl,
                                  degree_dl=degree_dl,
                                  degree_dl_kind=degree_dl_kind,
                                  edges_dl=edges_dl, dense=dense,
                                  multigraph=multigraph,
                                  deg_entropy=deg_entropy, recs=recs,
                                  exact=exact, **kwargs)


    def _mcmc_sweep_dispatch(self, mcmc_state):
        dS, nmoves = libinference.overlap_mcmc_sweep(mcmc_state, self._state,
                                                     _get_rng())
        if self.__bundled:
            ret = libinference.overlap_mcmc_bundled_sweep(mcmc_state,
                                                          self._state,
                                                          _get_rng())
            dS += ret[0]
            nmoves += ret[1]
        del self.__bundled
        return dS, nmoves

    def mcmc_sweep(self, bundled=False, **kwargs):
        r"""Perform sweeps of a Metropolis-Hastings rejection sampling MCMC to sample
        network partitions. If ``bundled == True``, the half-edges incident of
        the same node that belong to the same group are moved together. All
        remaining parameters are passed to
        :meth:`graph_tool.inference.BlockState.mcmc_sweep`."""
        self.__bundled = bundled
        return BlockState.mcmc_sweep(self, **kwargs)

    def _multiflip_mcmc_sweep_dispatch(self, mcmc_state):
        return libinference.multiflip_mcmc_overlap_sweep(mcmc_state,
                                                         self._state,
                                                         _get_rng())

    def _multicanonical_sweep_dispatch(self, multicanonical_state):
        return libinference.multicanonical_overlap_sweep(multicanonical_state,
                                                         self._state,
                                                         _get_rng())

    def _exhaustive_sweep_dispatch(self, exhaustive_state, callback, hist):
        if callback is not None:
            return libinference.exhaustive_overlap_sweep(exhaustive_state,
                                                         self._state, callback)
        else:
            if hist is None:
                return libinference.exhaustive_overlap_sweep_iter(exhaustive_state,
                                                                  self._state)
            else:
                return libinference.exhaustive_overlap_dens(exhaustive_state,
                                                            self._state,
                                                            hist[0], hist[1],
                                                            hist[2])

    def _gibbs_sweep_dispatch(self, gibbs_state):
        return libinference.gibbs_overlap_sweep(multicanonical_state,
                                                self._state,
                                                _get_rng())

    def _merge_sweep_dispatch(self, merge_state):
        return libinference.vacate_overlap_sweep(merge_state, self._state,
                                                 _get_rng())

    def shrink(self, B, **kwargs):
        """Reduces the order of current state by progressively merging groups,
        until only ``B`` are left. All remaining keyword arguments are passed to
        :meth:`graph_tool.inference.BlockState.merge_sweep`.

        This function leaves the current state untouched and returns instead a
        copy with the new partition.
        """

        b = self.b.copy()
        continuous_map(b)
        bstate = self.copy(b=b)

        assert self.get_nonempty_B() == bstate.get_nonempty_B(), \
            "Error: inconsistent number of groups after copying (%d, %d)" % \
            (self.get_nonempty_B(), bstate.get_nonempty_B())

        if bstate.get_nonempty_B() < B:
            raise ValueError("cannot shrink state to a smaller number" +
                             " of groups: %d -> %d (total: %d)" %
                             (bstate.get_nonempty_B(), B, self.B))

        while bstate.get_nonempty_B() > B:
            bstate.merge_sweep(bstate.get_nonempty_B() - B, **kwargs)

        continuous_map(bstate.b)
        bstate = self.copy(b=bstate.b.a)

        if _bm_test():
            assert bstate.get_nonempty_B() == B, \
                "wrong number of groups after shrink: %d, %d" % \
                (bstate.get_nonempty_B(), B)
            assert bstate.wr.a.min() > 0, "empty group after shrink!"

        return bstate

    def draw(self, **kwargs):
        r"""Convenience wrapper to :func:`~graph_tool.draw.graph_draw` that
        draws the state of the graph as colors on the vertices and edges."""

        bv, bc_in, bc_out, bc_total = self.get_overlap_blocks()
        if self.deg_corr:
            pie_fractions = bc_total.copy("vector<double>")
        else:
            pie_fractions = self.base_g.new_vp("vector<double>",
                                               vals=[ones(len(bv[v])) for v
                                                     in self.base_g.vertices()])

        gradient = kwargs.get("edge_gradient",
                              get_block_edge_gradient(self.base_g,
                                                      self.get_edge_blocks(),
                                                      cmap=kwargs.get("ecmap",
                                                                      None)))
        from graph_tool.draw import graph_draw
        return graph_draw(self.base_g,
                          vertex_shape=kwargs.get("vertex_shape", "pie"),
                          vertex_pie_colors=kwargs.get("vertex_pie_colors", bv),
                          vertex_pie_fractions=kwargs.get("vertex_pie_fractions",
                                                          pie_fractions),
                          edge_gradient=gradient,
                          **dmask(kwargs, ["vertex_shape", "vertex_pie_colors",
                                           "vertex_pie_fractions",
                                           "edge_gradient"]))


def half_edge_graph(g, b=None, B=None, rec=None):
    r"""Generate a half-edge graph, where each half-edge is represented by a node,
    and an edge connects the half-edges like in the original graph."""

    E = g.num_edges()

    b_array = None
    if b is None:
        # if no partition is given, obtain a random one.
        ba = random.randint(0, B, 2 * E)
        ba[:B] = arange(B)        # avoid empty blocks
        if B < len(ba):
            random.shuffle(ba)
        b = ba

    if isinstance(b, numpy.ndarray):
        # if given an array, assume it corresponds to the *final* half-edge
        # partitions
        b_array = b
        b = g.new_vertex_property("int")

    if b.key_type() == "v":
        # If a vertex partition is given, we convert it into a
        # non-overlapping edge partition
        be = g.new_edge_property("vector<int>")
        libinference.get_be_from_b_overlap(g._Graph__graph,
                                           _prop("e", g, be),
                                           _prop("v", g, b))
        b = be
    else:
        # If an half-edge partition is provided, we incorporate it
        b = b.copy(value_type="vector<int32_t>")

    if B is None:
        if b_array is None:
            bs, bt = ungroup_vector_property(b, [0, 1])
            B = int(max(bs.fa.max(), bt.fa.max())) + 1
        else:
            B = b_array.max() + 1

    bs, bt = ungroup_vector_property(b, [0, 1])

    if bs.fa.max() >= B or bt.fa.max() >= B or (b_array is not None and b_array.max() >= B):
        raise ValueError("Maximum value of b is larger or equal to B!")

    eg = Graph(directed=g.is_directed())
    node_index = eg.new_vertex_property("int64_t")
    half_edges = g.new_vertex_property("vector<int64_t>")
    be = eg.new_vertex_property("int")
    eindex = eg.new_edge_property("int64_t")
    erec = eg.new_edge_property("vector<double>")

    if rec is None:
        rec_ = g.new_edge_property("vector<double>")
    else:
        rec_ = rec

    # create half-edge graph
    libinference.get_eg_overlap(g._Graph__graph,
                                eg._Graph__graph,
                                _prop("e", g, b),
                                _prop("v", eg, be),
                                _prop("v", eg, node_index),
                                _prop("v", g, half_edges),
                                _prop("e", eg, eindex),
                                _prop("e", g, rec_),
                                _prop("e", eg, erec))

    if b_array is not None:
        be.a = b_array

    if rec is None:
        erec = None

    return eg, be, node_index, half_edges, eindex, erec

def augmented_graph(g, b, node_index, eweight=None):
    r"""Generates an augmented graph from the half-edge graph ``g`` partitioned
    according to ``b``, where each half-edge belonging to a different group
    inside each node forms a new node."""

    node_map = g.new_vertex_property("int")
    br_b = libcore.Vector_int32_t()
    br_ni = libcore.Vector_int32_t()
    libinference.get_augmented_overlap(g._Graph__graph,
                                       _prop("v", g, b),
                                       _prop("v", g, node_index),
                                       _prop("v", g, node_map),
                                       br_b, br_ni)


    au, idx, vcount, ecount = condensation_graph(g, node_map,
                                                 eweight=eweight,
                                                 self_loops=True)[:4]
    anidx = idx.copy("int")
    libinference.vector_map(anidx.a, br_ni.a)

    ab = idx.copy("int")
    libinference.vector_map(ab.a, br_b.a)

    return au, ab, anidx, ecount, node_map

def get_block_edge_gradient(g, be, cmap=None):
    r"""Get edge gradients corresponding to the block membership at the endpoints of
    the edges given by the ``be`` edge property map.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        The graph.
    be : :class:`~graph_tool.PropertyMap`
        Vector-valued edge property map with the block membership at each
        endpoint.
    cmap : :class:`matplotlib.colors.Colormap` (optional, default: ``default_cm``)
        Color map used to construct the gradient.

    Returns
    -------
    cp : :class:`~graph_tool.PropertyMap`
       A vector-valued edge property map containing a color gradient.
    """

    if cmap is None:
        from .. draw import default_cm
        cmap = default_cm

    cp = g.new_edge_property("vector<double>")
    rg = [numpy.inf, -numpy.inf]
    for e in g.edges():
        s, t = be[e]
        rg[0] = min(s, rg[0])
        rg[0] = min(t, rg[0])
        rg[1] = max(s, rg[1])
        rg[1] = max(t, rg[1])

    for e in g.edges():
        if int(e.source()) < int(e.target()) or g.is_directed():
            s, t = be[e]
        else:
            t, s = be[e]
        cs = cmap((s - rg[0]) / max(rg[1] - rg[0], 1))
        ct = cmap((t - rg[0]) / max(rg[1] - rg[0], 1))
        cp[e] = [0] + list(cs) + [1] + list(ct)
    return cp

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

from .. import _degree, _prop, Graph, GraphView, conv_pickle_state
from . blockmodel import *
from . blockmodel import _bm_test
from . overlap_blockmodel import *
from . layered_blockmodel import *

from numpy import *
import numpy
import copy

def get_edges_dl(state, hstate_args, hentropy_args):
    bclabel = state.get_bclabel()
    bstate = state.get_block_state(b=bclabel, **hstate_args)
    return bstate.entropy(**dict(hentropy_args, dl=True, edges_dl=False,
                                 multigraph=True))


class NestedBlockState(object):
    r"""The nested stochastic block model state of a given graph.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be modeled.
    bs : ``list`` of :class:`~graph_tool.PropertyMap` or :class:`numpy.ndarray`
        Hierarchical node partition.
    base_type : ``type`` (optional, default: :class:`~graph_tool.inference.BlockState`)
        State type for lowermost level
        (e.g. :class:`~graph_tool.inference.BlockState`,
        :class:`~graph_tool.inference.OverlapBlockState` or
        :class:`~graph_tool.inference.LayeredBlockState`)
    hstate_args : ``dict`` (optional, default: `{}`)
        Keyword arguments to be passed to the constructor of the higher-level
        states.
    hentropy_args : ``dict`` (optional, default: `{}`)
        Keyword arguments to be passed to the ``entropy()`` method of the
        higher-level states.
    sampling : ``bool`` (optional, default: ``False``)
        If ``True``, the state will be properly prepared for MCMC sampling (as
        opposed to minimization).
    state_args : ``dict`` (optional, default: ``{}``)
        Keyword arguments to be passed to base type constructor.
    **kwargs :  keyword arguments
        Keyword arguments to be passed to base type constructor. The
        ``state_args`` parameter overrides this.
    """

    def __init__(self, g, bs, base_type=BlockState, state_args={},
                 hstate_args={}, hentropy_args={}, sampling=False, **kwargs):
        self.g = g
        self.state_args = dict(kwargs, **state_args)
        self.hstate_args = dict(dict(deg_corr=False), **hstate_args)
        self.sampling = sampling
        if sampling:
            self.hstate_args = dict(self.hstate_args, vweight="nonempty",
                                    copy_bg=False, B=g.num_vertices())
            self.state_args = dict(self.state_args, B=g.num_vertices())
            if self.state_args.get("vweight", None) is None:
                self.state_args["vweight"] = "unity"
            if self.state_args.get("eweight", None) is None:
                self.state_args["eweight"] = "unity"
            nbs = []
            for b in bs:
                nb = numpy.zeros(g.num_vertices(), dtype="int")
                nb[:len(b)] = b
                nbs.append(nb)
            bs = nbs
        self.hentropy_args = dict(dict(adjacency=True,
                                       dense=True,
                                       multigraph=True,
                                       dl=True,
                                       partition_dl=True,
                                       degree_dl=True,
                                       degree_dl_kind="distributed",
                                       edges_dl=True,
                                       exact=True,
                                       recs=False),
                                  **hentropy_args)
        self.levels = [base_type(g, b=bs[0], **self.state_args)]
        for i, b in enumerate(bs[1:]):
            state = self.levels[-1]
            args = self.hstate_args
            if i == len(bs[1:]) - 1:
                args = dict(args, clabel=None, pclabel=None)
            bstate = state.get_block_state(b=b, **args)
            self.levels.append(bstate)

        if _bm_test():
            self._consistency_check()

    def _regen_levels(self):
        for l in range(1, len(self.levels)):
            state = self.levels[l]
            nstate = self.levels[l-1].get_block_state(b=state.b,
                                                      **self.hstate_args)
            self.levels[l] = nstate

    def __repr__(self):
        return "<NestedBlockState object, with base %s, and %d levels of sizes %s at 0x%x>" % \
            (repr(self.levels[0]), len(self.levels),
             str([(s.get_N(), s.get_nonempty_B()) for s in self.levels]), id(self))

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        g = copy.deepcopy(self.g, memo)
        return self.copy(g=g)

    def copy(self, g=None, bs=None, state_args=None, hstate_args=None,
             hentropy_args=None, sampling=None, **kwargs):
        r"""Copies the block state. The parameters override the state properties,
        and have the same meaning as in the constructor."""
        bs = self.get_bs() if bs is None else bs
        return NestedBlockState(self.g if g is None else g, bs,
                                base_type=type(self.levels[0]),
                                state_args=self.state_args if state_args is None else state_args,
                                hstate_args=self.hstate_args if hstate_args is None else hstate_args,
                                hentropy_args=self.hentropy_args if hentropy_args is None else hentropy_args,
                                sampling=self.sampling if sampling is None else sampling,
                                **kwargs)

    def __getstate__(self):
        state = dict(g=self.g, bs=self.get_bs(), base_type=type(self.levels[0]),
                     hstate_args=self.hstate_args,
                     hentropy_args=self.hentropy_args, sampling=self.sampling,
                     state_args=self.state_args)
        return state

    def __setstate__(self, state):
        conv_pickle_state(state)
        if "kwargs" in state: # backwards compatibility
            state["state_args"] = state["kwargs"]
            del  state["kwargs"]
        self.__init__(**state)

    def get_bs(self):
        """Get hierarchy levels as a list of :class:`numpy.ndarray` objects with the
        group memberships at each level.
        """
        return [s.b.fa for s in self.levels]

    def get_levels(self):
        """Get hierarchy levels as a list of :class:`~graph_tool.inference.BlockState`
        instances."""
        return self.levels

    def project_partition(self, j, l):
        """Project partition of level ``j`` onto level ``l``, and return it."""
        b = self.levels[l].b.copy()
        for i in range(l + 1, j + 1):
            clabel = self.levels[i].b.copy()
            pmap(b, clabel)
        return b

    def propagate_clabel(self, l):
        """Project base clabel to level ``l``."""
        clabel = self.levels[0].clabel.copy()
        for j in range(l):
            bg = self.levels[j].bg
            bclabel = bg.new_vertex_property("int")
            reverse_map(self.levels[j].b, bclabel)
            pmap(bclabel, clabel)
            clabel = bclabel
        return clabel

    def get_clabel(self, l):
        """Get clabel for level ``l``."""
        clabel = self.propagate_clabel(l)
        if l < len(self.levels) - 1:
            b = self.project_partition(l + 1, l)
            clabel.fa += (clabel.fa.max() + 1) * b.fa
        return clabel

    def _consistency_check(self):
        for l in range(1, len(self.levels)):
            b = self.levels[l].b.fa.copy()
            state = self.levels[l-1]
            args = self.hstate_args
            if l == len(self.levels) - 1:
                args = dict(args, clabel=None, pclabel=None)
            bstate = state.get_block_state(b=b, **args)
            b2 = bstate.b.fa.copy()
            continuous_map(b)
            continuous_map(b2)
            assert ((b == b2).all() and
                    (bstate.entropy(dl=False) -
                     self.levels[l].entropy(dl=False))) < 1e-6, \
                "inconsistent level %d (%s %g,  %s %g): %s" % \
                (l, str(bstate), bstate.entropy(), str(self.levels[l]),
                 self.levels[l].entropy(), str(self))
            assert (bstate.get_N() >= bstate.get_nonempty_B()), \
                (l, bstate.get_N(), bstate.get_nonempty_B(), str(self))

    def replace_level(self, l, b):
        """Replace level ``l`` given the new partition ``b``"""

        if l < len(self.levels) - 1:
            clabel = self.project_partition(l + 1, l)
        self.levels[l] = self.levels[l].copy(b=b)
        if l < len(self.levels) - 1:
            bclabel = self.levels[l].bg.new_vertex_property("int")
            reverse_map(self.levels[l].b, bclabel)
            pmap(bclabel, clabel)
            bstate = self.levels[l].get_block_state(b=bclabel,
                                                    **self.hstate_args)
            self.levels[l + 1] = bstate

        if _bm_test():
            self._consistency_check()

    def delete_level(self, l):
        """Delete level ``l``."""
        if l == 0:
            raise ValueError("cannot delete level l=0")
        b = self.project_partition(l, l - 1)
        self.replace_level(l - 1, b.fa)
        del self.levels[l]

        if _bm_test():
            self._consistency_check()

    def duplicate_level(self, l):
        """Duplicate level ``l``."""
        bstate = self.levels[l].copy(b=self.levels[l].g.vertex_index.copy("int").fa)
        self.levels.insert(l, bstate)

        if _bm_test():
            self._consistency_check()

    def level_entropy(self, l, bstate=None, **kwargs):
        """Compute the entropy of level ``l``."""

        if bstate is None:
            bstate = self.levels[l]

        if l > 0:
            eargs = self.hentropy_args
        else:
            eargs = kwargs

        S = bstate.entropy(**dict(eargs, dl=True,
                                  edges_dl=(l == (len(self.levels) - 1))))
        return S

    def entropy(self, **kwargs):
        """Compute the entropy of whole hierarchy.

        The keyword arguments are passed to the ``entropy()`` method of the
        underlying state objects
        (e.g. :class:`graph_tool.inference.BlockState.entropy`,
        :class:`graph_tool.inference.OverlapBlockState.entropy`, or
        :class:`graph_tool.inference.LayeredBlockState.entropy`).  """
        S = 0
        for l in range(len(self.levels)):
            S += self.level_entropy(l, **kwargs)
        return S

    def move_vertex(self, v, s):
        r"""Move vertex ``v`` to block ``s``."""
        self.levels[0].move_vertex(v, s)
        self._regen_levels()

    def remove_vertex(self, v):
        r"""Remove vertex ``v`` from its current group.

        This optionally accepts a list of vertices to remove.

        .. warning::

           This will leave the state in an inconsistent state before the vertex
           is returned to some other group, or if the same vertex is removed
           twice.
        """
        self.levels[0].remove_vertex(v)
        self._regen_levels()

    def add_vertex(self, v, r):
        r"""Add vertex ``v`` to block ``r``.

        This optionally accepts a list of vertices and blocks to add.

        .. warning::

           This can leave the state in an inconsistent state if a vertex is
           added twice to the same group.
        """
        self.levels[0].add_vertex(v, r)
        self._regen_levels()

    def get_edges_prob(self, missing, spurious=[], entropy_args={}):
        """Compute the joint log-probability of the missing and spurious edges given by
        ``missing`` and ``spurious`` (a list of ``(source, target)``
        tuples, or :meth:`~graph_tool.Edge` instances), together with the
        observed edges.

        More precisely, the log-likelihood returned is

        .. math::

            \ln \frac{P(\boldsymbol G + \delta \boldsymbol G | \boldsymbol b)}{P(\boldsymbol G| \boldsymbol b)}

        where :math:`\boldsymbol G + \delta \boldsymbol G` is the modified graph
        (with missing edges added and spurious edges deleted).

        The values in ``entropy_args`` are passed to
        :meth:`graph_tool.BlockState.entropy()` to calculate the
        log-probability.
        """

        L = 0
        for l, lstate in enumerate(self.levels):
            if l > 0:
                eargs = self.hentropy_args
            else:
                eargs = entropy_args

            eargs = dict(eargs, dl=True,
                         edges_dl=(l == (len(self.levels) - 1)))

            if self.sampling:
                lstate._couple_state(None, None)
                if l > 0:
                    lstate._state.sync_emat()
                    lstate._state.clear_egroups()

            L += lstate.get_edges_prob(missing, spurious, entropy_args=eargs)
            if isinstance(self.levels[0], LayeredBlockState):
                missing = [(lstate.b[u], lstate.b[v], l_) for u, v, l_ in missing]
                spurious = [(lstate.b[u], lstate.b[v], l_) for u, v, l_ in spurious]
            else:
                missing = [(lstate.b[u], lstate.b[v]) for u, v in missing]
                spurious = [(lstate.b[u], lstate.b[v]) for u, v in spurious]

        return L


    def get_bstack(self):
        """Return the nested levels as individual graphs.

        This returns a list of :class:`~graph_tool.Graph` instances
        representing the inferred hierarchy at each level. Each graph has two
        internal vertex and edge property maps named "count" which correspond to
        the vertex and edge counts at the lower level, respectively. Additionally,
        an internal vertex property map named "b" specifies the block partition.
        """

        bstack = []
        for l, bstate in enumerate(self.levels):
            cg = bstate.g
            if l == 0:
                cg = GraphView(cg, skip_properties=True)
            cg.vp["b"] = bstate.b.copy()
            if bstate.is_weighted:
                cg.ep["count"] = cg.own_property(bstate.eweight.copy())
                cg.vp["count"] = cg.own_property(bstate.vweight.copy())
            else:
                cg.ep["count"] = cg.new_ep("int", 1)

            bstack.append(cg)
            if bstate.get_N() == 1:
                break
        return bstack

    def project_level(self, l):
        """Project the partition at level ``l`` onto the lowest level, and return the
        corresponding state."""
        b = self.project_partition(l, 0)
        return self.levels[0].copy(b=b)

    def print_summary(self):
        """Print a hierarchy summary."""
        for l, state in enumerate(self.levels):
            print("l: %d, N: %d, B: %d" % (l, state.get_N(),
                                           state.get_nonempty_B()))

    def find_new_level(self, l, sparse_thres=100, bisection_args={}, B_min=None,
                       B_max=None, b_min=None, b_max=None):
        """Attempt to find a better network partition at level ``l``, using
        :func:`~graph_tool.inference.bisection_minimize` with arguments given by
        ``bisection_args``.

        If the number of nodes is larger than `sparse_thres`, the graph is
        treated as a sparse graph for minimization purposes (the full entropy is
        always computed exactly).
        """

        # assemble minimization arguments
        mcmc_multilevel_args = bisection_args.get("mcmc_multilevel_args", {})
        mcmc_equilibrate_args = mcmc_multilevel_args.get("mcmc_equilibrate_args", {})
        mcmc_args = mcmc_equilibrate_args.get("mcmc_args", {})
        entropy_args = mcmc_args.get("entropy_args", {})
        entropy_args = dict(entropy_args, dl=True,
                            edges_dl=l==len(self.levels) - 1)
        extra_entropy_args = bisection_args.get("extra_entropy_args", {})
        if l > 0 and self.hentropy_args.get("dense"):
            entropy_args = dict(entropy_args,
                                dense=self.levels[l].get_N() < sparse_thres)
            if self.levels[l].get_N() >= sparse_thres:
                extra_entropy_args = dict(extra_entropy_args, dense=True)
        if l < len(self.levels) - 1:
            entropy_args = dict(entropy_args,
                                callback=lambda s: get_edges_dl(s,
                                                                self.hstate_args,
                                                                self.hentropy_args))
        mcmc_args = dict(mcmc_args, entropy_args=entropy_args,
                         disable_callback_test=isinstance(self.levels[0],
                                                          LayeredBlockState))
        if l > 0:
            mcmc_args = dmask(mcmc_args, ["bundled"])
        mcmc_equilibrate_args = dict(mcmc_equilibrate_args,
                                     mcmc_args=mcmc_args)
        mcmc_multilevel_args = dict(mcmc_multilevel_args,
                                    mcmc_equilibrate_args=mcmc_equilibrate_args)
        bisection_args = dict(bisection_args,
                              mcmc_multilevel_args=mcmc_multilevel_args,
                              extra_entropy_args=extra_entropy_args)

        # construct boundary states and constraints
        clabel = self.get_clabel(l)
        state = self.levels[l]
        if b_max is None:
            b_max = state.g.vertex_index.copy("int").fa
        else:
            b_max = state.g.new_vp("int", b_max)
            b_max = group_vector_property([b_max, clabel])
            b_max = perfect_prop_hash([b_max])[0].fa
        continuous_map(b_max)
        max_state = state.copy(b=b_max, clabel=clabel)
        if B_max is not None and max_state.B > B_max:
            max_state = mcmc_multilevel(max_state, B_max,
                                        **mcmc_multilevel_args)
        if l < len(self.levels) - 1:
            if B_min is None:
                min_state = state.copy(b=clabel.fa, clabel=clabel.fa)
                B_min = min_state.B
            else:
                B_min = max(B_min, clabel.fa.max() + 1)
                min_state = mcmc_multilevel(max_state, B_min,
                                            **mcmc_multilevel_args)
            if _bm_test():
                assert (min_state.B == self.levels[l+1].B or
                        min_state.B == B_min), (B_min, min_state.B,
                                                self.levels[l+1].B)
        else:
            min_state = state.copy(b=clabel.fa, clabel=clabel.fa)
        if B_min is not None and  min_state.B > B_min:
            min_state = mcmc_multilevel(min_state, B_min,
                                        **mcmc_multilevel_args)

        if _bm_test():
            assert min_state._check_clabel(), "invalid clabel %s" % str((l, self))
            assert max_state._check_clabel(), "invalid clabel %s" % str((l, self))

        # find new state
        state = bisection_minimize([min_state, max_state], **bisection_args)

        if _bm_test():
            assert state.B >= min_state.B, (l, state.B, min_state.B, str(self))
            assert state._check_clabel(), "invalid clabel %s" % str((l, self))
        return state

    def _h_sweep(self, algo, **kwargs):

        if not self.sampling:
            raise ValueError("NestedBlockState must be constructed with 'sampling=True'")

        verbose = kwargs.get("verbose", False)
        entropy_args = kwargs.get("entropy_args", {})

        for l in range(len(self.levels) - 1):
            eargs = dict(self.hentropy_args,
                         edges_dl=(l + 1 == len(self.levels) - 1))
            self.levels[l]._couple_state(self.levels[l + 1],
                                         get_entropy_args(eargs))

        dS = 0
        nmoves = 0

        c = kwargs.get("c", None)

        lrange = list(range(len(self.levels)))
        numpy.random.shuffle(lrange)
        for l in lrange:
            if check_verbose(verbose):
                print(verbose_pad(verbose) + "level:", l)
            if l > 0:
                eargs = dict(self.hentropy_args,
                             **dict(entropy_args, multigraph=True))
            else:
                eargs = entropy_args

            eargs = dict(eargs, dl=True,
                         edges_dl=(l == len(self.levels) - 1))

            if l < len(self.levels) - 1:
                def callback(s):
                    s = self.levels[l + 1]
                    S = s.entropy(**dict(self.hentropy_args,
                                         edges_dl=(l + 1 == len(self.levels) - 1)))
                    return S
                eargs = dict(eargs, callback=callback)

            if l < len(self.levels) - 1:
                self.levels[l].bclabel.a = self.levels[l + 1].b.a

            self.levels[l]._state.sync_emat()
            if l > 0:
                self.levels[l]._state.clear_egroups()
                self.levels[l]._state.rebuild_neighbour_sampler()

            if c is None:
                args = dict(kwargs, entropy_args=eargs)
            else:
                args = dict(kwargs, entropy_args=eargs, c=c[l])

            if l > 0:
                N_ = self.levels[l].get_N()
                idx_ = self.levels[l].wr.a == 0
                rs = arange(len(idx_), dtype="int")
                rs = rs[idx_]
                rs = rs[:N_]
                self.levels[l].empty_blocks.resize(len(rs))
                self.levels[l].empty_blocks.a = rs
                if len(rs) > 0:
                    reverse_map(rs, self.levels[l].empty_pos)

            ret = algo(self.levels[l], **args)

            dS += ret[0]
            nmoves += ret[1]

        return dS, nmoves

    def mcmc_sweep(self, **kwargs):
        r"""Perform ``niter`` sweeps of a Metropolis-Hastings acceptance-rejection
        MCMC to sample hierarchical network partitions.

        The arguments accepted are the same as in
        :method:`graph_tool.inference.BlockState.mcmc_sweep`.

        If the parameter ``c`` is a scalar, the values used at each level are
        ``c * 2 ** l`` for ``l`` in the range ``[0, L-1]``. Optionally, a list
        of values may be passed instead, which specifies the value of ``c[l]``
        to be used at each level.
        """

        c = kwargs.pop("c", 1)
        if not isinstance(c, collections.Iterable):
            c = [c] + [c * 2 ** l for l in range(1, len(self.levels))]

        return self._h_sweep(lambda s, **a: s.mcmc_sweep(**a), c=c, **kwargs)

    def multiflip_mcmc_sweep(self, **kwargs):
        r"""Perform ``niter`` sweeps of a Metropolis-Hastings acceptance-rejection MCMC
        with multiple moves to sample hierarchical network partitions.

        The arguments accepted are the same as in
        :method:`graph_tool.inference.BlockState.multiflip_mcmc_sweep`.

        If the parameter ``c`` is a scalar, the values used at each level are
        ``c * 2 ** l`` for ``l`` in the range ``[0, L-1]``. Optionally, a list
        of values may be passed instead, which specifies the value of ``c[l]``
        to be used at each level.

        """

        c = kwargs.pop("c", 1)
        if not isinstance(c, collections.Iterable):
            c = [c] + [c * 2 ** l for l in range(1, len(self.levels))]

        return self._h_sweep(lambda s, **a: s.multiflip_mcmc_sweep(**a), c=c, **kwargs)

    def gibbs_sweep(self, **kwargs):
        r"""Perform ``niter`` sweeps of a rejection-free Gibbs MCMC to sample network
        partitions.

        The arguments accepted are the same as in
        :method:`graph_tool.inference.BlockState.gibbs_sweep`.
        """
        return self._h_sweep(lambda s, **a: s.gibbs_sweep(**a))

    def multicanonical_sweep(self, **kwargs):
        r"""Perform ``niter`` sweeps of a non-Markovian multicanonical sampling using the
        Wang-Landau algorithm.

        The arguments accepted are the same as in
        :method:`graph_tool.inference.BlockState.multicanonical_sweep`.
        """
        return self._h_sweep(lambda s, **a: s.multicanonical_sweep(**a))

    def collect_partition_histogram(self, h=None, update=1):
        r"""Collect a histogram of partitions.

        This should be called multiple times, e.g. after repeated runs of the
        :meth:`graph_tool.inference.NestedBlockState.mcmc_sweep` function.

        Parameters
        ----------
        h : :class:`~graph_tool.inference.PartitionHist` (optional, default: ``None``)
            Partition histogram. If not provided, an empty histogram will be created.
        update : float (optional, default: ``1``)
            Each call increases the current count by the amount given by this
            parameter.

        Returns
        -------
        h : :class:`~graph_tool.inference.PartitionHist` (optional, default: ``None``)
            Updated Partition histogram.

        """

        if h is None:
            h = PartitionHist()
        bs = [_prop("v", state.g, state.b) for state in self.levels]
        libinference.collect_hierarchical_partitions(bs, h, update)
        return h

    def draw(self, **kwargs):
        r"""Convenience wrapper to :func:`~graph_tool.draw.draw_hierarchy` that
        draws the hierarchical state."""
        import graph_tool.draw
        return graph_tool.draw.draw_hierarchy(self, **kwargs)



def hierarchy_minimize(state, B_min=None, B_max=None, b_min=None, b_max=None,
                       frozen_levels=None, sparse_thres=100, bisection_args={},
                       epsilon=1e-8, verbose=False):
    """Attempt to find a fit of the nested stochastic block model that minimizes the
    description length.

    Parameters
    ----------
    state : :class:`~graph_tool.inference.NestedBlockState`
        The nested block state.
    B_min : ``int`` (optional, default: ``None``)
        The minimum number of blocks.
    B_max : ``int`` (optional, default: ``None``)
        The maximum number of blocks.
    b_min : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        The partition to be used with the minimum number of blocks.
    b_max : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        The partition to be used with the maximum number of blocks.
    frozen_levels : sequence of ``int`` values (optional, default: ``None``)
        List of hierarchy levels that are kept constant during the minimization.
    sparse_thres : int (optional, default: ``100``)
        If the number of nodes in a given level is larger than `sparse_thres`,
        the graph is treated as a sparse graph for minimization purposes (the
        full entropy is always computed exactly).
    bisection_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.bisection_minimize`.
    epsilon: ``float`` (optional, default: ``1e-8``)
        Only replace levels if the description length difference is above this
        threshold.
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

    This algorithms moves along the hierarchical levels, attempting to replace,
    delete or insert partitions that minimize the description length, until no
    further progress is possible.

    See [peixoto-hierarchical-2014]_ for details on the algorithm.

    This algorithm has a complexity of :math:`O(V \ln^2 V)`, where :math:`V` is
    the number of nodes in the network.

    References
    ----------

    .. [peixoto-hierarchical-2014] Tiago P. Peixoto, "Hierarchical block
       structures and high-resolution model selection in large networks ",
       Phys. Rev. X 4, 011047 (2014), :doi:`10.1103/PhysRevX.4.011047`,
       :arxiv:`1310.4377`.
    """

    dS = 0

    if frozen_levels is None:
        frozen_levels = set()

    l = len(state.levels) - 1  # begin from top!
    done = []
    while l >= 0:

        bisection_args = dict(bisection_args,
                              verbose=verbose_push(verbose, ("    l=%d  " % l)))

        while len(done) < len(state.levels) + 2:
            done.append(False)

        if done[l]:
            if check_verbose(verbose):
                print(verbose_pad(verbose) + "level", l, ": skipping",
                      state.levels[l].B)
            l -= 1
            continue

        Si = state.entropy()

        kept = True

        if l in frozen_levels:
            kept = False

        # replace level
        if kept:
            Si = state.entropy()

            if l < len(state.levels) - 1:
                bstates = [state.levels[l], state.levels[l+1]]
            else:
                bstates = [state.levels[l]]

            if l == 0:
                bstate = state.find_new_level(l, bisection_args=bisection_args,
                                              B_min=B_min, B_max=B_max,
                                              b_min=b_min, b_max=b_max)
            else:
                bstate = state.find_new_level(l, bisection_args=bisection_args)
            state.replace_level(l, bstate.b.fa)

            Sf = state.entropy()

            if Si - Sf > epsilon:
                kept = False
                dS += Sf - Si

                if check_verbose(verbose):
                    print(verbose_pad(verbose) + "level", l, ": replaced",
                          (bstates[0].get_N(), bstates[0].get_nonempty_B()), "->",
                          (bstate.get_N(), bstate.get_nonempty_B()),", dS:",
                          Sf - Si, len(state.levels))
            else:
                state.levels[l:l+len(bstates)] = bstates

                if check_verbose(verbose):
                    print(verbose_pad(verbose) + "level", l,
                          ": rejected replacement",
                          (bstates[0].get_N(), bstates[0].get_nonempty_B()), "->",
                          (bstate.get_N(), bstate.get_nonempty_B()),", dS:",
                          Sf - Si)

        # delete level
        if (kept and l > 0 and l < len(state.levels) - 1 and
            not (B_min is not None and l == 1 and state.levels[l].B < B_min)):

            Si = state.entropy()

            bstates = [state.levels[l-1], state.levels[l]]

            state.delete_level(l)

            Sf = state.entropy()

            if Si - Sf < epsilon:
                state.levels[l - 1] = bstates[0]
                state.levels.insert(l, bstates[1])
            else:
                kept = False
                del done[l]
                dS += Sf - Si

                if check_verbose(verbose):
                    print(verbose_pad(verbose) + "level", l, ": deleted",
                          (bstates[1].get_N(), bstates[1].get_nonempty_B()),
                          ", dS:", Sf - Si, len(state.levels))

            if _bm_test():
                if kept:
                    assert abs(state.entropy() - Si) < 1e-6, \
                    "inconsistent delete at level %d (%g, %g)" % \
                    (l, state.entropy(), Si)

        # insert new level (duplicate and replace)
        if kept and l > 0:
            Si = state.entropy()

            bstates = [state.levels[l]]
            if l < len(state.levels) - 1:
                bstates.append(state.levels[l + 1])
            if l < len(state.levels) - 2:
                bstates.append(state.levels[l + 2])

            state.duplicate_level(l)
            bstate = state.find_new_level(l + 1, bisection_args=bisection_args)
            state.replace_level(l + 1, bstate.b.fa)

            Sf = state.entropy()

            if Si - Sf < epsilon:
                if check_verbose(verbose):
                    print(verbose_pad(verbose) + "level", l, ": rejected insert",
                          state.levels[l].B, ", dS:", Sf - Si)

                del state.levels[l + 1]
                for j in range(len(bstates)):
                    state.levels[l + j] = bstates[j]
                if bstates[-1].B == 1:
                    del state.levels[l + len(bstates):]
            else:
                kept = False
                dS += Sf - Si

                l += 1
                done.insert(l, False)

                if check_verbose(verbose):
                    print(verbose_pad(verbose) + "level", l, ": inserted",
                          state.levels[l].B, ", dS:", Sf - Si)

        # create a new level at the top with B=1, if necessary
        if state.levels[-1].B > 1:
            bstate = state.levels[-1]
            bstate = bstate.get_block_state(b=zeros(state.levels[-1].B),
                                            deg_corr=False)
            state.levels.append(bstate)
            if _bm_test():
                state._consistency_check()

        done[l] = True
        if not kept:
            if l + 1 < len(state.levels):
                done[l+1] = False
            if l > 0:
                done[l-1] = False
            l += 1
        else:
            if ((l + 1 < len(state.levels) and not done[l + 1]) or
                (l + 1 == len(state.levels) and state.levels[l].B > 1)):
                l += 1
            else:
                l -= 1

        if l >= len(state.levels):
            l = len(state.levels) - 1

    return dS


def get_hierarchy_tree(state, empty_branches=True):
    r"""Obtain the nested hierarchical levels as a tree.

    This transforms a :class:`~graph_tool.inference.NestedBlockState` instance
    into a single :class:`~graph_tool.Graph` instance containing the hierarchy
    tree.

    Parameters
    ----------
    state : :class:`~graph_tool.inference.NestedBlockState`
       Nested block model state.
    empty_branches : ``bool`` (optional, default: ``True``)
       If ``empty_branches == False``, dangling branches at the upper layers
       will be pruned.

    Returns
    -------

    tree : :class:`~graph_tool.Graph`
       A directed graph, where vertices are blocks, and a directed edge points
       to an upper to a lower level in the hierarchy.
    label : :class:`~graph_tool.PropertyMap`
       A vertex property map containing the block label for each node.
    order : :class:`~graph_tool.PropertyMap`
       A vertex property map containing the relative ordering of each layer
       according to the total degree of the groups at the specific levels.
    """

    bstack = state.get_bstack()

    g = bstack[0]
    b = g.vp["b"]
    bstack = bstack[1:]

    if bstack[-1].num_vertices() > 1:
        bg = Graph(directed=g.is_directed())
        bg.add_vertex()
        e = bg.add_edge(0, 0)
        bg.vp.count = bg.new_vp("int", 1)
        bg.ep.count = bg.new_ep("int", g.ep.count.fa.sum())
        bg.vp.b = bg.new_vp("int", 0)
        bstack.append(bg)

    t = Graph()

    if g.get_vertex_filter()[0] is None:
        t.add_vertex(g.num_vertices())
    else:
        t.add_vertex(g.num_vertices(ignore_filter=True))
        filt = g.get_vertex_filter()
        t.set_vertex_filter(t.own_property(filt[0].copy()),
                            filt[1])
    label = t.vertex_index.copy("int")

    order = t.own_property(g.degree_property_map("total").copy())
    t_vertices = list(t.vertices())

    last_pos = 0
    for l, s in enumerate(bstack):
        pos = t.num_vertices()
        if s.num_vertices() > 1:
            t_vertices.extend(t.add_vertex(s.num_vertices()))
        else:
            t_vertices.append(t.add_vertex(s.num_vertices()))
        label.a[-s.num_vertices():] = arange(s.num_vertices())

        # relative ordering based on total degree
        count = s.ep["count"].copy("double")
        for e in s.edges():
            if e.source() == e.target():
                count[e] /= 2
        vs = []
        pvs = {}
        for vi in range(pos, t.num_vertices()):
            vs.append(t_vertices[vi])
            pvs[vs[-1]] = vi - pos
        vs = sorted(vs, key=lambda v: (s.vertex(pvs[v]).out_degree(count) +
                                       s.vertex(pvs[v]).in_degree(count)))
        for vi, v in enumerate(vs):
            order[v] = vi

        for vi, v in enumerate(g.vertices()):
            w = t_vertices[vi + last_pos]
            if s.num_vertices() == 1:
                u = t_vertices[pos]
            else:
                u = t_vertices[b[v] + pos]
            t.add_edge(u, w)

        last_pos = pos
        g = s
        if g.num_vertices() == 1:
            break
        b = g.vp["b"]

    if not empty_branches:
        vmask = t.new_vertex_property("bool", True)
        t = GraphView(t, vfilt=vmask)
        vmask = t.get_vertex_filter()[0]

        for vi in range(state.g.num_vertices(ignore_filter=True),
                        t.num_vertices()):
            v = t.vertex(t_vertices[vi])
            if v.out_degree() == 0:
                vmask[v] = False

        t.vp.label = label
        t.vp.order = order
        t = Graph(t, prune=True)
        label = t.vp.label
        order = t.vp.order
        del t.vp["label"]
        del t.vp["order"]

    return t, label, order

from . minimize import *

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
import numpy.random
import bisect

from . util import *
from . mcmc import *

def fibo(n):
    phi = (1 + sqrt(5)) / 2
    return int(round(phi ** n / sqrt(5)))

def fibo_n_floor(x):
    phi = (1 + sqrt(5)) / 2
    n = floor(log(x * sqrt(5) + 0.5) / log(phi))
    return int(n)

def get_mid(a, b, random=False):
    if random:
        return a + numpy.random.randint(b - a + 1)
    else:
        n = fibo_n_floor(b - a)
        return b - fibo(n - 1)

def cleanup_cache(b_cache, B_min, B_max):
    best_B = None
    min_dl = numpy.inf
    for Bi in b_cache.keys():
        if b_cache[Bi][0] <= min_dl:
            min_dl = b_cache[Bi][0]
            best_B = Bi

    del_Bs = []

    for Bi in b_cache.keys():
        if (Bi < B_min or Bi > B_max) and Bi != best_B:
            del_Bs.append(Bi)

    for Bi in del_Bs:
        del b_cache[Bi]

def get_ent(state, mcmc_multilevel_args, extra_entropy_args):
    mcmc_equilibrate_args = mcmc_multilevel_args.get("mcmc_equilibrate_args", {})
    mcmc_args = mcmc_equilibrate_args.get("mcmc_args", {})
    entropy_args = mcmc_args.get("entropy_args", {})
    S = state.entropy(**dict(entropy_args, **extra_entropy_args))
    return S

def get_state_dl(B, b_cache, mcmc_multilevel_args={}, extra_entropy_args={},
                 verbose=False):
    if B in b_cache:
        return b_cache[B][0]
    Bs = sorted(b_cache.keys())
    B_prev = Bs[bisect.bisect(Bs, B)]
    state = b_cache[B_prev][1]
    state = mcmc_multilevel(state,
                            **dict(mcmc_multilevel_args,
                                   B=B,
                                   verbose=verbose_push(verbose,
                                                        ("B: %d <- %d    " %
                                                         (B, B_prev)))))
    dl = get_ent(state, mcmc_multilevel_args, extra_entropy_args)
    b_cache[B] = (dl, state)
    return dl

def bisection_minimize(init_states, random_bisection=False,
                       mcmc_multilevel_args={}, extra_entropy_args={},
                       verbose=False):
    r"""Find the best order (number of groups) given an initial set of states by
    performing a one-dimension minimization, using a Fibonacci (or golden
    section) search.

    Parameters
    ----------
    init_states : Any state class (e.g. :class:`~graph_tool.inference.BlockState`)
        List with two or more states that will be used to bracket the search.
    random_bisection : ``bool`` (optional, default: ``False``)
        If ``True``, the bisection will be done randomly in the interval,
        instead of using the golden rule.
    mcmc_multilevel_args : ``dict`` (optional, default: ``{}``)
        Arguments to be passed to :func:`~graph_tool.inference.mcmc_multilevel`.
    extra_entropy_args : ``dict`` (optional, default: ``{}``)
        Extra arguments to be passed to ``state.entropy()``.
    verbose : ``bool`` or ``tuple`` (optional, default: ``False``)
        If ``True``, progress information will be shown. Optionally, this
        accepts arguments of the type ``tuple`` of the form ``(level, prefix)``
        where ``level`` is a positive integer that specifies the level of
        detail, and ``prefix`` is a string that is prepended to the all output
        messages.

    Returns
    -------
    min_state : Any state class (e.g. :class:`~graph_tool.inference.BlockState`)
        State with minimal entropy in the interval.

    Notes
    -----

    This function calls :func:`~graph_tool.inference.mcmc_multilevel` to reduce
    the order of a given state, and uses the value of ``state.entropy(**args)``
    for the minimization, with ``args`` obtained from ``mcmc_multilevel_args``.

    References
    ----------

    .. [golden-section-search] "Golden section search",
       https://en.wikipedia.org/wiki/Golden_section_search
    .. [peixoto-efficient-2014] Tiago P. Peixoto, "Efficient Monte Carlo and
       greedy heuristic for the inference of stochastic block models", Phys.
       Rev. E 89, 012804 (2014), :doi:`10.1103/PhysRevE.89.012804`,
       :arxiv:`1310.4378`
    """

    b_cache = {}
    for state in init_states:
        b_cache[state.B] = (get_ent(state, mcmc_multilevel_args,
                                    extra_entropy_args),
                            state.copy())

    max_B = max(b_cache.keys())
    min_B = min(b_cache.keys())
    mid_B = get_mid(min_B, max_B, random=random_bisection)

    kwargs = dict(b_cache=b_cache,
                  mcmc_multilevel_args=dict(mcmc_multilevel_args,
                                            b_cache=b_cache),
                  extra_entropy_args=extra_entropy_args,
                  verbose=verbose_push(verbose, (" " * 4)))

    # Initial bracketing
    while True:
        f_max = get_state_dl(B=max_B, **kwargs)
        f_mid = get_state_dl(B=mid_B, **kwargs)
        f_min = get_state_dl(B=min_B, **kwargs)

        if check_verbose(verbose):
            print(verbose_pad(verbose) + "Current bracket:",
                  (min_B, mid_B, max_B), (f_min, f_mid, f_max))

        cleanup_cache(b_cache, min_B, max_B)

        if f_mid > f_min or f_mid > f_max:
            if f_min < f_max:
                max_B = mid_B
                mid_B = get_mid(min_B, mid_B, random_bisection)
            else:
                min_B = mid_B
                mid_B = get_mid(mid_B, max_B, random_bisection)
        else:
            break

        if max_B - mid_B <= 1:
            break

    # Fibonacci search
    while True:
        if max_B - mid_B > mid_B - min_B:
            x = get_mid(mid_B, max_B, random_bisection)
        else:
            x = get_mid(min_B, mid_B, random_bisection)

        f_x = get_state_dl(B=x, **kwargs)
        f_mid = get_state_dl(B=mid_B, **kwargs)

        if check_verbose(verbose):
            print(verbose_pad(verbose) + "Current bracket:",
                  (min_B, mid_B, max_B), (get_state_dl(B=min_B, **kwargs), f_mid,
                                          get_state_dl(B=max_B, **kwargs)))
            print(verbose_pad(verbose) + "Bisect at B = %d" % x,
                  "with S = %.16g" % f_x)

        if max_B - mid_B <= 1:
            min_dl = numpy.inf
            best_B = None
            for Bi in b_cache.keys():
                if b_cache[Bi][0] <= min_dl:
                    min_dl = b_cache[Bi][0]
                    best_B = Bi
            if check_verbose(verbose):
                print(verbose_pad(verbose) +
                      "Best result: B = %d, S = %.16g" % (best_B, min_dl))

            return b_cache[best_B][1]

        if f_x < f_mid:
            if max_B - mid_B > mid_B - min_B:
                min_B = mid_B
                mid_B = x
            else:
                max_B = mid_B
                mid_B = x
        else:
            if max_B - mid_B > mid_B - min_B:
                max_B = x
            else:
                min_B = x

        cleanup_cache(b_cache, min_B, max_B)

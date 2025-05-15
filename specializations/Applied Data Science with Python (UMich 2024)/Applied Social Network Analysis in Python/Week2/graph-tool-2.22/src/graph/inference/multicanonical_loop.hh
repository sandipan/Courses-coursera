// graph-tool -- a general graph modification and manipulation thingy
//
// Copyright (C) 2006-2017 Tiago de Paula Peixoto <tiago@skewed.de>
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#ifndef MULTICANONICAL_LOOP_HH
#define MULTICANONICAL_LOOP_HH

#include "config.h"

#include <iostream>
#include <queue>

#include <tuple>

#include "hash_map_wrap.hh"
#include "parallel_rng.hh"

#ifdef USING_OPENMP
#include <omp.h>
#endif
namespace graph_tool
{

template <class MulticanonicalState, class RNG>
auto multicanonical_sweep(MulticanonicalState& state, RNG& rng)
{
    auto& g = state._g;

    auto& vlist = state._vlist;

    double S = state._S;
    size_t nmoves = 0;

    auto& hist = state._hist;
    auto& dens = state._dens;
    int M = hist.size();

    int i = state.get_bin(S);

    if (i < 0 || i >= M)
        throw ValueException("current state lies outside the allowed entropy range");

    for (size_t iter = 0; iter < state._niter; ++iter)
    {
        auto v = vertex(uniform_sample(vlist, rng), g);

        if (state.node_weight(v) == 0)
            continue;

        auto s = state.move_proposal(v, rng);

        std::pair<double, double> dS = state.virtual_move_dS(v, s);

        int j = state.get_bin(S + dS.first);

        bool accept;
        if (j < 0 || j >= M)
        {
            accept = false;
        }
        else
        {
            double a = (dens[i] - dens[j]) + dS.second;
            if (a > 0)
            {
                accept = true;
            }
            else
            {
                typedef std::uniform_real_distribution<> rdist_t;
                double sample = rdist_t()(rng);
                accept = sample < exp(a);
            }
        }

        if (accept)
        {
            state.perform_move(v, s);
            nmoves++;
            S += dS.first;
            i = j;
        }

        hist[i]++;
        dens[i] += state._f;

        state._time += 1./M;
        if (state._refine)
            state._f *= (state._time - 1. / M) / state._time;

        if (i == state._target_bin)
            break;
    }
    return make_pair(S, nmoves);
}

} // graph_tool namespace

#endif //MULTICANONICAL_LOOP_HH

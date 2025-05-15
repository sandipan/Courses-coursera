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

#ifndef MCMC_LOOP_HH
#define MCMC_LOOP_HH

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

template <class RNG>
bool metropolis_accept(double dS, double mP, double beta, RNG& rng)
{
    if (std::isinf(beta))
    {
        return dS < 0;
    }
    else
    {
        double a = -dS * beta + mP;
        if (a > 0)
        {
            return true;
        }
        else
        {
            typedef std::uniform_real_distribution<> rdist_t;
            double sample = rdist_t()(rng);
            return sample < exp(a);
        }
    }
}


template <class MCMCState, class RNG>
auto mcmc_sweep(MCMCState state, RNG& rng)
{
    auto& vlist = state._vlist;
    auto& beta = state._beta;

    double S = 0;
    size_t nmoves = 0;

    for (size_t iter = 0; iter < state._niter; ++iter)
    {
        if (state._sequential)
            std::shuffle(vlist.begin(), vlist.end(), rng);

        for (size_t vi = 0; vi < vlist.size(); ++vi)
        {
            size_t v;
            if (state._sequential)
                v = vlist[vi];
            else
                v = uniform_sample(vlist, rng);

            if (state.node_weight(v) == 0)
                continue;

            auto r = state.node_state(v);
            auto s = state.move_proposal(v, rng);

            if (s == r)
                continue;

            double dS, mP;
            std::tie(dS, mP) = state.virtual_move_dS(v, s);

            if (metropolis_accept(dS, mP, beta, rng))
            {
                state.perform_move(v, s);
                nmoves += state.node_weight(v);
                S += dS;
            }

            if (state._verbose)
                cout << v << ": " << r << " -> " << s << " " << S << endl;
        }
    }
    return make_pair(S, nmoves);
}


template <class MCMCState, class RNG>
auto mcmc_sweep_parallel(MCMCState state, RNG& rng_)
{
    auto& g = state._g;

    vector<std::shared_ptr<RNG>> rngs;
    std::vector<std::pair<size_t, double>> best_move;

    init_rngs(rngs, rng_);
    init_cache(state._E);
    best_move.resize(num_vertices(g));

    auto& vlist = state._vlist;
    auto& beta = state._beta;


    double S = 0;
    size_t nmoves = 0;

    for (size_t iter = 0; iter < state._niter; ++iter)
    {
        parallel_loop(vlist,
                      [&](size_t, auto v)
                      {
                          best_move[v] =
                              std::make_pair(state.node_state(v),
                                             numeric_limits<double>::max());
                      });

        #pragma omp parallel firstprivate(state)
        parallel_loop_no_spawn
            (vlist,
             [&](size_t, auto v)
             {
                 auto& rng = get_rng(rngs, rng_);

                 if (state.node_weight(v) == 0)
                     return;

                 auto r = state.node_state(v);
                 auto s = state.move_proposal(v, rng);

                 if (s == r)
                     return;

                 double dS, mP;
                 std::tie(dS, mP) = state.virtual_move_dS(v, s);

                 if (metropolis_accept(dS, mP, beta, rng))
                 {
                     best_move[v].first = s;
                     best_move[v].second = dS;
                 }

                 if (state._verbose)
                     cout << v << ": " << r << " -> " << s << " " << S << endl;
             });

        for (auto v : vlist)
        {
            auto s = best_move[v].first;
            double dS = best_move[v].second;
            if (dS != numeric_limits<double>::max())
            {
                auto ddS = state.virtual_move_dS(v, s);

                if (get<0>(ddS) > 0 && std::isinf(beta))
                    continue;

                state.perform_move(v, s);
                nmoves++;
                S += get<0>(ddS);
            }
        }
    }
    return make_pair(S, nmoves);
}


} // graph_tool namespace

#endif //MCMC_LOOP_HH

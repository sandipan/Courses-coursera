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

#ifndef MERGE_LOOP_HH
#define MERGE_LOOP_HH

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

template <class MergeState, class RNG>
auto merge_sweep(MergeState state, RNG& rng_)
{
    vector<std::shared_ptr<RNG>> rngs;
    if (state._parallel)
    {
        init_rngs(rngs, rng_);
        init_cache(state._E);
    }

    typedef std::tuple<size_t, size_t, double> merge_t;

    std::vector<merge_t>
        best_merge(*std::max_element(state._available.begin(),
                                     state._available.end()) + 1,
                   make_tuple(size_t(0), size_t(0),
                              numeric_limits<double>::max()));

    #pragma omp parallel firstprivate(state) if (state._parallel)
    parallel_loop_no_spawn
        (state._available,
         [&](size_t, auto v)
         {
             auto& rng = get_rng(rngs, rng_);

             if (state.node_weight(v) == 0)
                 return;

             gt_hash_set<size_t> past_moves;

             auto find_candidates = [&](bool random)
                 {
                     for (size_t iter = 0; iter < state._niter; ++iter)
                     {
                         auto s = state.move_proposal(v, random, rng);
                         if (s == state._null_move)
                             continue;
                         if (past_moves.find(s) != past_moves.end())
                             continue;
                         past_moves.insert(s);
                         double dS = state.virtual_move_dS(v, s);
                         if (dS < get<2>(best_merge[v]))
                             best_merge[v] = make_tuple(v, s, dS);
                     }
                 };

             find_candidates(false);

             // if no candidates were found, the group is likely to be "stuck"
             // (i.e. isolated or constrained by clabel); attempt random
             // movements instead

             if (get<2>(best_merge[v]) == numeric_limits<double>::max())
                 find_candidates(true);
         });

    auto cmp = [](auto& a, auto& b) { return get<2>(a) > get<2>(b); };

    std::priority_queue<merge_t, std::vector<merge_t>, decltype(cmp)>
        queue(cmp);

    std::shuffle(best_merge.begin(), best_merge.end(), rng_);
    for (auto& merge : best_merge)
        queue.push(merge);

    double S = 0;
    size_t nmerges = 0;
    while (nmerges != state._nmerges && !queue.empty())
    {
        auto merge = queue.top();
        queue.pop();

        auto v = state.get_root(get<0>(merge));
        auto s = state.get_root(get<1>(merge));
        double dS = get<2>(merge);
        if (v == s || dS == numeric_limits<double>::max())
            continue;
        double ndS = state.virtual_move_dS(v, s);
        if (!queue.empty() && ndS > get<2>(queue.top()))
        {
            get<2>(merge) = ndS;
            queue.push(merge);
            continue;
        }
        if (state._verbose)
            cout << "merging " << v << " -> " << s << " : "
                 << dS << " " << ndS << endl;
        state.perform_merge(v, s);
        S += ndS;
        nmerges++;
    }

    // collapse merge tree
    state.finalize();

    return make_pair(S, nmerges);
}

} // graph_tool namespace

#endif //MERGE_LOOP_HH

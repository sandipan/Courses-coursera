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

#ifndef SPLIT_MERGE_LOOP_HH
#define SPLIT_MERGE_LOOP_HH

#include "config.h"

#include <iostream>
#include <queue>

#include <tuple>

#include "hash_map_wrap.hh"

#ifdef USING_OPENMP
#include <omp.h>
#endif
namespace graph_tool
{

template <class MergeState, class RNG>
auto bundled_vacate_sweep(MergeState& state, RNG& rng)
{
    if (state._nmerges == 0)
        return make_pair(double(0), size_t(0));

    // individual bundles can move in different directions
    auto get_best_move = [&] (auto& bundle, auto& past_moves)
        {
            std::tuple<size_t, double> best_move(state._null_move,
                                                 numeric_limits<double>::max());

            auto find_candidates = [&](bool random)
            {
                for (size_t iter = 0; iter < state._niter; ++iter)
                {
                    auto s = state.move_proposal(bundle, random, rng);
                    if (s == state._null_move)
                        continue;
                    if (past_moves.find(s) != past_moves.end())
                        continue;
                    past_moves.insert(s);

                    double dS = state.virtual_move_dS(bundle, s);

                    if (dS < get<1>(best_move))
                    {
                        get<0>(best_move) = s;
                        get<1>(best_move) = dS;
                    }
                }
            };

            find_candidates(false);

            // if no candidates were found, the group is likely to be "stuck"
            // (i.e. isolated or constrained by clabel); attempt random
            // movements instead

            if (get<0>(best_move) == state._null_move)
                find_candidates(true);

            return best_move;
        };

    // all bundles move together
    auto get_best_move_coherent = [&] (auto& bundles)
        {
            auto r = state.bundle_state(bundles[0]);

            gt_hash_set<size_t> past_moves;
            std::tuple<size_t, double> best_move(state._null_move,
                                                 numeric_limits<double>::max());

            auto find_candidates = [&](bool random)
            {
                for (size_t iter = 0; iter < state._niter; ++iter)
                {
                    auto s = state.move_proposal(uniform_sample(bundles, rng),
                                                 random, rng);
                    if ( s == state._null_move)
                        continue;
                    if (past_moves.find(s) != past_moves.end())
                        continue;
                    past_moves.insert(s);

                    double dS = 0;
                    for (auto& bundle : bundles)
                    {
                        dS += state.virtual_move_dS(bundle, s);
                        state.perform_move(bundle, s);
                    }

                    for (auto& bundle : bundles)
                        state.perform_move(bundle, r);

                    if (dS < get<1>(best_move))
                    {
                        get<0>(best_move) = s;
                        get<1>(best_move) = dS;
                    }
                }
            };

            find_candidates(false);

            // if no candidates were found, the group is likely to be "stuck"
            // (i.e. isolated or constrained by clabel); attempt random
            // movements instead

            if (get<0>(best_move) == state._null_move)
                find_candidates(true);

            return best_move;
        };

    auto get_best_move_bundles = [&](auto& bundles, auto& forbidden_moves,
                                     auto& bmoves)
        {
            auto r = state.bundle_state(bundles[0]);

            double dS = 0;
            for (auto& bundle : bundles)
            {
                gt_hash_set<size_t> past_moves(forbidden_moves);
                auto best_move = get_best_move(bundle, past_moves);
                if (get<0>(best_move) == state._null_move)
                {
                    bmoves.clear();
                    break;
                }
                bmoves.push_back(get<0>(best_move));

                dS += state.virtual_move_dS(bundle, bmoves.back());
                state.perform_move(bundle, bmoves.back());
            }

            for (auto& bundle : bundles)
                state.perform_move(bundle, r);

            auto best_coherent = get_best_move_coherent(bundles);

            if (get<1>(best_coherent) < dS)
            {
                dS = get<1>(best_coherent);
                for (auto& r : bmoves)
                    r = get<0>(best_coherent);
            }

            return dS;
        };


    std::vector<std::tuple<std::reference_wrapper<std::vector<std::vector<size_t>>>,
                           std::vector<size_t>>> best_moves;
    std::vector<double> best_moves_dS;
    std::vector<size_t> idx;

    for (auto& bundles : state._block_bundles)
    {
        std::vector<size_t> bmoves;
        gt_hash_set<size_t> past_moves;
        double dS = get_best_move_bundles(bundles, past_moves, bmoves);
        if (!bmoves.empty())
        {
            best_moves.emplace_back(std::ref(bundles),
                                    std::move(bmoves));
            best_moves_dS.push_back(dS);
            idx.push_back(idx.size());
        }
    }

    std::shuffle(idx.begin(), idx.end(), rng);

    auto cmp = [&](auto& i, auto& j)
        { return best_moves_dS[i] > best_moves_dS[j]; };

    std::priority_queue<size_t, std::vector<size_t>, decltype(cmp)> queue(cmp);

    for (auto i : idx)
        queue.push(i);

    double S = 0;
    size_t nmerges = 0;
    gt_hash_set<size_t> vacated;
    while (nmerges < state._nmerges && !queue.empty())
    {
        auto pos = queue.top();
        queue.pop();

        auto& bundles = get<0>(best_moves[pos]).get();
        auto& bmoves = get<1>(best_moves[pos]);

        bool redo = false;
        for (auto s : bmoves)
        {
            if (vacated.find(s) != vacated.end())
            {
                redo = true;
                break;
            }
        }

        if (redo)
        {
            bmoves.clear();
            double dS = get_best_move_bundles(bundles, vacated, bmoves);
            if (bmoves.empty())
                continue;
            if (!queue.empty() && best_moves_dS[queue.top()] < dS)
            {
                best_moves_dS[pos] = dS;
                queue.push(pos);
                continue;
            }
        }

        auto r = state.bundle_state(bundles[0]);
        vacated.insert(r);

        for (size_t i = 0; i < bundles.size(); ++i)
        {
            auto& bundle = bundles[i];
            auto s = bmoves[i];
            S += state.virtual_move_dS(bundle, s);
            state.perform_move(bundle, s);
        }

        nmerges++;
    }

    return make_pair(S, nmerges);
}

} // graph_tool namespace

#endif //SPLIT_MERGE_LOOP_HH

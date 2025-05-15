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

#ifndef GRAPH_OVERLAP_BLOCKMODEL_MERGE_HH
#define GRAPH_OVERLAP_BLOCKMODEL_MERGE_HH

#include "config.h"

#include <vector>

#include "graph_tool.hh"
#include "graph_state.hh"
#include "graph_blockmodel_overlap_util.hh"
#include <boost/mpl/vector.hpp>

namespace graph_tool
{
using namespace boost;
using namespace std;

typedef vprop_map_t<int32_t>::type vmap_t;

#define MERGE_OVERLAP_BLOCK_STATE_params(State)                                \
    ((__class__, &, mpl::vector<python::object>, 1))                           \
    ((state, &, State&, 0))                                                    \
    ((E,, size_t, 0))                                                          \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((verbose,, bool, 0))                                                      \
    ((niter,, size_t, 0))                                                      \
    ((nmerges,, size_t, 0))

template <class State>
struct Merge
{
    GEN_STATE_BASE(MergeOverlapBlockStateBase,
                   MERGE_OVERLAP_BLOCK_STATE_params(State))

    template <class... Ts>
    class MergeOverlapBlockState
        : public MergeOverlapBlockStateBase<Ts...>
    {
    public:
        GET_PARAMS_USING(MergeOverlapBlockStateBase<Ts...>,
                         MERGE_OVERLAP_BLOCK_STATE_params(State))
        GET_PARAMS_TYPEDEF(Ts, MERGE_OVERLAP_BLOCK_STATE_params(State))

        template <class... ATs,
                  typename std::enable_if_t<sizeof...(ATs) ==
                                            sizeof...(Ts)>* = nullptr>
        MergeOverlapBlockState(ATs&&... as)
           : MergeOverlapBlockStateBase<Ts...>(as...),
            _g(_state._g),
            _null_move(std::numeric_limits<size_t>::max())
        {
            _state._egroups.clear();

            gt_hash_map<int, gt_hash_map<int, std::vector<size_t>>>
                block_bundles;

            for (auto v : vertices_range(_g))
            {
                auto r = _state._b[v];
                auto& bundles = block_bundles[r];
                for (auto e : all_edges_range(v, _g))
                {
                    auto w = target(e, _g);
                    if (w == v)
                        w = source(e, _g);
                    auto s = _state._b[w];
                    bundles[s].push_back(v);
                }
            }

            for (auto& rb : block_bundles)
            {
                std::vector<std::vector<size_t>> bundle;
                for (auto& sv : rb.second)
                    bundle.push_back(std::move(sv.second));
                _block_bundles.push_back(std::move(bundle));
                _block_list.push_back(rb.first);
            }
        }

        typename state_t::g_t& _g;
        std::vector<std::vector<std::vector<size_t>>> _block_bundles;
        std::vector<size_t> _block_list;
        const size_t _null_move;

        size_t bundle_state(vector<size_t>& bundle)
        {
            return _state._b[bundle[0]];
        }

        template <class RNG>
        size_t move_proposal(vector<size_t>& bundle, bool random, RNG& rng)
        {
            size_t r = bundle_state(bundle);

            size_t s;

            if (random)
            {
                s = uniform_sample(_block_list, rng);
                if (group_size(s) == 0)
                    s = r;
            }
            else
            {
                auto v = uniform_sample(bundle, rng);
                s = _state.sample_block(v, 0, rng);
            }

            if (s == r || _state._bclabel[r] != _state._bclabel[s])
                return _null_move;

            return s;
        }

        double virtual_move_dS(vector<size_t>& bundle, size_t nr)
        {
            size_t r = _state._b[bundle[0]];
            if (r == nr)
                return 0;
            double dS = 0;
            for (auto v : bundle)
            {
                assert(r == size_t(_state._b[v]));
                dS += _state.virtual_move(v, r, nr, _entropy_args);
                _state.move_vertex(v, nr);
            }
            for (auto v : bundle)
                _state.move_vertex(v, r);
            assert(_state._wr[r] > 0);
            return dS;
        }

        void perform_move(vector<size_t>& bundle, size_t nr)
        {
            for (auto v : bundle)
                _state.move_vertex(v, nr);
        }

        size_t group_size(size_t r)
        {
            return _state._wr[r];
        }
    };
};


} // graph_tool namespace

#endif //GRAPH_OVERLAP_BLOCKMODEL_MERGE_HH

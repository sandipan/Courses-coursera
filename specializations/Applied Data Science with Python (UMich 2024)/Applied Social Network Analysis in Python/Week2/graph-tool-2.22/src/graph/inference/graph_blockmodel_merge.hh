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

#ifndef GRAPH_BLOCKMODEL_MERGE_HH
#define GRAPH_BLOCKMODEL_MERGE_HH

#include "config.h"

#include <vector>

#include "graph_tool.hh"
#include "graph_state.hh"
#include "graph_blockmodel_util.hh"
#include <boost/mpl/vector.hpp>

namespace graph_tool
{
using namespace boost;
using namespace std;

typedef vprop_map_t<int32_t>::type vmap_t;

#define MERGE_BLOCK_STATE_params(State)                                        \
    ((__class__, &, mpl::vector<python::object>, 1))                           \
    ((state, &, State&, 0))                                                    \
    ((E,, size_t, 0))                                                          \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((parallel,, bool, 0))                                                     \
    ((verbose,, bool, 0))                                                      \
    ((niter,, size_t, 0))                                                      \
    ((nmerges,, size_t, 0))

template <class State>
struct Merge
{
    GEN_STATE_BASE(MergeBlockStateBase, MERGE_BLOCK_STATE_params(State))

    template <class... Ts>
    class MergeBlockState
        : public MergeBlockStateBase<Ts...>
    {
    public:
        GET_PARAMS_USING(MergeBlockStateBase<Ts...>,
                         MERGE_BLOCK_STATE_params(State))
        GET_PARAMS_TYPEDEF(Ts, MERGE_BLOCK_STATE_params(State))

        template <class... ATs,
                  typename std::enable_if_t<sizeof...(ATs) ==
                                            sizeof...(Ts)>* = nullptr>
        MergeBlockState(ATs&&... as)
           : MergeBlockStateBase<Ts...>(as...),
            _g(_state._g),
            _m_entries(num_vertices(_state._bg)),
            _null_move(numeric_limits<size_t>::max())
        {
            _state._egroups.clear();

            if (_entropy_args.partition_dl || _entropy_args.degree_dl ||
                _entropy_args.edges_dl)
                _state.enable_partition_stats();
            else
                _state.disable_partition_stats();

            for (auto v : vertices_range(_state._g))
            {
                if (_state._vweight[v] > 0)
                    _available.push_back(v);
            }
        }

        typename state_t::g_t& _g;
        typename state_t::m_entries_t _m_entries;
        const size_t _null_move;
        vector<size_t> _available;

        size_t node_state(size_t v)
        {
            return _state._b[v];
        }

        size_t node_weight(size_t v)
        {
            return _state.node_weight(v);
        }

        template <class RNG>
        size_t move_proposal(size_t v, bool random, RNG& rng)
        {
            size_t r = _state._b[v];
            assert(r == v);
            size_t s;
            if (!random)
            {
                size_t t = _state.random_neighbour(v, rng);
                s = _state.random_neighbour(t, rng);
            }
            else
            {
                s = uniform_sample(_available, rng);
            }

            if (s == r || !_state.allow_move(r, s, false))
                return _null_move;

            return s;
        }

        double virtual_move_dS(size_t v, size_t nr)
        {
            return _state.virtual_move(v, _state._b[v], nr, _entropy_args,
                                       _m_entries);
        }

        void perform_merge(size_t r, size_t s)
        {
            assert(_state._bclabel[r] == _state._bclabel[s]);
            assert(_state._ignore_degrees[r] == _state._ignore_degrees[s]);
            _state.move_vertex(r, s);
            _state.merge_vertices(r, s);
        }

        size_t get_root(size_t s)
        {
            int r = s;
            while (_state._merge_map[r] != r)
                r = _state._merge_map[r];
            _state._merge_map[s] = r;
            return r;
        };

        bool is_empty_vertex(size_t r)
        {
            return _state._vweight[r] == 0;
        }

        void finalize()
        {
            for (auto v : vertices_range(_state._g))
                get_root(v);
        }
    };
};


} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_MERGE_HH

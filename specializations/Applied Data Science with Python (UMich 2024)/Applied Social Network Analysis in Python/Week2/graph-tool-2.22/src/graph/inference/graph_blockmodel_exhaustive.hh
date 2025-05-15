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

#ifndef GRAPH_BLOCKMODEL_EXHAUSTIVE_HH
#define GRAPH_BLOCKMODEL_EXHAUSTIVE_HH

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

typedef typename vprop_map_t<int32_t>::type vmap_t;

#define EXHAUSTIVE_BLOCK_STATE_params(State)                                   \
    ((__class__,&, mpl::vector<python::object>, 1))                            \
    ((state, &, State&, 0))                                                    \
    ((S, , double, 0))                                                         \
    ((vlist,&, std::vector<size_t>&, 0))                                       \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((b_min,, vmap_t, 0))                                                      \
    ((max_iter,, size_t, 0))


template <class State>
struct Exhaustive
{
    GEN_STATE_BASE(ExhaustiveBlockStateBase,
                   EXHAUSTIVE_BLOCK_STATE_params(State))

    template <class... Ts>
    class ExhaustiveBlockState
        : public ExhaustiveBlockStateBase<Ts...>
    {
    public:
        GET_PARAMS_USING(ExhaustiveBlockStateBase<Ts...>,
                         EXHAUSTIVE_BLOCK_STATE_params(State))
        GET_PARAMS_TYPEDEF(Ts, EXHAUSTIVE_BLOCK_STATE_params(State))

        template <class... ATs,
                  typename std::enable_if_t<sizeof...(ATs) ==
                                            sizeof...(Ts)>* = nullptr>
        ExhaustiveBlockState(ATs&&... as)
          : ExhaustiveBlockStateBase<Ts...>(as...),
            _g(_state._g), _S_min(_S)
        {
            _state.init_mcmc(numeric_limits<double>::infinity(),
                             (_entropy_args.partition_dl ||
                              _entropy_args.degree_dl ||
                              _entropy_args.edges_dl));
        }
        typename State::g_t& _g;
        double _S_min;

        size_t get_B()
        {
            return num_vertices(_state._bg);
        }

        size_t node_state(size_t v)
        {
            return _state._b[v];
        }

        double virtual_move_dS(size_t v, size_t nr)
        {
            return _state.virtual_move(v, _state._b[v], nr, _entropy_args);
        }

        void perform_move(size_t v, size_t nr)
        {
            _state.move_vertex(v, nr);
        }
    };
};


} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_EXHAUSTIVE_HH

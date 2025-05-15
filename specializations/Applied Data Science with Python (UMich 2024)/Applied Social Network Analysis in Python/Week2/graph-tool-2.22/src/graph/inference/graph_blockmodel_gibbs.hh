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

#ifndef GRAPH_BLOCKMODEL_GIBBS_HH
#define GRAPH_BLOCKMODEL_GIBBS_HH

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

#define GIBBS_BLOCK_STATE_params(State)                                        \
    ((__class__,&, mpl::vector<python::object>, 1))                            \
    ((state, &, State&, 0))                                                    \
    ((E,, size_t, 0))                                                          \
    ((vlist,&, std::vector<size_t>&, 0))                                       \
    ((beta,, double, 0))                                                       \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((allow_vacate,, bool, 0))                                                 \
    ((parallel,, bool, 0))                                                     \
    ((sequential,, bool, 0))                                                   \
    ((verbose,, bool, 0))                                                      \
    ((niter,, size_t, 0))


template <class State>
struct Gibbs
{
    GEN_STATE_BASE(GibbsBlockStateBase, GIBBS_BLOCK_STATE_params(State))

    template <class... Ts>
    class GibbsBlockState
        : public GibbsBlockStateBase<Ts...>
    {
    public:
        GET_PARAMS_USING(GibbsBlockStateBase<Ts...>,
                         GIBBS_BLOCK_STATE_params(State))
        GET_PARAMS_TYPEDEF(Ts, GIBBS_BLOCK_STATE_params(State))

        template <class... ATs,
                  typename std::enable_if_t<sizeof...(ATs) ==
                                            sizeof...(Ts)>* = nullptr>
        GibbsBlockState(ATs&&... as)
           : GibbsBlockStateBase<Ts...>(as...),
            _g(_state._g),
            _m_entries(num_vertices(_state._bg))
        {
            _state.init_mcmc(numeric_limits<double>::infinity(),
                             (_entropy_args.partition_dl ||
                              _entropy_args.degree_dl ||
                              _entropy_args.edges_dl));
        }

        typename state_t::g_t& _g;
        typename state_t::m_entries_t _m_entries;

        auto& get_moves(size_t) { return _state._candidate_blocks; }

        size_t node_state(size_t v)
        {
            return _state._b[v];
        }

        size_t node_weight(size_t v)
        {
            return _state.node_weight(v);
        }

        double virtual_move_dS(size_t v, size_t nr)
        {
            if (nr == null_group)
            {
                if (_state._empty_blocks.empty())
                    return numeric_limits<double>::infinity();
                else
                    nr = _state._empty_blocks.front();
            }
            size_t r = _state._b[v];
            if (!_state.allow_move(r, nr))
                return numeric_limits<double>::infinity();
            return _state.virtual_move(v, r, nr, _entropy_args, _m_entries);
        }

        template <class RNG>
        void perform_move(size_t v, size_t nr, RNG& rng)
        {
            size_t r = _state._b[v];

            if (nr == null_group)
                nr = uniform_sample(_state._empty_blocks, rng);

            if (r == nr)
                return;

            _state.move_vertex(v, nr);
        }
    };
};


} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_GIBBS_HH

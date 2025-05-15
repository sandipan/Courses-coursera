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

#ifndef GRAPH_BLOCKMODEL_MCMC_HH
#define GRAPH_BLOCKMODEL_MCMC_HH

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

#define MCMC_BLOCK_STATE_params(State)                                         \
    ((__class__,&, mpl::vector<python::object>, 1))                            \
    ((state, &, State&, 0))                                                    \
    ((E,, size_t, 0))                                                          \
    ((vlist,&, std::vector<size_t>&, 0))                                       \
    ((beta,, double, 0))                                                       \
    ((c,, double, 0))                                                          \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((allow_vacate,, bool, 0))                                                 \
    ((parallel,, bool, 0))                                                     \
    ((sequential,, bool, 0))                                                   \
    ((verbose,, bool, 0))                                                      \
    ((niter,, size_t, 0))


template <class State>
struct MCMC
{
    GEN_STATE_BASE(MCMCBlockStateBase, MCMC_BLOCK_STATE_params(State))

    template <class... Ts>
    class MCMCBlockState
        : public MCMCBlockStateBase<Ts...>
    {
    public:
        GET_PARAMS_USING(MCMCBlockStateBase<Ts...>,
                         MCMC_BLOCK_STATE_params(State))
        GET_PARAMS_TYPEDEF(Ts, MCMC_BLOCK_STATE_params(State))

        template <class... ATs,
                  typename std::enable_if_t<sizeof...(ATs) ==
                                            sizeof...(Ts)>* = nullptr>
        MCMCBlockState(ATs&&... as)
           : MCMCBlockStateBase<Ts...>(as...),
            _g(_state._g),
            _m_entries(num_vertices(_state._bg))
        {
            _state.init_mcmc(_c,
                             (_entropy_args.partition_dl ||
                              _entropy_args.degree_dl ||
                              _entropy_args.edges_dl));
        }

        typename state_t::g_t& _g;
        typename state_t::m_entries_t _m_entries;

        size_t node_state(size_t v)
        {
            return _state._b[v];
        }

        size_t node_weight(size_t v)
        {
            return _state.node_weight(v);
        }

        template <class RNG>
        size_t move_proposal(size_t v, RNG& rng)
        {
            auto r = _state._b[v];

            if (!_allow_vacate && _state.is_last(v))
                return r;

            size_t s = _state.sample_block(v, _c, rng);

            if (!_state.allow_move(r, s))
                return r;

            return s;
        }

        std::tuple<double, double>
        virtual_move_dS(size_t v, size_t nr)
        {
            size_t r = _state._b[v];
            double dS = _state.virtual_move(v, r, nr, _entropy_args,
                                            _m_entries);
            double a = 0;
            if (!std::isinf(_c) && !std::isinf(_beta))
            {
                double pf = _state.get_move_prob(v, r, nr, _c, false,
                                                 _m_entries);
                double pb = _state.get_move_prob(v, nr, r, _c, true,
                                                 _m_entries);
                a = log(pb) - log(pf);
            }
            return std::make_tuple(dS, a);
        }

        void perform_move(size_t v, size_t nr)
        {
            _state.move_vertex(v, nr);
        }
    };
};


} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_MCMC_HH

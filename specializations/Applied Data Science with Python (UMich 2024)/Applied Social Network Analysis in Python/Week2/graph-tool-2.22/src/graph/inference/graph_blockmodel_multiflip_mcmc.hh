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

#ifndef GRAPH_BLOCKMODEL_MULTIFLIP_MCMC_HH
#define GRAPH_BLOCKMODEL_MULTIFLIP_MCMC_HH

#include "config.h"

#include <vector>
#include <algorithm>

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
    ((beta,, double, 0))                                                       \
    ((c,, double, 0))                                                          \
    ((a,, double, 0))                                                          \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((mproposals, & ,std::vector<size_t>&, 0))                                 \
    ((maccept, & ,std::vector<size_t>&, 0))                                    \
    ((allow_vacate,, bool, 0))                                                 \
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
            _groups(num_vertices(_state._bg)),
            _vpos(get(vertex_index_t(), _state._g),
                  num_vertices(_state._g)),
            _mprobs(num_vertices(_state._g) + 1),
            _sequential(false)
        {
            _state.init_mcmc(_c,
                             (_entropy_args.partition_dl ||
                              _entropy_args.degree_dl ||
                              _entropy_args.edges_dl));
            for (auto v : vertices_range(_state._g))
            {
                if (_state._vweight[v] > 0)
                    add_element(_groups[_state._b[v]], _vpos, v);
            }
            for (auto r : vertices_range(_state._bg))
                _vlist.push_back(r);
            for (size_t m = 1; m < _mprobs.size(); ++m)
                _mprobs[m] = _mprobs[m-1] + std::pow(m, -_a);
        }

        typename state_t::g_t& _g;

        std::vector<std::vector<size_t>> _groups;
        typename vprop_map_t<size_t>::type::unchecked_t _vpos;

        std::vector<size_t> _vlist;
        std::vector<size_t> _vs;
        std::vector<double> _mprobs;

        bool _sequential;

        size_t node_state(size_t r)
        {
            return r;
        }

        size_t node_weight(size_t r)
        {
            return _groups[r].size();
        }

        template <class RNG>
        size_t sample_m(size_t n, RNG& rng)
        {
            double M = _mprobs[n];
            std::uniform_real_distribution<> u_sample(0, M);
            auto u = u_sample(rng);
            auto iter = std::lower_bound(_mprobs.begin(),
                                         _mprobs.begin() + n + 1, u);
            return iter - _mprobs.begin();
        }

        double log_pm(size_t m, size_t n)
        {
            return - _a * log(m) - log(_mprobs[n]);
        }

        template <class RNG>
        size_t move_proposal(size_t r, RNG& rng)
        {
            if (!_allow_vacate && _groups[r].size() == 1)
                return r;

            size_t m = sample_m(_groups[r].size(), rng);

            assert(m <= _groups[r].size());

            _vs.clear();

            while (_vs.size() < m)
            {
                size_t v = uniform_sample(_groups[r], rng);
                _vs.push_back(v);
                remove_element(_groups[r], _vpos, v);
            }

            for (auto v : _vs)
                add_element(_groups[r], _vpos, v);

            size_t v = uniform_sample(_vs, rng);
            size_t s = _state.sample_block(v, _c, rng);

            if (!_state.allow_move(r, s))
                return r;

            if (_groups[s].size() == 0)
                _state._bclabel[s] = _state._bclabel[r];

            _mproposals[m]++;
            return s;
        }

        std::tuple<double, double>
        virtual_move_dS(size_t r, size_t nr)
        {
            double dS = 0, a = 0;
            size_t m = _vs.size();

            a -= log_pm(m, _groups[r].size());
            a += log_pm(m, _groups[nr].size() + m);
            a -= -lbinom(_groups[r].size(), m);
            a += -lbinom(_groups[nr].size() + m, m);

            if (m == 1)
            {
                auto v = _vs.front();
                dS = _state.virtual_move(v, r, nr, _entropy_args);
                if (!std::isinf(_c))
                {
                    double pf = _state.get_move_prob(v, r, nr, _c, false);
                    double pb = _state.get_move_prob(v, nr, r, _c, true);
                    a += log(pb) - log(pf);
                }
            }
            else
            {
                _state._egroups_enabled = false;
                double pf = 0, pb = 0;
                if (!std::isinf(_c))
                {
                    for (auto v : _vs)
                        pf += _state.get_move_prob(v, r, nr, _c, false);
                    pf /= m;
                }
                for (auto v : _vs)
                {
                    dS += _state.virtual_move(v, r, nr, _entropy_args);
                    _state.move_vertex(v, nr);
                }
                if (!std::isinf(_c))
                {
                    for (auto v : _vs)
                        pb += _state.get_move_prob(v, nr, r, _c, false);
                    pb /= m;
                    a += log(pb) - log(pf);
                }
                for (auto v : _vs)
                    _state.move_vertex(v, r);
                _state._egroups_enabled = true;
            }
            return std::make_tuple(dS, a);
        }

        void perform_move(size_t r, size_t nr)
        {
            for (auto v : _vs)
            {
                _state.move_vertex(v, nr);
                remove_element(_groups[r], _vpos, v);
                add_element(_groups[nr], _vpos, v);
            }
            _maccept[_vs.size()]++;
        }
    };
};


} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_MCMC_HH

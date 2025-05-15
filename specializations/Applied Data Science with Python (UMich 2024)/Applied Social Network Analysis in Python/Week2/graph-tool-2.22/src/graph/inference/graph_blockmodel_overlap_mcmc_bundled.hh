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

#ifndef GRAPH_BLOCKMODEL_OVERLAP_MCMC_BUNDLED_HH
#define GRAPH_BLOCKMODEL_OVERLAP_MCMC_BUNDLED_HH

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

#define BUNDLED_MCMC_OVERLAP_BLOCK_STATE_params(State)                         \
    ((__class__,&, mpl::vector<python::object>, 1))                            \
    ((state, &, State&, 0))                                                    \
    ((E,, size_t, 0))                                                          \
    ((vlist,, std::vector<size_t>, 0))                                         \
    ((beta,, double, 0))                                                       \
    ((c,, double, 0))                                                          \
    ((entropy_args,, entropy_args_t, 0))                                       \
    ((allow_vacate,, bool, 0))                                                 \
    ((sequential,, bool, 0))                                                   \
    ((verbose,, bool, 0))                                                      \
    ((niter,, size_t, 0))


template <class State>
struct MCMC
{
    GEN_STATE_BASE(BundledMCMCOverlapBlockStateBase,
                   BUNDLED_MCMC_OVERLAP_BLOCK_STATE_params(State))

    template <class... Ts>
    class BundledMCMCOverlapBlockState
        : public BundledMCMCOverlapBlockStateBase<Ts...>
    {
    public:
        GET_PARAMS_USING(BundledMCMCOverlapBlockStateBase<Ts...>,
                         BUNDLED_MCMC_OVERLAP_BLOCK_STATE_params(State))
        GET_PARAMS_TYPEDEF(Ts, BUNDLED_MCMC_OVERLAP_BLOCK_STATE_params(State))

        template <class... ATs,
                  typename std::enable_if_t<sizeof...(ATs) ==
                                            sizeof...(Ts)>* = nullptr>
        BundledMCMCOverlapBlockState(ATs&&... as)
           : BundledMCMCOverlapBlockStateBase<Ts...>(as...),
             _g(_state._g),
             _parallel(false)
        {
            _state.init_mcmc(_c,
                             (_entropy_args.partition_dl ||
                              _entropy_args.degree_dl ||
                              _entropy_args.edges_dl));

            for (auto v : _vlist)
            {
                auto i = _state._overlap_stats.get_node(v);
                if (i >= _half_edges.size())
                    _half_edges.resize(i + 1);
                _half_edges[i].push_back(v);
            }

            for (auto& he : _half_edges)
            {
                gt_hash_map<int, vector<size_t>> bundle;
                for (auto v : he)
                    bundle[_state._b[v]].push_back(v);
                for (auto& kv : bundle)
                {
                    _bundles.emplace_back();
                    _bundles.back().swap(kv.second);
                }
            }

            _vlist.clear();
            std::generate_n(std::back_inserter(_vlist), _bundles.size(),
                            [&](){ return _vlist.size(); });
        }

        typename state_t::g_t& _g;
        std::vector<std::vector<size_t>> _half_edges;
        std::vector<std::vector<size_t>> _bundles;
        bool _parallel;

        size_t node_state(size_t i)
        {
            auto v = _bundles[i][0];
            return _state._b[v];
        }

        size_t node_weight(size_t v)
        {
            return _state.node_weight(v);
        }

        template <class RNG>
        size_t move_proposal(size_t i, RNG& rng)
        {
            auto v = _bundles[i][0];
            auto r = _state._b[v];

            size_t s = _state.sample_block(v, _c, rng);

            if (_state._bclabel[s] != _state._bclabel[r])
                return r;

            return s;
        }

        std::tuple<double, double>
        virtual_move_dS(size_t i, size_t nr)
        {
            double dS = 0;

            auto r = _state._b[_bundles[i][0]];

            for (auto v : _bundles[i])
            {
                assert(_state._b[v] == r);
                dS += _state.virtual_move(v, r, nr, _entropy_args);
                _state.move_vertex(v, nr);
            }

            if (!_allow_vacate || _state._wr[r] == 0)
                dS = numeric_limits<double>::infinity();

            double a = 0;
            // TODO: bundled moves are not ergodic, so we give up on detailed
            // balance too. However, this can be improved.

            // if (!std::isinf(_c))
            // {
            //     size_t r = _state._b[v];
            //     double pf = _state.get_move_prob(v, r, nr, _c, false); // forward
            //     double pb = _state.get_move_prob(v, nr, r, _c, true);  // backward
            //     a = log(pb) - log(pf);
            // }

            for (auto v : _bundles[i])
                _state.move_vertex(v, r);

            return std::make_tuple(dS, a);
        }

        void perform_move(size_t i, size_t nr)
        {
            for (auto v : _bundles[i])
                _state.move_vertex(v, nr);
        }
    };
};

} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_OVERLAP_MCMC_BUNDLED_HH

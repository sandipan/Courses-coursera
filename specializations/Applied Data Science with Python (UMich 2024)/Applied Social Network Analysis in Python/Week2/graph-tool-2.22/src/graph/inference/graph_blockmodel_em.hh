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

#ifndef GRAPH_BLOCKMODEL_EM_HH
#define GRAPH_BLOCKMODEL_EM_HH

#include "config.h"

#include <vector>

#include "graph_state.hh"

namespace graph_tool
{
using namespace boost;
using namespace std;

typedef vprop_map_t<int32_t>::type vmap_t;
typedef vprop_map_t<double>::type vrmap_t;
typedef vprop_map_t<vector<double>>::type vvmap_t;
typedef eprop_map_t<vector<double>>::type vemap_t;
typedef eprop_map_t<double>::type edmap_t;

typedef multi_array_ref<double, 2> mat_t;
typedef multi_array_ref<double, 1> vec_t;

#define EM_BLOCK_STATE_params                                                  \
    ((g, &, all_graph_views, 1))                                               \
    ((prs,, mat_t, 0))                                                         \
    ((wr,, vec_t, 0))                                                          \
    ((em_s,, vemap_t, 0))                                                      \
    ((em_t,, vemap_t, 0))                                                      \
    ((vm,, vvmap_t, 0))                                                        \
    ((Z,, edmap_t, 0))                                                         \
    ((max_E,, size_t, 0))

GEN_STATE_BASE(EMBlockStateBase, EM_BLOCK_STATE_params)

template <class... Ts>
class EMBlockState
    : public EMBlockStateBase<Ts...>
{
public:
    GET_PARAMS_USING(EMBlockStateBase<Ts...>, EM_BLOCK_STATE_params)
    GET_PARAMS_TYPEDEF(Ts, EM_BLOCK_STATE_params)

    template <class RNG, class... ATs,
              typename std::enable_if_t<sizeof...(ATs) == sizeof...(Ts)>* = nullptr>
    EMBlockState(RNG& rng, ATs&&... args)
      : EMBlockStateBase<Ts...>(std::forward<ATs>(args)...)
    {
        _B = _prs.shape()[0];
        _N = HardNumVertices()(_g);

        std::uniform_int_distribution<size_t> rand(0, _B - 1);

        for (auto v : vertices_range(_g))
        {
            _vm[v].resize(_B, 1e-3);
            auto r = rand(rng);
            _vm[v][r] = 1;
            normalize(_vm[v]);
        }

        for (auto e : edges_range(_g))
        {
            auto u = source(e, _g);
            auto v = target(e, _g);
            if (u > v)
                std::swap(u, v);
            _em_s[e] = _vm[u];
            _em_t[e] = _vm[v];
        }
    }

    size_t _B;
    size_t _N;

    template <class Edge>
    vector<double>& get_m(size_t u, size_t v, const Edge& e)
    {
        if (u < v)
            return _em_s[e];
        else
            return _em_t[e];
    }

    double learn_iter()
    {
        double delta = 0;

        for (size_t r = 0; r < _B; ++r)
        {
            double& wr_r = _wr[r];
            double old_wr = wr_r;
            wr_r = 0;
            for (auto v : vertices_range(_g))
                wr_r += _vm[v][r];
            wr_r /= num_vertices(_g);
            delta += abs(old_wr - wr_r);
        }

        for (auto e : edges_range(_g))
        {
            auto u = source(e, _g);
            auto v = target(e, _g);
            double& Z_e = _Z[e];
            Z_e = 0;
            for (size_t r = 0; r < _B; ++r)
            {
                for (size_t s = r + 1; s < _B; ++s)
                {
                    Z_e += _prs[r][s] * ((get_m(u, v, e)[r] * get_m(v, u, e)[s]) +
                                         (get_m(u, v, e)[s] * get_m(v, u, e)[r]));
                }
                Z_e += _prs[r][r] * (get_m(u, v, e)[r] * get_m(v, u, e)[r]);
            }
        }

        for (size_t r = 0; r < _B; ++r)
        {
            for (size_t s = r; s < _B; ++s)
            {
                double& x = _prs[r][s];
                double p = x;
                x = 0;
                for (auto e : edges_range(_g))
                {
                    if (_Z[e] == 0)
                        continue;
                    auto u = source(e, _g);
                    auto v = target(e, _g);
                    x += p * (((get_m(u, v, e)[r] * get_m(v, u, e)[s]) +
                               (get_m(u, v, e)[s] * get_m(v, u, e)[r]))) / _Z[e];
                }
                if (x > 0)
                    x /= (_wr[r] * _wr[s] * num_vertices(_g));
                _prs[s][r] = x;
                delta += abs(x - p);
            }
        }
        return delta;
    }


    template <class Vec>
    void normalize(Vec& vec)
    {
        auto max_x = *std::max_element(vec.begin(), vec.end());
        std::for_each(vec.begin(), vec.end(),
                      [&](auto& x){ x = (std::isinf(x)) ? 1. : x / max_x; });
        auto S = std::accumulate(vec.begin(), vec.end(), 0.);
        std::for_each(vec.begin(), vec.end(),
                      [&](auto& x){ x /= S; });
    };

    double bp_iter(size_t max_iter, double epsilon,
                   bool verbose, rng_t& rng)
    {
        typedef typename graph_traits<g_t>::edge_descriptor edge_t;
        vector<pair<edge_t, bool>> messages;
        for (auto e : edges_range(_g))
        {
            messages.emplace_back(e, true);
            messages.emplace_back(e, false);
        }

        vector<double> h(_B), h_temp(_B);
        for (auto v : vertices_range(_g))
        {
            for (size_t r = 0; r < _B; ++r)
                for (size_t s = 0; s < _B; ++s)
                    h[r] += _vm[v][s] * _prs[s][r] / _N;
        }

        size_t niter = 0;
        double delta = epsilon + 1;
        while (delta > epsilon)
        {
            delta = 0;
            std::shuffle(messages.begin(), messages.end(), rng);
            vector<double> temp(_B);
            for (auto& ei : messages)
            {
                auto& e = ei.first;
                auto u = source(e, _g);
                auto v = target(e, _g);
                if (ei.second)
                    std::swap(u, v);
                for (size_t r = 0; r < _B; ++r)
                {
                    double phi_r = 0;
                    for (auto eo : out_edges_range(u, _g))
                    {
                        auto k = target(eo, _g);
                        if (k == v)
                            continue;
                        double T = 0;
                        const auto& m = get_m(k, u, eo);
                        for (size_t s = 0; s < _B; ++s)
                            T += _prs[s][r] * m[s];
                        phi_r += log(T);
                    }
                    phi_r = exp(phi_r - h[r]) * _wr[r];
                    temp[r] = phi_r;
                }

                normalize(temp);

                auto& phi = get_m(u, v, e);
                for (size_t r = 0; r < _B; ++r)
                {
                    delta += abs(temp[r] - phi[r]);
                    phi[r] = temp[r];
                }

                auto& vm_u = _vm[u];
                for (size_t r = 0; r < _B; ++r)
                {
                    h_temp[r] = h[r];
                    for (size_t s = 0; s < _B; ++s)
                        h_temp[r] -= vm_u[s] * _prs[s][r] / _N;
                }

                for (size_t r = 0; r < _B; ++r)
                {
                    double& vm_u_r = vm_u[r];
                    vm_u_r = 0;
                    for (auto eo : out_edges_range(u, _g))
                    {
                        auto k = target(eo, _g);
                        double T = 0;
                        auto& m = get_m(k, u, eo);
                        for (size_t s = 0; s < _B; ++s)
                            T += _prs[s][r] * m[s];
                        vm_u_r += log(T);
                    }
                    vm_u_r = exp(vm_u_r - h[r]) * _wr[r];
                }

                normalize(vm_u);

                for (size_t r = 0; r < _B; ++r)
                {
                    for (size_t s = 0; s < _B; ++s)
                        h_temp[r] += (vm_u[s] * _prs[s][r]) / _N;
                    h[r] = h_temp[r];
                }

            }
            niter++;
            if (verbose)
                cout << niter << " " << delta << endl;
            if (max_iter > 0 && niter > max_iter)
                break;
        }
        return delta;
    }

    double bethe_fe()
    {
        double F = 0;
        vector<double> h(_B);
        for (auto v : vertices_range(_g))
        {
            for (size_t r = 0; r < _B; ++r)
                for (size_t s = 0; s < _B; ++s)
                    h[r] += _vm[v][s] * _prs[s][r] / _N;
        }

        for (auto u : vertices_range(_g))
        {
            double Z_v = 0;
            for (size_t r = 0; r < _B; ++r)
            {
                double vm_u_r = 0;
                for (auto eo : out_edges_range(u, _g))
                {
                    auto k = target(eo, _g);
                    double T = 0;
                    auto& m = get_m(k, u, eo);
                    for (size_t s = 0; s < _B; ++s)
                        T += _prs[s][r] * m[s];
                    vm_u_r += log(T);
                }
                vm_u_r = exp(vm_u_r - h[r]) * _wr[r];
                Z_v += vm_u_r;
            }
            F -= log(Z_v) / _N;
        }

        for (auto e : edges_range(_g))
        {
            auto u = source(e, _g);
            auto v = target(e, _g);
            double Z_e = 0;
            for (size_t r = 0; r < _B; ++r)
            {
                for (size_t s = r + 1; s < _B; ++s)
                {
                    Z_e += _prs[r][s] * ((get_m(u, v, e)[r] * get_m(v, u, e)[s]) +
                                         (get_m(u, v, e)[s] * get_m(v, u, e)[r]));
                }
                Z_e += _prs[r][r] * (get_m(u, v, e)[r] * get_m(v, u, e)[r]);
            }
            F += log(Z_e) / _N;
        }

        double c = 0;
        for (size_t r = 0; r < _B; ++r)
            for (size_t s = 0; s < _B; ++s)
                c += _prs[r][s] * _wr[r] * _wr[s] / 2;
        F -= c;

        return F;
    }


    template <class VMap>
    void get_MAP(VMap&& vmap)
    {
        for (auto v : vertices_range(_g))
        {
            auto& p = _vm[v];
            vmap[v] = int(std::max_element(p.begin(), p.end()) - p.begin());
        }
    }

    void get_MAP_any(boost::any avmap)
    {
        vmap_t vmap = boost::any_cast<vmap_t>(avmap);
        get_MAP(vmap.get_unchecked());
    }

};

} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_EM_HH

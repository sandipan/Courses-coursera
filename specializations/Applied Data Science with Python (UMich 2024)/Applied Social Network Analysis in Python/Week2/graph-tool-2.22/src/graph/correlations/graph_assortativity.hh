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

#ifndef GRAPH_ASSORTATIVITY_HH
#define GRAPH_ASSORTATIVITY_HH

#include "shared_map.hh"
#include "graph_util.hh"
#include "hash_map_wrap.hh"

namespace graph_tool
{
using namespace std;
using namespace boost;


// this will calculate the assortativity coefficient, based on the property
// pointed by 'deg'

struct get_assortativity_coefficient
{
    template <class Graph, class DegreeSelector>
    void operator()(const Graph& g, DegreeSelector deg, double& r,
                    double& r_err) const
    {
        size_t n_edges = 0;
        size_t e_kk = 0;

        typedef typename DegreeSelector::value_type val_t;
        typedef gt_hash_map<val_t, size_t> map_t;
        map_t a, b;

        SharedMap<map_t> sa(a), sb(b);
        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            firstprivate(sa, sb) reduction(+:e_kk, n_edges)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 val_t k1 = deg(v, g);
                 for (auto w : out_neighbours_range(v, g))
                 {
                     val_t k2 = deg(w, g);
                     if (k1 == k2)
                         e_kk++;
                     sa[k1]++;
                     sb[k2]++;
                     n_edges++;
                 }
             });

        sa.Gather();
        sb.Gather();

        double t1 = double(e_kk) / n_edges, t2 = 0.0;

        for (auto& ai : a)
        {
            auto bi = b.find(ai.first);
            if (bi != b.end())
                t2 += ai.second * bi->second;
        }
        t2 /= n_edges * n_edges;

        r = (t1 - t2)/(1.0 - t2);

        // "jackknife" variance
        double err = 0;
        size_t one = (is_directed::apply<Graph>::type::value) ? 1 : 2;
        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            reduction(+:err)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 val_t k1 = deg(v, g);
                 for (auto w : out_neighbours_range(v, g))
                 {
                     val_t k2 = deg(w, g);
                     double tl2 = (t2 * (n_edges * n_edges)
                                   - one * b[k1] - one * a[k2]) /
                         ((n_edges - one) * (n_edges - one));
                     double tl1 = t1 * n_edges;
                     if (k1 == k2)
                         tl1 -= one;
                     tl1 /= n_edges - one;
                     double rl = (tl1 - tl2) / (1.0 - tl2);
                     err += (r - rl) * (r - rl);
                }
             });
        if (!is_directed::apply<Graph>::type::value)
            err /= 2;
        r_err = sqrt(err);
    }
};

// this will calculate the _scalar_ assortativity coefficient, based on the
// scalar property pointed by 'deg'

struct get_scalar_assortativity_coefficient
{
    template <class Graph, class DegreeSelector>
    void operator()(const Graph& g, DegreeSelector deg, double& r,
                    double& r_err) const
    {
        size_t n_edges = 0;
        double e_xy = 0;
        double a = 0, b = 0, da = 0, db = 0;

        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            reduction(+:e_xy,n_edges,a,b,da,db)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 double k1 = double(deg(v, g));
                 for (auto u : out_neighbours_range(v, g))
                 {
                     auto k2 = deg(u, g);
                     a += k1;
                     da += k1 * k1;
                     b += k2;
                     db += k2 * k2;
                     e_xy += k1 * k2;
                     n_edges++;
                 }
             });

        double t1 = e_xy/n_edges;
        a /= n_edges;
        b /= n_edges;
        double stda = sqrt(da/n_edges - a*a);
        double stdb = sqrt(db/n_edges - b*b);

        if (stda*stdb > 0)
            r = (t1 - a*b)/(stda*stdb);
        else
            r = (t1 - a*b);

        // "jackknife" variance
        r_err = 0.0;

        double err = 0.0;
        size_t one = (is_directed::apply<Graph>::type::value) ? 1 : 2;
        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            reduction(+:err)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 double k1 = double(deg(v, g));
                 double al = (a * n_edges - k1) / (n_edges - one);
                 double dal = sqrt((da - k1 * k1) / (n_edges - one) - al * al);

                 for (auto u : out_neighbours_range(v, g))
                 {
                     double k2 = deg(u, g);
                     double bl = (b * n_edges - k2 * one) / (n_edges - one);
                     double dbl = sqrt((db - k2 * k2 * one) / (n_edges - one) - bl * bl);
                     double t1l = (e_xy - k1 * k2 * one)/(n_edges - one);
                     double rl;
                     if (dal * dbl > 0)
                         rl = (t1l - al * bl)/(dal * dbl);
                     else
                         rl = (t1l - al * bl);
                     err += (r - rl) * (r - rl);
                 }
             });
        if (!is_directed::apply<Graph>::type::value)
            err /= 2;
        r_err = sqrt(err);
    }
};

} // graph_tool namespace

#endif //GRAPH_ASSORTATIVITY_HH

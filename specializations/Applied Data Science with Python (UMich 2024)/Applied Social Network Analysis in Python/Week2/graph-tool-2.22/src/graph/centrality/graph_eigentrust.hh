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

#ifndef GRAPH_TRUST_HH
#define GRAPH_TRUST_HH

#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_util.hh"

namespace graph_tool
{
using namespace std;

struct get_eigentrust
{
    typedef void result_type;
    template <class Graph, class VertexIndex, class EdgeIndex, class TrustMap,
              class InferredTrustMap>
    void operator()(Graph& g, VertexIndex vertex_index,
                    EdgeIndex edge_index, TrustMap c, InferredTrustMap t,
                    double epslon, size_t max_iter, size_t& iter) const
    {
        using namespace boost;
        typedef typename property_traits<TrustMap>::value_type c_type;
        typedef typename property_traits<InferredTrustMap>::value_type t_type;

        InferredTrustMap t_temp(vertex_index, num_vertices(g));

        // Norm c values
        InferredTrustMap c_sum(vertex_index);
        if (is_directed::apply<Graph>::type::value)
        {
            TrustMap c_temp(edge_index, c.get_storage().size());
            parallel_vertex_loop
                (g,
                 [&](auto v)
                 {
                     c_type sum = 0;
                     for (const auto& e : out_edges_range(v, g))
                         sum += get(c, e);
                     if (sum > 0)
                     {
                         for (const auto& e : out_edges_range(v, g))
                             put(c_temp, e, get(c, e) / sum);
                     }
                 });
            c = c_temp;
        }
        else
        {
            c_sum.reserve(num_vertices(g));
            parallel_vertex_loop
                (g,
                 [&](auto v)
                 {
                     c_sum[v] = 0;
                     for (const auto& e : out_edges_range(v, g))
                         c_sum[v] += c[e];
                 });
        }

        // init inferred trust t
        auto V = HardNumVertices()(g);
        parallel_vertex_loop(g, [&](auto v) { t[v] = 1.0/V; });

        t_type delta = epslon + 1;
        iter = 0;
        while (delta >= epslon)
        {
            delta = 0;
            #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
                reduction(+:delta)
            parallel_vertex_loop_no_spawn
                (g,
                 [&](auto v)
                 {
                     t_temp[v] = 0;
                     for (const auto& e : in_or_out_edges_range(v, g))
                     {
                         typename graph_traits<Graph>::vertex_descriptor s;
                         if (is_directed::apply<Graph>::type::value)
                             s = source(e, g);
                         else
                             s = target(e, g);
                         if (!is_directed::apply<Graph>::type::value)
                             t_temp[v] += get(c, e) * t[s] / abs(c_sum[s]);
                         else
                             t_temp[v] += get(c, e) * t[s];
                     }
                     delta += abs(t_temp[v] - t[v]);
                 });
            swap(t_temp, t);

            ++iter;
            if (max_iter > 0 && iter== max_iter)
                break;
        }

        if (iter % 2 != 0)
            parallel_vertex_loop(g, [&](auto v) {t[v] = t_temp[v];});
    }
};

}

#endif

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

#ifndef GRAPH_EIGENVECTOR_HH
#define GRAPH_EIGENVECTOR_HH

#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_util.hh"

#ifndef __clang__
#include <ext/numeric>
using __gnu_cxx::power;
#else
template <class Value>
Value power(Value value, int n)
{
    return pow(value, n);
}
#endif

namespace graph_tool
{
using namespace std;
using namespace boost;

struct get_eigenvector
{
    template <class Graph, class VertexIndex, class WeightMap,
              class CentralityMap>
    void operator()(Graph& g, VertexIndex vertex_index, WeightMap w,
                    CentralityMap c, double epsilon, size_t max_iter,
                    long double& eig) const
    {
        typedef typename property_traits<CentralityMap>::value_type t_type;

        CentralityMap c_temp(vertex_index, num_vertices(g));

        t_type norm = 0;
        t_type delta = epsilon + 1;
        t_type prev_delta = delta + 1;
        size_t iter = 0;
        while (delta >= epsilon)
        {
            prev_delta = delta;
            norm = 0;
            #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
                reduction(+:norm)
            parallel_vertex_loop_no_spawn
                (g,
                 [&](auto v)
                 {
                     c_temp[v] = 0;
                     for (const auto& e : in_or_out_edges_range(v, g))
                     {
                         typename graph_traits<Graph>::vertex_descriptor s;
                         if (is_directed::apply<Graph>::type::value)
                             s = source(e, g);
                         else
                             s = target(e, g);
                         c_temp[v] += get(w, e) * c[s];
                     }
                     norm += power(c_temp[v], 2);
                 });

            norm = sqrt(norm);

            delta = 0;
            #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
                reduction(+:delta)
            parallel_vertex_loop_no_spawn
                (g,
                 [&](auto v)
                 {
                     c_temp[v] /= norm;
                     delta += abs(c_temp[v] - c[v]);
                 });

            swap(c_temp, c);

            ++iter;
            if (max_iter > 0 && iter == max_iter)
                break;
            if (max_iter == 0 && delta >= prev_delta && iter > 100)
                break;
        }

        if (iter % 2 != 0)
            parallel_vertex_loop(g, [&](auto v) { c[v] = c_temp[v]; });

        eig = norm;
    }
};

}

#endif

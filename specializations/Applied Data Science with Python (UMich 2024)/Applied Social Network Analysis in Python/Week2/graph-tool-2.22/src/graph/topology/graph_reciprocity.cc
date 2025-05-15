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


#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_selectors.hh"
#include "graph_properties.hh"

using namespace std;
using namespace boost;
using namespace graph_tool;

struct get_reciprocity
{
    template <class Graph>
    void operator()(const Graph& g, double& reciprocity) const
    {
        size_t L = 0, Lbd = 0;

        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            reduction(+: L, Lbd)
        parallel_edge_loop_no_spawn
            (g,
             [&](auto e)
             {
                 auto v = source(e, g);
                 auto t = target(e, g);
                 for (auto a : adjacent_vertices_range(t, g))
                 {
                     if (a == v)
                     {
                         Lbd++;
                         break;
                     }
                 }
                 L++;
             });
        reciprocity = Lbd / double(L);
    }
};

double reciprocity(GraphInterface& gi)
{
    double reciprocity;
    run_action<>()(gi, std::bind(get_reciprocity(), std::placeholders::_1,
                                 std::ref(reciprocity)))();
    return reciprocity;
}

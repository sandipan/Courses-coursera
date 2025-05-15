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

#ifndef GRAPH_PREDECESSOR_HH
#define GRAPH_PREDECESSOR_HH

#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_util.hh"

namespace graph_tool
{
using namespace std;
using namespace boost;

struct get_predecessor_graph
{
    template <class Graph, class PredGraph, class PredMap>
    void operator()(Graph& g, PredGraph& pg, PredMap pred_map) const
    {
        while (num_vertices(pg) < num_vertices(g))
            add_vertex(pg);

        for (auto v : vertices_range(g))
        {
            size_t pred_i = get(pred_map, v);
            if (pred_i >= num_vertices(g))
                continue;

            size_t pred = vertex(pred_i, g);
            if (pred == graph_traits<Graph>::null_vertex())
                continue;

            if (pred != v)
            {
                auto s = vertex(pred, pg);
                auto t = vertex(v, pg);
                add_edge(s, t, pg);
            }
        }
    }
};

} // graph_tool namespace

#endif // GRAPH_PREDECESSOR_HH

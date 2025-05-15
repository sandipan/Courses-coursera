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

#ifndef GRAPH_KCORE_HH
#define GRAPH_KCORE_HH

namespace graph_tool
{
using namespace std;
using namespace boost;

template <class Graph, class CoreMap>
void kcore_decomposition(Graph& g, CoreMap core_map)
{
    auto vertex_index = get(vertex_index_t(), g);

    typedef typename vprop_map_t<size_t>::type::unchecked_t vmap_t;

    vmap_t deg(vertex_index, num_vertices(g));  // Remaining degree
    vmap_t pos(vertex_index, num_vertices(g));  // Position in bin (core)

    typedef typename graph_traits<Graph>::vertex_descriptor vertex_t;

    vector<vector<vertex_t>> bins; // Each bin stores the set of vertices of
                                   // a core

    // Put each vertex to the bin corresponding to its degree
    for (auto v : vertices_range(g))
    {
        size_t k = degree(v, g);
        deg[v] = k;
        if (k >= bins.size())
            bins.resize(k + 1);
        bins[k].push_back(v);
        pos[v] = bins[k].size() - 1;
    }

    // Proceed from smallest bin to largest. For each vertex in bin, check
    // the neighbours; if any of them have a larger remaining degree, reduce
    // it by one, and put it in the correct bin.
    for (size_t k = 0; k < bins.size(); ++k)
    {
        auto& bins_k = bins[k];
        while (!bins_k.empty())
        {
            auto v = bins_k.back();
            bins_k.pop_back();
            core_map[v] = k;
            for (auto u : all_neighbours_range(v, g))
            {
                auto& ku = deg[u];
                if (ku > deg[v])
                {
                    auto& bins_ku = bins[ku];
                    auto w = bins_ku.back();
                    auto pos_w = pos[w] = pos[u];
                    bins_ku[pos_w] = w;
                    bins_ku.pop_back();
                    --ku;
                    auto& bins_ku_m = bins[ku];
                    bins_ku_m.push_back(u);
                    pos[u] = bins_ku_m.size() - 1;
                }
            }
        }
    }
}

} // graph_tool namespace

#endif // GRAPH_KCORE_HH

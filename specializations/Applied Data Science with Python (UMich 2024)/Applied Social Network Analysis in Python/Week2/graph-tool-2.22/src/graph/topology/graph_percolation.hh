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

#ifndef GRAPH_PERCOLATION_HH
#define GRAPH_PERCOLATION_HH

namespace graph_tool
{
using namespace std;
using namespace boost;

template <class Graph, class TreeMap>
typename graph_traits<Graph>::vertex_descriptor
find_root(size_t vi, TreeMap tree, Graph& g,
          vector<size_t>& temp)
{
    auto parent = vertex(vi, g);
    temp.clear();
    while(size_t(tree[vertex(parent, g)]) != parent)
    {
        temp.push_back(parent);
        parent = tree[vertex(parent, g)];
    }
    // path compression
    for (auto v: temp)
        tree[vertex(v, g)] = parent;
    return vertex(parent, g);
}


template <class Graph, class TreeMap, class SizeMap>
void join_cluster(const pair<size_t, size_t>& e, TreeMap tree, SizeMap size,
                  size_t& max_size, Graph& g, vector<size_t>& temp)
{
    auto rs = find_root(e.first, tree, g, temp);
    auto rt = find_root(e.second, tree, g, temp);
    if (rt != rs)
    {
        if (size[rs] < size[rt])
            swap(rs, rt);
        tree[rt] = rs;
        size[rs] += size[rt];
        max_size = max(size_t(size[rs]), max_size);
    }
}

template <class Graph, class TreeMap,
          class SizeMap, class MaxSize, class Edges>
void edge_percolate(Graph& g, TreeMap tree, SizeMap size, MaxSize& max_size,
                    Edges& edges)
{
    vector<size_t> temp;
    size_t s = 0;
    for (size_t i = 0; i < edges.size(); ++i)
    {
        join_cluster(make_pair(size_t(edges[i][0]), size_t(edges[i][1])),
                     tree, size, s, g, temp);
        max_size[i] = s;
    }

    boost::multi_array_ref<typename Edges::element, 1>
        vertices(edges.data(),
                 boost::extents[edges.num_elements()]);

    for (auto& v : vertices)
    {
        auto root = find_root(v, tree, g, temp);
        size[v] = size[root];
    }
};

template <class Graph,  class TreeMap, class SizeMap, class MaxSize,
          class Vertices>
void vertex_percolate(Graph& g, TreeMap tree, SizeMap size, MaxSize& max_size,
                      Vertices& vertices)
{
    vector<size_t> temp;
    size_t s = 0;
    for (size_t i = 0; i < vertices.size(); ++i)
    {
        auto v = vertex(vertices[i], g);
        if (v == graph_traits<Graph>::null_vertex())
        {
            max_size[i] = s;
            continue;
        }

        for (auto a : adjacent_vertices_range(v, g))
        {
            join_cluster(make_pair(size_t(v), size_t(a)), tree, size, s, g,
                         temp);
        }
        max_size[i] = s;
    }

    //flatten tree
    for (auto vi : vertices)
    {
        auto v = vertex(vi, g);
        if (v == graph_traits<Graph>::null_vertex())
            continue;
        auto root = find_root(vi, tree, g, temp);
        size[v] = size[root];
    }
}

} // graph_tool namespace

#endif // GRAPH_PERCOLATION_HH

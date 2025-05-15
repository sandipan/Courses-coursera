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

#ifndef GRAPH_SIMILARITY_HH
#define GRAPH_SIMILARITY_HH

#include "hash_map_wrap.hh"

namespace graph_tool
{
using namespace std;
using namespace boost;

template <class Keys, class Set1, class Set2>
auto set_difference(Keys& ks, Set1& s1, Set2& s2)
{
    typename Set1::value_type::second_type s = 0;
    for (auto& k : ks)
    {
        auto x1 = s1[k];
        auto x2 = s2[k];
        s += std::max(x1, x2) - std::min(x1, x2);
    }
    return s;
}

template <class Vertex, class WeightMap, class LabelMap, class Graph1, class Graph2>
auto vertex_difference(Vertex v1, Vertex v2, WeightMap& ew1, WeightMap& ew2,
                       LabelMap& l1, LabelMap& l2, const Graph1& g1,
                       const Graph2& g2)
{
    typedef typename property_traits<LabelMap>::value_type label_t;
    typedef typename property_traits<WeightMap>::value_type val_t;

    std::unordered_set<label_t> keys;
    std::unordered_map<label_t, val_t> adj1;
    std::unordered_map<label_t, val_t> adj2;

    if (v1 != graph_traits<Graph1>::null_vertex())
    {
        for (auto e : out_edges_range(v1, g1))
        {
            auto w = ew1[e];
            auto k = get(l1, target(e, g1));
            adj1[k] += w;
            keys.insert(k);
        }
    }

    if (v2 != graph_traits<Graph2>::null_vertex())
    {
        for (auto e : out_edges_range(v2, g2))
        {
            auto w = ew2[e];
            auto k = get(l2, target(e, g2));
            adj2[k] += w;
            keys.insert(k);
        }
    }

    return set_difference(keys, adj1, adj2);
}

template <class Graph1, class Graph2, class WeightMap, class LabelMap>
auto get_similarity(const Graph1& g1, const Graph2& g2, WeightMap ew1,
                    WeightMap ew2, LabelMap l1, LabelMap l2)
{
    typedef typename property_traits<LabelMap>::value_type label_t;
    typedef typename property_traits<WeightMap>::value_type val_t;

    typedef typename graph_traits<Graph1>::vertex_descriptor vertex_t;
    std::unordered_map<label_t, vertex_t> lmap1;
    std::unordered_map<label_t, vertex_t> lmap2;

    for (auto v : vertices_range(g1))
        lmap1[get(l1, v)] = v;
    for (auto v : vertices_range(g2))
        lmap2[get(l2, v)] = v;

    val_t s = 0;
    for (auto& lv1 : lmap1)
    {
        vertex_t v1 = lv1.second;
        vertex_t v2;

        auto li2 = lmap2.find(lv1.first);
        if (li2 == lmap2.end())
            v2 = graph_traits<Graph2>::null_vertex();
        else
            v2 = li2->second;

        s += vertex_difference(v1, v2, ew1, ew2, l1, l2, g1, g2);
    }

    for (auto& lv2 : lmap2)
    {
        vertex_t v2 = lv2.second;
        vertex_t v1;

        auto li1 = lmap1.find(lv2.first);
        if (li1 == lmap1.end())
            v1 = graph_traits<Graph2>::null_vertex();
        else
            continue;

        s += vertex_difference(v1, v2, ew1, ew2, l1, l2, g1, g2);
    }
    return s;
}

template <class Graph1, class Graph2, class WeightMap, class LabelMap>
auto get_similarity_fast(const Graph1& g1, const Graph2& g2, WeightMap ew1,
                         WeightMap ew2, LabelMap l1, LabelMap l2)
{
    typedef typename property_traits<WeightMap>::value_type val_t;
    typedef typename graph_traits<Graph1>::vertex_descriptor vertex_t;

    vector<vertex_t> lmap1, lmap2;

    for (auto v : vertices_range(g1))
    {
        size_t i = get(l1, v);
        if (lmap1.size() <= i)
            lmap1.resize(i + 1, graph_traits<Graph1>::null_vertex());
        lmap1[i] = v;
    }

    for (auto v : vertices_range(g2))
    {
        size_t i = get(l2, v);
        if (lmap2.size() <= i)
            lmap2.resize(i + 1, graph_traits<Graph2>::null_vertex());
        lmap2[i] = v;
    }

    size_t N = std::max(lmap1.size(), lmap2.size());
    lmap1.resize(N, graph_traits<Graph1>::null_vertex());
    lmap2.resize(N, graph_traits<Graph2>::null_vertex());

    val_t s = 0;
    #pragma omp parallel if (num_vertices(g1) > OPENMP_MIN_THRESH) \
        reduction(+:s)
    parallel_loop_no_spawn
        (lmap1,
         [&](size_t i, auto v1)
         {
             auto v2 = lmap2[i];
             if (v1 == graph_traits<Graph1>::null_vertex() &&
                 v2 == graph_traits<Graph1>::null_vertex())
                 return;
             s += vertex_difference(v1, v2, ew1, ew2, l1, l2, g1, g2);
         });

    #pragma omp parallel if (num_vertices(g2) > OPENMP_MIN_THRESH)  \
        reduction(+:s)
    parallel_loop_no_spawn
        (lmap2,
         [&](size_t i, auto v2)
         {
             auto v1 = lmap1[i];
             if (v1 != graph_traits<Graph1>::null_vertex() ||
                 v2 == graph_traits<Graph1>::null_vertex())
                 return;
             s += vertex_difference(v1, v2, ew1, ew2, l1, l2, g1, g2);
         });

    return s;
}

} // graph_tool namespace

#endif // GRAPH_SIMILARITY_HH

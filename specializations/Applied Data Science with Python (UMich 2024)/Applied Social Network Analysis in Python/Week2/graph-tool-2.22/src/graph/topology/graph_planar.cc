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

#include "graph_filtering.hh"
#include "graph.hh"
#include "graph_properties.hh"

#include <boost/graph/boyer_myrvold_planar_test.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct get_planar_embedding
{
    template <class EdgeMap>
    class edge_inserter
    {
    public:
        edge_inserter(EdgeMap edge_map): _edge_map(edge_map) {}

        edge_inserter& operator++() { return *this; }
        edge_inserter& operator++(int) { return *this; }
        edge_inserter& operator*() { return *this; }

        template <class Key>
        edge_inserter& operator=(const Key& e)
        {
            _edge_map[e] = 1;
            return *this;
        }

    private:
        EdgeMap _edge_map;
    };

    template <class Graph, class VertexIndex, class EdgeIndex, class EmbedMap,
              class KurMap>
    void operator()(Graph& g, VertexIndex vertex_index, EdgeIndex edge_index,
                    EmbedMap embed_map, KurMap kur_map, bool& is_planar) const
    {
        edge_inserter<KurMap> kur_insert(kur_map);
        unchecked_vector_property_map
            <vector<typename graph_traits<Graph>::edge_descriptor>, VertexIndex>
            embedding(vertex_index, num_vertices(g));
        is_planar = boyer_myrvold_planarity_test
            (boyer_myrvold_params::graph = g,
             boyer_myrvold_params::edge_index_map = edge_index,
             boyer_myrvold_params::embedding = embedding,
             boyer_myrvold_params::kuratowski_subgraph = kur_insert);

        parallel_vertex_loop
            (g,
             [&](auto v)
             {
                 embed_map[v].clear();
                 for (auto& e : embedding[v])
                     embed_map[v].push_back(edge_index[e]);
             });
    }

    template <class Graph, class VertexIndex, class EdgeIndex, class KurMap>
    void operator()(Graph& g, VertexIndex, EdgeIndex edge_index,
                    dummy_property_map, KurMap kur_map,
                    bool& is_planar) const
    {
        edge_inserter<KurMap> kur_insert(kur_map);
        is_planar = boyer_myrvold_planarity_test
            (boyer_myrvold_params::graph = g,
             boyer_myrvold_params::edge_index_map = edge_index,
             boyer_myrvold_params::kuratowski_subgraph = kur_insert);
    }
};

bool is_planar(GraphInterface& gi, boost::any embed_map, boost::any kur_map)
{
    bool is_planar;

    if (embed_map.empty())
        embed_map = dummy_property_map();
    if (kur_map.empty())
        kur_map = dummy_property_map();

    typedef mpl::push_back<writable_edge_scalar_properties,
                           dummy_property_map>::type edge_map_types;
    typedef mpl::push_back<vertex_scalar_vector_properties,
                           dummy_property_map>::type vertex_map_types;

    run_action<graph_tool::detail::never_directed>()
        (gi, std::bind(get_planar_embedding(), std::placeholders::_1, gi.get_vertex_index(),
                       gi.get_edge_index(), std::placeholders::_2, std::placeholders::_3,
                       std::ref(is_planar)),
         vertex_map_types(), edge_map_types())
        (embed_map, kur_map);
    return is_planar;
}

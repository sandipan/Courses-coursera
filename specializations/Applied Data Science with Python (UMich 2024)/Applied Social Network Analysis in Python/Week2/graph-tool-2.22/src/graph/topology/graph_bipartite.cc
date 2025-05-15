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

#include <boost/graph/bipartite.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct get_bipartite
{
    template <class Graph, class VertexIndex, class PartMap>
    void operator()(Graph& g, VertexIndex vertex_index, PartMap part_map,
                    bool& is_bip, bool find_cycle, vector<size_t>& odd_cycle)
        const
    {
        unchecked_vector_property_map<default_color_type, VertexIndex>
            part(vertex_index, num_vertices(g));

        if (!find_cycle)
        {
            is_bip = is_bipartite(g, vertex_index, part);
        }
        else
        {
            find_odd_cycle(g, vertex_index, part, std::back_inserter(odd_cycle));
            is_bip = odd_cycle.empty();
        }

        parallel_vertex_loop
            (g,
             [&](auto v)
             {
                 part_map[v] = (part[v] == color_traits<default_color_type>::white());
             });
    }

    template <class Graph, class VertexIndex>
    void operator()(Graph& g, VertexIndex vertex_index, dummy_property_map,
                    bool& is_bip, bool find_cycle, vector<size_t>& odd_cycle) const
    {
        if (!find_cycle)
        {
            is_bip = is_bipartite(g, vertex_index);
        }
        else
        {
            find_odd_cycle(g, vertex_index, std::back_inserter(odd_cycle));
            is_bip = odd_cycle.empty();
        }
    }
};

bool is_bipartite(GraphInterface& gi, boost::any part_map, bool find_cycle,
                  boost::python::list cycle)
{
    bool is_bip;
    vector<size_t> vcycle;

    if (part_map.empty())
        part_map = dummy_property_map();

    typedef mpl::push_back<writable_vertex_scalar_properties,
                           dummy_property_map>::type vertex_map_types;

    run_action<graph_tool::detail::never_directed>()
        (gi, std::bind(get_bipartite(), std::placeholders::_1,
                       gi.get_vertex_index(), std::placeholders::_2,
                       std::ref(is_bip), find_cycle, std::ref(vcycle)),
         vertex_map_types())(part_map);

    for (auto v : vcycle)
        cycle.append(v);

    return is_bip;
}

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

#include "graph_python_interface.hh"
#include "graph_filtering.hh"
#include "graph.hh"
#include "graph_selectors.hh"
#include "graph_properties.hh"

#include <boost/bind.hpp>
#include <boost/bind/placeholders.hpp>
#include <boost/mpl/push_back.hpp>
#include <boost/python.hpp>

#include "graph_community_network.hh"

using namespace std;
using namespace boost;

using namespace graph_tool;

typedef UnityPropertyMap<int,GraphInterface::edge_t> no_eweight_map_t;
typedef eprop_map_t<int32_t>::type ecount_map_t;

struct get_edge_sum_dispatch
{
    template <class Graph, class CommunityGraph, class CommunityMap,
              class Eprop>
    void operator()(const Graph& g, CommunityGraph& cg, CommunityMap s_map,
                    boost::any acs_map, Eprop eprop, boost::any aceprop,
                    bool self_loops, bool parallel_edges) const
    {
        typename CommunityMap::checked_t cs_map = boost::any_cast<typename CommunityMap::checked_t>(acs_map);
        typename Eprop::checked_t ceprop = boost::any_cast<typename Eprop::checked_t>(aceprop);
        get_edge_community_property_sum()(g, cg, s_map, cs_map, eprop, ceprop,
                                          self_loops, parallel_edges);
    }
};

void sum_eprops(GraphInterface& gi, GraphInterface& cgi,
                boost::any community_property,
                boost::any condensed_community_property, boost::any ceprop,
                boost::any eprop, bool self_loops, bool parallel_edges)
{
    typedef boost::mpl::insert_range<writable_edge_scalar_properties,
                                     boost::mpl::end<writable_edge_scalar_properties>::type,
                                     edge_scalar_vector_properties>::type eprops_temp;
    typedef boost::mpl::push_back<eprops_temp,
                                  eprop_map_t<boost::python::object>::type >::type
        eprops_t;

    run_action<>()
        (gi, std::bind(get_edge_sum_dispatch(),
                       std::placeholders::_1, std::ref(cgi.get_graph()),
                       std::placeholders::_2,
                       condensed_community_property, std::placeholders::_3,
                       ceprop, self_loops, parallel_edges),
         writable_vertex_properties(), eprops_t())
        (community_property, eprop);
}

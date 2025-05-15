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

struct get_weighted_edge_property_dispatch
{
    template <class Graph, class EdgeWeightMap, class Eprop>
    void operator()(const Graph& g, EdgeWeightMap eweight, Eprop eprop,
                    boost::any atemp) const
    {
        typename Eprop::checked_t temp = boost::any_cast<typename Eprop::checked_t>(atemp);
        get_weighted_edge_property()(g, eweight, eprop,
                                     temp.get_unchecked(eprop.get_storage().size()));
    }
};

void sum_eprops(GraphInterface& gi, GraphInterface& cgi,
                boost::any community_property,
                boost::any condensed_community_property, boost::any ceprop,
                boost::any eprop, bool self_loops, bool parallel_edges);

void community_network_eavg(GraphInterface& gi, GraphInterface& cgi,
                            boost::any community_property,
                            boost::any condensed_community_property,
                            boost::any eweight, boost::python::list aeprops,
                            bool self_loops, bool parallel_edges)
{
    typedef boost::mpl::push_back<writable_edge_scalar_properties, no_eweight_map_t>::type
        eweight_properties;

    bool no_weight = false;
    if (eweight.empty())
    {
        no_weight = true;
        eweight = no_eweight_map_t();
    }

    typedef boost::mpl::insert_range<writable_edge_scalar_properties,
                                     boost::mpl::end<writable_edge_scalar_properties>::type,
                                     edge_scalar_vector_properties>::type eprops_temp;
    typedef boost::mpl::push_back<eprops_temp,
                                  eprop_map_t<boost::python::object>::type >::type
        eprops_t;

    for(int i = 0; i < boost::python::len(aeprops); ++i)
    {
        boost::any eprop = boost::python::extract<any>(aeprops[i][0])();
        boost::any temp = boost::python::extract<any>(aeprops[i][1])();
        boost::any ceprop = boost::python::extract<any>(aeprops[i][2])();

        if (!no_weight)
        {
            // compute weighted values to temp
            run_action<>()
                (gi, std::bind(get_weighted_edge_property_dispatch(),
                               std::placeholders::_1, std::placeholders::_2,
                               std::placeholders::_3, temp),
                 eweight_properties(), eprops_t())
                (eweight, eprop);

            // sum weighted values
            sum_eprops(gi, cgi, community_property,
                       condensed_community_property, ceprop, temp,
                       self_loops, parallel_edges);
        }
        else
        {
            // sum unweighted values
            sum_eprops(gi, cgi, community_property,
                       condensed_community_property, ceprop, eprop,
                       self_loops, parallel_edges);
        }

    }
}

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

#include "graph_modularity.hh"

#include <boost/mpl/push_back.hpp>
#include <boost/python.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

double modularity(GraphInterface& gi, boost::any weight, boost::any property)
{
    double Q = 0;

    typedef UnityPropertyMap<int, GraphInterface::edge_t> weight_map_t;
    typedef boost::mpl::push_back<edge_scalar_properties, weight_map_t>::type
        edge_props_t;

    if(weight.empty())
        weight = weight_map_t();

    run_action<>()
        (gi, [&](auto& g, auto& w, auto& b){ Q = get_modularity(g, w, b);},
         edge_props_t(), vertex_scalar_properties())
        (weight, property);

    return Q;
}

using namespace boost::python;

void export_modularity()
{
    def("modularity", &modularity);
}

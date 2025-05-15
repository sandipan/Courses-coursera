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

#include "graph_union.hh"

#include <boost/bind.hpp>

#include <boost/python/extract.hpp>

using namespace graph_tool;
using namespace boost;

typedef vprop_map_t<int64_t>::type vprop_t;

typedef eprop_map_t<GraphInterface::edge_t>::type eprop_t;

boost::python::tuple graph_union(GraphInterface& ugi, GraphInterface& gi,
                                 boost::any avprop)
{
    vprop_t vprop = boost::any_cast<vprop_t>(avprop);
    eprop_t eprop(gi.get_edge_index());
    gt_dispatch<boost::mpl::true_>()
        (std::bind(graph_tool::graph_union(),
                   std::placeholders::_1, std::placeholders::_2, vprop, eprop),
         always_directed(), always_directed())
        (ugi.get_graph_view(), gi.get_graph_view());
    return boost::python::make_tuple(avprop, boost::any(eprop));
}

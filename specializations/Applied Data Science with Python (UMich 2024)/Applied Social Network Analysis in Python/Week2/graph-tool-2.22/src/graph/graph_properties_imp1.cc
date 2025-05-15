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
#include "graph.hh"
#include "graph_properties.hh"
#include "graph_filtering.hh"
#include "graph_selectors.hh"
#include "graph_util.hh"

#ifdef USING_OPENMP
#include <omp.h>
#endif

using namespace std;
using namespace boost;
using namespace graph_tool;

template <bool src>
struct do_edge_endpoint
{
    template <class Graph, class EdgeIndexMap, class VertexPropertyMap>
    void operator()(Graph& g, EdgeIndexMap, VertexPropertyMap prop,
                    boost::any aeprop, size_t edge_index_range) const
    {
        typedef typename property_traits<VertexPropertyMap>::value_type vval_t;
        typedef typename boost::mpl::if_<std::is_same<vval_t, size_t>, int64_t, vval_t>::type
            val_t;
        typedef typename property_map_type::apply<val_t, EdgeIndexMap>::type
            eprop_t;
        eprop_t eprop = any_cast<eprop_t>(aeprop);
        eprop.reserve(edge_index_range);

        #ifdef USING_OPENMP
        size_t __attribute__ ((unused)) nt = omp_get_num_threads();
        if (std::is_convertible<val_t,python::object>::value)
            nt = 1; // python is not thread-safe
        #endif

        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            num_threads(nt)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 for (const auto& e : out_edges_range(v, g))
                 {
                     auto s = v;
                     auto t = target(e, g);
                     if (!is_directed::apply<Graph>::type::value && s > t)
                         continue;
                     if (src)
                         eprop[e] = prop[s];
                     else
                         eprop[e] = prop[t];
                 }
             });
    }
};

void edge_endpoint(GraphInterface& gi, boost::any prop,
                   boost::any eprop, std::string endpoint)
{
    size_t edge_index_range = gi.get_edge_index_range();
    if (endpoint == "source")
        run_action<>()(gi, std::bind(do_edge_endpoint<true>(), std::placeholders::_1,
                                     gi.get_edge_index(), std::placeholders::_2, eprop,
                                     edge_index_range),
                       vertex_properties())(prop);
    else
        run_action<>()(gi, std::bind(do_edge_endpoint<false>(), std::placeholders::_1,
                                     gi.get_edge_index(), std::placeholders::_2, eprop,
                                     edge_index_range),
                       vertex_properties())(prop);
}

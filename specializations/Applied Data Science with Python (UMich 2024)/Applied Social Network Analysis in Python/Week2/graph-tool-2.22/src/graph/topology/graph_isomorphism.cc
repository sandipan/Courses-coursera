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

#include <boost/graph/isomorphism.hpp>

using namespace graph_tool;
using namespace boost;

struct check_iso
{

    template <class Graph1, class Graph2, class IsoMap, class InvMap,
              class VertexIndexMap>
    void operator()(Graph1& g1, Graph2& g2, InvMap cinv_map1, InvMap cinv_map2,
                    int64_t max_inv, IsoMap map, VertexIndexMap index1,
                    VertexIndexMap index2, bool& result) const
    {
        auto inv_map1 = cinv_map1.get_unchecked(num_vertices(g1));
        auto inv_map2 = cinv_map2.get_unchecked(num_vertices(g2));

        vinv_t<decltype(inv_map1)> vinv1(inv_map1, max_inv);
        vinv_t<decltype(inv_map2)> vinv2(inv_map2, max_inv);

        result = isomorphism(g1, g2,
                             isomorphism_map(map.get_unchecked(num_vertices(g1))).
                             vertex_invariant1(vinv1).
                             vertex_invariant2(vinv2).
                             vertex_index1_map(index1).
                             vertex_index2_map(index2));
    }

    template <class Prop>
    struct vinv_t
    {
        vinv_t(Prop& prop, int64_t max)
            : _prop(prop), _max(max) {}
        Prop& _prop;
        int64_t _max;

        template <class Vertex>
        int64_t operator()(Vertex v) const
        {
            return _prop[v];
        };

        int64_t max() const { return _max; }

        typedef int64_t result_type;
        typedef size_t argument_type;
    };
};

typedef property_map_types::apply<integer_types,
                                  GraphInterface::vertex_index_map_t,
                                  mpl::bool_<false> >::type
    vertex_props_t;

bool check_isomorphism(GraphInterface& gi1, GraphInterface& gi2,
                       boost::any ainv_map1, boost::any ainv_map2,
                       int64_t max_inv, boost::any aiso_map)
{
    bool result;

    typedef vprop_map_t<int32_t>::type iso_map_t;
    auto iso_map = any_cast<iso_map_t>(aiso_map);

    typedef vprop_map_t<int64_t>::type inv_map_t;
    auto inv_map1 = any_cast<inv_map_t>(ainv_map1);
    auto inv_map2 = any_cast<inv_map_t>(ainv_map2);

    if (gi1.get_directed() != gi2.get_directed())
        return false;
    if (gi1.get_directed())
    {
        gt_dispatch<>()
            (std::bind(check_iso(),
                       std::placeholders::_1, std::placeholders::_2,
                       inv_map1, inv_map2, max_inv, iso_map,
                       gi1.get_vertex_index(),
                       gi2.get_vertex_index(), std::ref(result)),
             always_directed(), always_directed())
            (gi1.get_graph_view(), gi2.get_graph_view());
    }
    else
    {
        gt_dispatch<>()
            (std::bind(check_iso(),
                       std::placeholders::_1, std::placeholders::_2,
                       inv_map1, inv_map2, max_inv, iso_map,
                       gi1.get_vertex_index(),
                       gi2.get_vertex_index(), std::ref(result)),
             never_directed(), never_directed())
            (gi1.get_graph_view(), gi2.get_graph_view());
    }

    return result;
}

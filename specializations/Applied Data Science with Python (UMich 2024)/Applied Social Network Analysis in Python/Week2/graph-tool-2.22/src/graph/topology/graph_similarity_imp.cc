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
#include "graph_filtering.hh"
#include "graph_properties.hh"
#include "graph_selectors.hh"

#include "graph_similarity.hh"

using namespace std;
using namespace boost;
using namespace graph_tool;

template <class Type, class Index>
auto uncheck(boost::unchecked_vector_property_map<Type,Index>, boost::any p)
{
    return boost::any_cast<boost::checked_vector_property_map<Type,Index>>(p).get_unchecked();
}

template <class T>
auto&& uncheck(T&&, boost::any p)
{
    return boost::any_cast<T>(p);
}

typedef UnityPropertyMap<size_t,GraphInterface::edge_t> ecmap_t;
typedef boost::mpl::push_back<edge_scalar_properties, ecmap_t>::type
        weight_props_t;

python::object similarity_fast(GraphInterface& gi1, GraphInterface& gi2,
                               boost::any weight1, boost::any weight2,
                               boost::any label1, boost::any label2)
{
    if (weight1.empty())
        weight1 = ecmap_t();
    if (weight2.empty())
        weight2 = ecmap_t();
    python::object s;
    gt_dispatch<>()
        ([&](const auto& g1, const auto& g2, auto ew1, auto l1)
         {
             auto l2 = uncheck(l1, label2);
             auto ew2 = uncheck(ew1, weight2);
             auto ret = get_similarity_fast(g1, g2, ew1, ew2, l1, l2);
             s = python::object(ret);
         },
         all_graph_views(),
         all_graph_views(),
         weight_props_t(),
         vertex_integer_properties())
        (gi1.get_graph_view(), gi2.get_graph_view(), weight1, label1);
    return s;
}

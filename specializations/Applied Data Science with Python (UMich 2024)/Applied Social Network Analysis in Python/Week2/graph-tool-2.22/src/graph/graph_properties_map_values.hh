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

#ifndef GRAPH_PROPERTIES_MAP_VALUES_HH
#define GRAPH_PROPERTIES_MAP_VALUES_HH

#include <unordered_map>
#include <boost/python/extract.hpp>

namespace graph_tool
{

using namespace boost;

struct do_map_values
{

    template <class Graph, class SrcProp, class TgtProp>
    void operator()(Graph& g, SrcProp src, TgtProp tgt, python::object& mapper) const
    {
        typedef typename graph_traits<Graph>::vertex_descriptor vertex_t;
        typedef typename property_traits<SrcProp>::key_type key_type;
        typedef typename property_traits<SrcProp>::value_type src_value_type;
        typedef typename property_traits<TgtProp>::value_type tgt_value_type;

        std::unordered_map<src_value_type, tgt_value_type> value_map;

        dispatch(g, src, tgt, value_map, mapper, std::is_same<key_type, vertex_t>());

    }

    template <class Graph, class SrcProp, class TgtProp, class ValueMap>
    void dispatch(Graph& g, SrcProp& src, TgtProp& tgt, ValueMap& value_map,
                  python::object& mapper, std::true_type) const
    {
        dispatch_descriptor(src, tgt, value_map, mapper, vertices_range(g));
    }

    template <class Graph, class SrcProp, class TgtProp, class ValueMap>
    void dispatch(Graph& g, SrcProp& src, TgtProp& tgt, ValueMap& value_map,
                  python::object& mapper, std::false_type) const
    {
        dispatch_descriptor(src, tgt, value_map, mapper, edges_range(g));
    }

    template <class SrcProp, class TgtProp, class ValueMap, class Range>
    void dispatch_descriptor(SrcProp& src, TgtProp& tgt, ValueMap& value_map,
                             python::object& mapper, Range&& range) const
    {
        typedef typename property_traits<TgtProp>::value_type tgt_value_type;
        for (const auto& v : range)
        {
            const auto& k = src[v];
            const auto& iter = value_map.find(k);
            if (iter == value_map.end())
            {
                value_map[k] = tgt[v] =
                    boost::python::extract<tgt_value_type>(mapper(k));
            }
            else
            {
                tgt[v] = iter->second;
            }
        }
    }
};

} // namespace graph_tool

#endif // GRAPH_PROPERTIES_MAP_VALUES_HH

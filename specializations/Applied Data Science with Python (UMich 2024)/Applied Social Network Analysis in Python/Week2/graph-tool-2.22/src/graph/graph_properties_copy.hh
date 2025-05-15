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

#ifndef GRAPH_PROPERTIES_COPY_HH
#define GRAPH_PROPERTIES_COPY_HH

#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_properties.hh"

#include <boost/mpl/contains.hpp>
#include <boost/python/extract.hpp>

namespace graph_tool
{

//
// Property map copying
// ====================

template <class IteratorSel, class PropertyMaps>
struct copy_property
{
    template <class GraphTgt, class GraphSrc, class PropertyTgt>
    void operator()(const GraphTgt& tgt, const GraphSrc& src,
                    PropertyTgt dst_map, boost::any prop_src) const
    {
        try
        {
            auto src_map = boost::any_cast<typename PropertyTgt::checked_t>(prop_src);
            dispatch(tgt, src, dst_map, src_map);
        }
        catch (boost::bad_any_cast)
        {
            typedef typename boost::property_traits<PropertyTgt>::value_type val_tgt;
            typedef typename IteratorSel::template get_descriptor<GraphSrc>::type src_d;

            DynamicPropertyMapWrap<val_tgt, src_d> src_map(prop_src, PropertyMaps());

            dispatch(tgt, src, dst_map, src_map);
        }
    }

    template <class GraphTgt, class GraphSrc, class PropertyTgt, class PropertySrc>
    void dispatch(const GraphTgt& tgt, const GraphSrc& src,
                  PropertyTgt dst_map, PropertySrc src_map) const
    {
        try
        {
            typename IteratorSel::template apply<GraphSrc>::type vs, vs_end;
            typename IteratorSel::template apply<GraphTgt>::type vt, vt_end;
            std::tie(vt, vt_end) = IteratorSel::range(tgt);
            std::tie(vs, vs_end) = IteratorSel::range(src);
            for (; vs != vs_end; ++vs)
            {
                put(dst_map, *vt++, get(src_map, *vs));
            }
        }
        catch (boost::bad_lexical_cast&)
        {
            throw ValueException("property values are not convertible");
        }
    }

};

struct edge_selector
{
    template <class Graph>
    struct apply
    {
        typedef typename boost::graph_traits<Graph>::edge_iterator type;
    };

    template <class Graph>
    struct get_descriptor
    {
        typedef typename boost::graph_traits<Graph>::edge_descriptor type;
    };

    template <class Graph>
    static std::pair<typename apply<Graph>::type,
                     typename apply<Graph>::type>
    range(Graph& g)
    {
        return edges(g);
    }
};

struct vertex_selector
{
    template <class Graph>
    struct apply
    {
        typedef typename boost::graph_traits<Graph>::vertex_iterator type;
    };

    template <class Graph>
    struct get_descriptor
    {
        typedef typename boost::graph_traits<Graph>::vertex_descriptor type;
    };

    template <class Graph>
    static std::pair<typename apply<Graph>::type,
                     typename apply<Graph>::type>
    range(Graph& g)
    {
        return vertices(g);
    }
};

} // namespace graph_tool

#endif // GRAPH_PROPERTIES_COPY_HH

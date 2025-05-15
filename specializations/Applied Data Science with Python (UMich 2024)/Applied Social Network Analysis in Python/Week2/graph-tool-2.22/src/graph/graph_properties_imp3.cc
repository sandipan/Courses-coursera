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
#include "hash_map_wrap.hh"

#include <boost/mpl/for_each.hpp>

#include <boost/python/extract.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct do_perfect_vhash
{
    template <class Graph, class VertexPropertyMap, class HashProp>
    void operator()(Graph& g, VertexPropertyMap prop, HashProp hprop,
                    boost::any& adict) const
    {
        typedef typename property_traits<VertexPropertyMap>::value_type val_t;
        typedef typename property_traits<HashProp>::value_type hash_t;
        typedef std::unordered_map<val_t, hash_t> dict_t;

        if (adict.empty())
            adict = dict_t();

        dict_t& dict = any_cast<dict_t&>(adict);

        for (auto v : vertices_range(g))
        {
            auto val = prop[v];
            auto iter = dict.find(val);
            hash_t h;
            if (iter == dict.end())
            {
                h = dict.size();
                dict[val] = h;
            }
            else
            {
                h = iter->second;
            }
            hprop[v] = h;
        }
    }
};

void perfect_vhash(GraphInterface& gi, boost::any prop, boost::any hprop,
                   boost::any& dict)
{
    run_action<graph_tool::detail::always_directed>()
        (gi, std::bind<void>(do_perfect_vhash(), std::placeholders::_1,
         std::placeholders::_2, std::placeholders::_3, std::ref(dict)),
         vertex_properties(), writable_vertex_scalar_properties())
        (prop, hprop);
}

struct do_set_vertex_property
{
    template <class Graph, class PropertyMap>
    void operator()(Graph& g, PropertyMap prop, boost::python::object oval) const
    {
        typedef typename property_traits<PropertyMap>::value_type val_t;
        val_t val = boost::python::extract<val_t>(oval);

        for (auto v : vertices_range(g))
            prop[v] = val;
    }
};

void set_vertex_property(GraphInterface& gi, boost::any prop,
                         boost::python::object val)
{
    run_action<>()(gi, std::bind(do_set_vertex_property(), std::placeholders::_1,
                                 std::placeholders::_2, val),
                   writable_vertex_properties())(prop);
}

struct do_set_edge_property
{
    template <class Graph, class PropertyMap>
    void operator()(Graph& g, PropertyMap prop, boost::python::object oval) const
    {
        typedef typename property_traits<PropertyMap>::value_type val_t;
        val_t val = boost::python::extract<val_t>(oval);

        for (auto e : edges_range(g))
            prop[e] = val;
    }
};

void set_edge_property(GraphInterface& gi, boost::any prop,
                       boost::python::object val)
{
    run_action<>()(gi, std::bind(do_set_edge_property(), std::placeholders::_1,
                                 std::placeholders::_2, val),
                   writable_edge_properties())(prop);
}

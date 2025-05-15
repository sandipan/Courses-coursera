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

#include "graph_filtering.hh"
#include "graph.hh"
#include "graph_python_interface.hh"
#include "demangle.hh"

#include <boost/python.hpp>
#include <boost/lambda/bind.hpp>
#include <functional>

using namespace std;
using namespace boost;
using namespace graph_tool;

// this will register the property maps types and all its possible access
// functions to python
struct export_vertex_property_map
{
    template <class PropertyMap>
    void operator()(PropertyMap) const
    {
        typedef PythonPropertyMap<PropertyMap> pmap_t;

        string type_name;
        if (std::is_same<typename boost::mpl::find<value_types,
                                                   typename pmap_t::value_type>::type,
                         typename boost::mpl::end<value_types>::type>::value)
            type_name =
                name_demangle(typeid(typename pmap_t::value_type).name());
        else
            type_name =
                type_names[boost::mpl::find<value_types,typename pmap_t::value_type>
                           ::type::pos::value];
        string class_name = "VertexPropertyMap<" + type_name + ">";

        typedef typename boost::mpl::if_<
            typename return_reference::apply<typename pmap_t::value_type>::type,
            boost::python::return_internal_reference<>,
            boost::python::return_value_policy<boost::python::return_by_value> >
            ::type return_policy;

        boost::python::class_<pmap_t> pclass(class_name.c_str(),
                                             boost::python::no_init);
        pclass.def("__hash__", &pmap_t::get_hash)
            .def("value_type", &pmap_t::get_type)
            .def("get_map", &pmap_t::get_map)
            .def("get_dynamic_map", &pmap_t::get_dynamic_map)
            .def("get_array", &pmap_t::get_array)
            .def("is_writable", &pmap_t::is_writable)
            .def("reserve", &pmap_t::reserve)
            .def("resize", &pmap_t::resize)
            .def("shrink_to_fit", &pmap_t::shrink_to_fit)
            .def("data_ptr", &pmap_t::data_ptr);

        typedef boost::mpl::transform<graph_tool::all_graph_views,
                                      boost::mpl::quote1<std::add_const> >::type const_graph_views;
        typedef boost::mpl::transform<graph_tool::all_graph_views,
                                      boost::mpl::quote1<std::add_pointer> >::type all_graph_views;
        typedef boost::mpl::transform<const_graph_views,
                                      boost::mpl::quote1<std::add_pointer> >::type all_const_graph_views;
        typedef boost::mpl::joint_view<all_graph_views, all_const_graph_views>::type graph_views;

        boost::mpl::for_each<graph_views>(std::bind(dispatch_access<PropertyMap>(),
                                                    std::placeholders::_1,
                                                    std::ref(pclass), return_policy()));
    }

    template <class PropertyMap>
    struct dispatch_access
    {
        typedef PythonPropertyMap<PropertyMap> pmap_t;

        template <class Graph, class PClass, class ReturnPolicy>
        void operator()(Graph*, PClass& pclass, ReturnPolicy return_policy) const
        {
            pclass
                .def("__getitem__", &pmap_t::template get_value<PythonVertex<Graph>>,
                     return_policy)
                .def("__setitem__", &pmap_t::template set_value<PythonVertex<Graph>>);
        }
    };
};

struct export_edge_property_map
{
    template <class PropertyMap>
    struct dispatch_access
    {
        typedef PythonPropertyMap<PropertyMap> pmap_t;
        template <class Graph, class PClass, class ReturnPolicy>
        void operator()(Graph*, PClass& pclass, ReturnPolicy return_policy) const
        {
            pclass
                .def("__getitem__",
                     &pmap_t::template get_value<PythonEdge<Graph> >,
                     return_policy)
                .def("__setitem__",
                     &pmap_t::template set_value<PythonEdge<Graph> >);
        }
    };

    template <class PropertyMap>
    void operator()(PropertyMap) const
    {
        typedef PythonPropertyMap<PropertyMap> pmap_t;

        string type_name;
        if (std::is_same<typename boost::mpl::find<value_types,
                                                   typename pmap_t::value_type>::type,
                         typename boost::mpl::end<value_types>::type>::value)
            type_name =
                name_demangle(typeid(typename pmap_t::value_type).name());
        else
            type_name =
                type_names[boost::mpl::find<value_types,typename pmap_t::value_type>
                           ::type::pos::value];
        string class_name = "EdgePropertyMap<" + type_name + ">";

        typedef typename boost::mpl::if_<
            typename return_reference::apply<typename pmap_t::value_type>::type,
            boost::python::return_internal_reference<>,
            boost::python::return_value_policy<boost::python::return_by_value> >
            ::type return_policy;

        boost::python::class_<pmap_t> pclass(class_name.c_str(),
                                             boost::python::no_init);
        pclass.def("__hash__", &pmap_t::get_hash)
            .def("value_type", &pmap_t::get_type)
            .def("get_map", &pmap_t::get_map)
            .def("get_dynamic_map", &pmap_t::get_dynamic_map)
            .def("get_array", &pmap_t::get_array)
            .def("is_writable", &pmap_t::is_writable)
            .def("reserve", &pmap_t::reserve)
            .def("resize", &pmap_t::resize)
            .def("shrink_to_fit", &pmap_t::shrink_to_fit)
            .def("data_ptr", &pmap_t::data_ptr);


        typedef boost::mpl::transform<graph_tool::all_graph_views,
                                      boost::mpl::quote1<std::add_const> >::type const_graph_views;
        typedef boost::mpl::transform<graph_tool::all_graph_views,
                                      boost::mpl::quote1<std::add_pointer> >::type all_graph_views;
        typedef boost::mpl::transform<const_graph_views,
                                      boost::mpl::quote1<std::add_pointer> >::type all_const_graph_views;
        typedef boost::mpl::joint_view<all_graph_views, all_const_graph_views>::type graph_views;

        boost::mpl::for_each<graph_views>(std::bind(dispatch_access<PropertyMap>(),
                                                    std::placeholders::_1,
                                                    std::ref(pclass), return_policy()));
    }
};

struct export_graph_property_map
{
    template <class PropertyMap>
    void operator()(PropertyMap) const
    {
        typedef PythonPropertyMap<PropertyMap> pmap_t;

        string type_name =
            type_names[boost::mpl::find<value_types,
                       typename pmap_t::value_type>::type::pos::value];
        string class_name = "GraphPropertyMap<" + type_name + ">";

        typedef typename boost::mpl::if_<
            typename return_reference::apply<typename pmap_t::value_type>::type,
            boost::python::return_internal_reference<>,
            boost::python::return_value_policy<boost::python::return_by_value> >
            ::type return_policy;

        boost::python::class_<pmap_t> pclass(class_name.c_str(),
                                             boost::python::no_init);
        pclass.def("__hash__", &pmap_t::get_hash)
            .def("value_type", &pmap_t::get_type)
            .def("__getitem__", &pmap_t::template get_value<GraphInterface>,
                 return_policy())
            .def("__setitem__", &pmap_t::template set_value<GraphInterface>)
            .def("get_map", &pmap_t::get_map)
            .def("get_dynamic_map", &pmap_t::get_dynamic_map)
            .def("get_array", &pmap_t::get_array)
            .def("is_writable", &pmap_t::is_writable)
            .def("reserve", &pmap_t::reserve)
            .def("resize", &pmap_t::resize)
            .def("shrink_to_fit", &pmap_t::shrink_to_fit);
    }
};

void export_python_properties()
{
    typedef property_map_types::apply<
            value_types,
            GraphInterface::vertex_index_map_t,
            boost::mpl::bool_<true>
        >::type vertex_property_maps;
    typedef property_map_types::apply<
            value_types,
            GraphInterface::edge_index_map_t,
            boost::mpl::bool_<true>
        >::type edge_property_maps;
    typedef property_map_types::apply<
            value_types,
            ConstantPropertyMap<size_t,graph_property_tag>,
            boost::mpl::bool_<false>
        >::type graph_property_maps;

    boost::mpl::for_each<vertex_property_maps>(export_vertex_property_map());
    boost::mpl::for_each<edge_property_maps>(export_edge_property_map());
    boost::mpl::for_each<graph_property_maps>(export_graph_property_map());
}

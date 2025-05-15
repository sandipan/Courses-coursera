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

#ifndef GRAPH_HH
#define GRAPH_HH
#include "config.h"

#include <Python.h>
#include <boost/python/object.hpp>
#include <boost/python/dict.hpp>

#include <deque>

#include "graph_adjacency.hh"

#include <boost/graph/graph_traits.hpp>

#include "fast_vector_property_map.hh"
#include <boost/variant.hpp>
#include <boost/mpl/vector.hpp>
#include "graph_properties.hh"
#include "graph_exceptions.hh"

namespace graph_tool
{

// GraphInterface
// this class is the main interface to the internally kept graph. This is how
// the external world will manipulate the graph. All the algorithms should be
// registered here. This class will be exported to python in graph_bind.hh

namespace detail
{
// Generic graph_action functor. See graph_filtering.hh for details.
template <class Action, class GraphViews, class Wrap = boost::mpl::false_,
          class... TRS>
struct graph_action;
}

class GraphInterface
{
public:
    GraphInterface();
    GraphInterface(const GraphInterface& g, bool keep_ref,
                   boost::python::object ovprops, boost::python::object oeprops,
                   boost::python::object vorder);
    ~GraphInterface();

    // useful enums

    typedef enum
    {
        IN_DEGREE,
        OUT_DEGREE,
        TOTAL_DEGREE
    } degree_t;

    // general "degree" type, i.e., either a degree_t above or a string
    // representing a scalar vertex property
    typedef boost::variant<degree_t, boost::any> deg_t;

    //
    // Basic manipulation
    //

    size_t get_num_vertices(bool filtered = true);
    size_t get_num_edges(bool filtered = true);
    void set_directed(bool directed) {_directed = directed;}
    bool get_directed() {return _directed;}
    void set_reversed(bool reversed) {_reversed = reversed;}
    bool get_reversed() {return _reversed;}
    void set_keep_epos(bool keep) {_mg->set_keep_epos(keep);}
    bool get_keep_epos() {return _mg->get_keep_epos();}


    // graph filtering
    void set_vertex_filter_property(boost::any prop, bool invert);
    bool is_vertex_filter_active() const;
    void set_edge_filter_property(boost::any prop, bool invert);
    bool is_edge_filter_active() const;

    // graph modification
    void re_index_edges();
    void purge_vertices(boost::any old_index); // removes filtered vertices
    void purge_edges();    // removes filtered edges
    void clear();
    void clear_edges();
    void shift_vertex_property(boost::any map, boost::python::object oindex) const;
    void move_vertex_property(boost::any map, boost::python::object oindex) const;
    void re_index_vertex_property(boost::any map, boost::any old_index) const;
    void copy_vertex_property(const GraphInterface& src, boost::any prop_src,
                              boost::any prop_tgt);
    void copy_edge_property(const GraphInterface& src, boost::any prop_src,
                            boost::any prop_tgt);
    void shrink_to_fit() { _mg->shrink_to_fit(); }

    //
    // python interface
    //
    boost::python::object degree_map(std::string deg, boost::any weight) const;

    // used for graph properties
    boost::graph_property_tag get_descriptor() const { return boost::graph_property_tag(); }
    bool check_valid() const {return true;}

    // I/O
    void write_to_file(std::string s, boost::python::object pf, std::string format,
                       boost::python::list properties);
    boost::python::tuple read_from_file(std::string s, boost::python::object pf,
                                        std::string format,
                                        boost::python::list ignore_vp,
                                        boost::python::list ignore_ep,
                                        boost::python::list ignore_gp);

    //
    // Internal types
    //

    typedef boost::adj_list<size_t> multigraph_t;
    typedef boost::graph_traits<multigraph_t>::vertex_descriptor vertex_t;
    typedef boost::graph_traits<multigraph_t>::edge_descriptor edge_t;

    typedef boost::property_map<multigraph_t, boost::vertex_index_t>::type vertex_index_map_t;
    typedef boost::property_map<multigraph_t, boost::edge_index_t>::type edge_index_map_t;
    typedef ConstantPropertyMap<size_t,boost::graph_property_tag> graph_index_map_t;

    // internal access

    multigraph_t&      get_graph() {return *_mg;}
    std::shared_ptr<multigraph_t> get_graph_ptr() {return _mg;}
    vertex_index_map_t get_vertex_index()   {return _vertex_index;}
    edge_index_map_t   get_edge_index()     {return _edge_index;}
    size_t             get_edge_index_range() {return _mg->get_edge_index_range();}

    graph_index_map_t  get_graph_index()  {return graph_index_map_t(0);}

    // Gets the encapsulated graph view. See graph_filtering.cc for details
    boost::any get_graph_view() const;
    std::vector<boost::any>& get_graph_views() {return _graph_views;}

private:

    // Generic graph_action functor. See graph_filtering.hh for details.
    template <class Action, class GraphViews, class Wrap, class... TRS>
    friend struct detail::graph_action;

    // this is the main graph
    std::shared_ptr<multigraph_t> _mg;

    // vertex index map
    vertex_index_map_t _vertex_index;

    // edge index map
    edge_index_map_t _edge_index;

    // this will hold an instance of the graph views at run time
    std::vector<boost::any> _graph_views;

    // reverse and directed states
    bool _reversed;
    bool _directed;

    // graph index map
    graph_index_map_t _graph_index;

    // vertex filter
    typedef boost::unchecked_vector_property_map<uint8_t,vertex_index_map_t>
        vertex_filter_t;
    vertex_filter_t _vertex_filter_map;
    bool _vertex_filter_invert;
    bool _vertex_filter_active;

    // edge filter
    typedef boost::unchecked_vector_property_map<uint8_t,edge_index_map_t>
        edge_filter_t;
    edge_filter_t _edge_filter_map;
    bool _edge_filter_invert;
    bool _edge_filter_active;
};

// convenience metafunctions to get property map types

template <class ValType>
struct eprop_map_t
{
    typedef typename property_map_type::apply<ValType,
                                              GraphInterface::edge_index_map_t>::type
        type;
};

template <class ValType>
struct vprop_map_t
{
    typedef typename property_map_type::apply<ValType,
                                              GraphInterface::vertex_index_map_t>::type
        type;
};

template <class ValType>
struct gprop_map_t
{
    typedef typename property_map_type::apply<ValType,
                                              GraphInterface::graph_index_map_t>::type
        type;
};


} //namespace graph_tool

#endif

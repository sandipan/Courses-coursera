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

#ifndef GRAPH_ADAPTOR_HH
#define GRAPH_ADAPTOR_HH

#include <list>

#include <boost/config.hpp>
#include <boost/iterator_adaptors.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/properties.hpp>

#include "transform_iterator.hh"

namespace boost {

//==============================================================================
// undirected_adaptor
// This class encapsulates a directed graph with parallel edges and provides a
// view of the graph as undirected with parallel edges.
//==============================================================================
template <class Graph> class undirected_adaptor
{
public:
    undirected_adaptor(const Graph& g) : _g(const_cast<Graph&>(g)){}

    typedef typename vertex_property_type<Graph>::type vertex_property_type;
    typedef typename edge_property_type<Graph>::type edge_property_type;
    typedef typename Graph::graph_tag graph_tag;
    typedef Graph graph_type;

    typedef Graph original_graph_t;

    typedef typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor
        vertex_descriptor;
    typedef typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor
        edge_descriptor;

    typedef undirected_tag directed_category;
    typedef allow_parallel_edge_tag edge_parallel_category;
    typedef typename graph_traits<Graph>::traversal_category traversal_category;

    typedef typename Graph::out_edge_iterator all_edge_iterator;
    typedef typename Graph::out_edge_iterator all_edge_iterator_reversed;

    const Graph& original_graph() const {return _g;}
    Graph& original_graph() {return _g;}

    static vertex_descriptor null_vertex() {graph_traits<Graph>::null_vertex();}

private:
    Graph& _g;
};

template <class Graph>
struct get_iterator_category
{
    typedef typename graph_traits<Graph>::out_edge_iterator iter_t;
    typedef typename std::iterator_traits<iter_t>::iterator_category type;
};


//==============================================================================
// graph_traits<undirected_adaptor>
// this defines all the necessary types associated with undirected_adaptor
//==============================================================================
template <class Graph>
struct graph_traits<undirected_adaptor<Graph> > {
    typedef typename graph_traits<Graph>::vertex_descriptor vertex_descriptor;
    typedef typename graph_traits<Graph>::edge_descriptor edge_descriptor;

    typedef typename graph_traits<Graph>::adjacency_iterator adjacency_iterator;
    typedef typename graph_traits<Graph>::out_edge_iterator out_edge_iterator;
    typedef typename graph_traits<Graph>::in_edge_iterator in_edge_iterator;
    typedef typename graph_traits<Graph>::vertex_iterator vertex_iterator;
    typedef typename graph_traits<Graph>::edge_iterator edge_iterator;


    typedef undirected_tag directed_category;
    typedef allow_parallel_edge_tag edge_parallel_category;
    typedef typename graph_traits<Graph>::traversal_category traversal_category;
    typedef typename graph_traits<Graph>::vertices_size_type vertices_size_type;
    typedef typename graph_traits<Graph>::edges_size_type edges_size_type;
    typedef typename graph_traits<Graph>::degree_size_type degree_size_type;

    static vertex_descriptor null_vertex()
    {
        return graph_traits<Graph>::null_vertex();
    }

private:
    typedef is_convertible<typename std::iterator_traits<typename graph_traits<Graph>::out_edge_iterator>::iterator_category,
                           std::random_access_iterator_tag> is_orig_ra;
    typedef is_convertible<typename std::iterator_traits<out_edge_iterator>::iterator_category,
                           std::random_access_iterator_tag> is_ra;
    BOOST_STATIC_ASSERT((!is_orig_ra::value || is_ra::value));
};

template <class Graph>
struct graph_traits< const undirected_adaptor<Graph> >:
    public graph_traits<undirected_adaptor<Graph> > {};

//==============================================================================
// Nonmember functions
// these provide manipulation of the graph
//==============================================================================

//==============================================================================
// source(e,g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
source(const typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor& e,
       const undirected_adaptor<Graph>& g)
{
    return source(e, g.original_graph());
}

//==============================================================================
// target(e,g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
target(const typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor& e,
       const undirected_adaptor<Graph>& g)
{
    return target(e, g.original_graph());
}

//==============================================================================
// vertex(n,g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
vertex(typename graph_traits<undirected_adaptor<Graph> >::vertices_size_type n,
       const undirected_adaptor<Graph>& g)
{
    return vertex(n, g.original_graph());
}

//==============================================================================
// vertices(g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
vertices(const undirected_adaptor<Graph>& g)
{
    return vertices(g.original_graph());
}

//==============================================================================
// edges(g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
edges(const undirected_adaptor<Graph>& g)
{
    return edges(g.original_graph());
}

//==============================================================================
// edge(u, v, g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
edge(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
     typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
     const undirected_adaptor<Graph>& g)
{
    auto res = edge(u, v, g.original_graph());

    if (!res.second)
    {
        res = edge(v, u, g.original_graph());
        std::swap(res.first.s, res.first.t);
    }

    return res;
}

//==============================================================================
// out_edges(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
out_edges(typename graph_traits<undirected_adaptor<Graph>>::vertex_descriptor u,
          const undirected_adaptor<Graph>& g)
{
    return _all_edges_out(u, g.original_graph());
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
_all_edges_out(typename graph_traits<undirected_adaptor<Graph>>::vertex_descriptor u,
               const undirected_adaptor<Graph>& g)
{
    return out_edges(u, g);
}

//==============================================================================
// in_edges(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
in_edges(typename graph_traits<undirected_adaptor<Graph>>::vertex_descriptor u,
         const undirected_adaptor<Graph>& g)
{
    return _all_edges_in(u, g.original_graph());
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
all_edges(typename graph_traits<undirected_adaptor<Graph>>::vertex_descriptor u,
          const undirected_adaptor<Graph>& g)
{
    return out_edges(u, g);
}

//==============================================================================
// out_neighbours(u, g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
out_neighbours(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
               const undirected_adaptor<Graph>& g)
{
    return all_neighbours(u, g.original_graph());
}

//==============================================================================
// in_neighbours(u, g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
in_neighbours(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
              const undirected_adaptor<Graph>& g)
{
    return out_neighbours(u, g);
}

//==============================================================================
// all_neighbours(u, g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
all_neighbours(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
               const undirected_adaptor<Graph>& g)
{
    return out_neighbours(u, g);
}

//==============================================================================
// adjacent_vertices(u,g)
//==============================================================================
template <class Graph>
inline  __attribute__((always_inline)) __attribute__((flatten))
auto
adjacent_vertices
    (typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
     const undirected_adaptor<Graph>& g)
{
    return out_neighbours(u, g);
}

//==============================================================================
// num_vertices(g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
num_vertices(const undirected_adaptor<Graph>& g)
{
    return num_vertices(g.original_graph());
}

//==============================================================================
// num_edges(g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
num_edges(const undirected_adaptor<Graph>& g)
{
    return num_edges(g.original_graph());
}

//==============================================================================
// out_degree(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
out_degree(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
           const undirected_adaptor<Graph>& g)
{
    return degree(u, g.original_graph());
}

//==============================================================================
// in_degree(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
in_degree(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
          const undirected_adaptor<Graph>& g)
{
    return out_degree(u, g);
}

//==============================================================================
// degree(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto
degree(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
       const undirected_adaptor<Graph>& g)
{
    return out_degree(u, g);
}


//==============================================================================
// add_vertex(g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
auto
add_vertex(undirected_adaptor<Graph>& g)
{
    return add_vertex(g.original_graph());
}

//==============================================================================
// add_vertex(vp,g)
//==============================================================================
template <class Graph, class VertexProperties>
inline __attribute__((always_inline))
auto
add_vertex(const VertexProperties& p, undirected_adaptor<Graph>& g)
{
    return add_vertex(p, g.original_graph());
}

//==============================================================================
// clear_vertex(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
void clear_vertex(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
                  undirected_adaptor<Graph>& g)
{
    clear_vertex(u, g.original_graph());
}

//==============================================================================
// clear_vertex(u,g,pred)
//==============================================================================
template <class Graph, class Pred>
inline __attribute__((always_inline))
void clear_vertex(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
                  undirected_adaptor<Graph>& g, Pred&& pred)
{
    clear_vertex(u, g.original_graph(), pred);
}

//==============================================================================
// remove_vertex(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
void remove_vertex(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
                   undirected_adaptor<Graph>& g)
{
    remove_vertex(u, g.original_graph());
}

//==============================================================================
// remove_vertex_fast(u,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
void remove_vertex_fast(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
                        undirected_adaptor<Graph>& g)
{
    remove_vertex_fast(u, g.original_graph());
}

//==============================================================================
// add_edge(u,v,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
std::pair<typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor,
          bool>
add_edge(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
         typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
         undirected_adaptor<Graph>& g)
{
    return add_edge(u, v, g.original_graph());
}

//==============================================================================
// add_edge(u,v,ep,g)
//==============================================================================
template <class Graph, class EdgeProperties>
inline __attribute__((always_inline))
auto
add_edge(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
         typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
         const EdgeProperties& ep, undirected_adaptor<Graph>& g)
{
    return add_edge(u, v, ep, g.original_graph());
}

//==============================================================================
// remove_edge(u,v,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
void remove_edge(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor u,
                 typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
                 undirected_adaptor<Graph>& g)
{
    auto e = edge(u, v, g);
    if (e.second)
        remove_edge(e.first, g);
}

//==============================================================================
// remove_edge(e,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
void remove_edge(typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor e,
                 undirected_adaptor<Graph>& g)
{
    auto& u = g.original_graph();
    remove_edge(e, u);
    std::swap(e.s, e.t);
    remove_edge(e, u);
}

//==============================================================================
// remove_edge(e_iter,g)
//==============================================================================
template <class Graph>
inline __attribute__((always_inline))
void remove_edge(const typename graph_traits<undirected_adaptor<Graph> >::out_edge_iterator& iter,
                 undirected_adaptor<Graph>& g)
{
    remove_edge(*iter, g);
}

//==============================================================================
// remove_out_edge_if(v,predicate,g)
//==============================================================================
template <class Graph, class Predicate>
inline
void remove_out_edge_if(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
                        Predicate predicate, undirected_adaptor<Graph>& g)
{
    std::vector<typename undirected_adaptor<Graph>::EdgeDescriptor> removed_edges;
    auto edge_range = out_edges(v,g);
    for(auto iter = edge_range.first; iter != edge_range.second; ++iter)
        if (predicate(*iter))
            removed_edges.push_back(*iter);
    for(auto& e : removed_edges)
        remove_edge(e, g);
}

//==============================================================================
// remove_in_edge_if(v,predicate,g)
//==============================================================================
template <class Graph, class Predicate>
inline
void remove_in_edge_if(typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
                       Predicate predicate, undirected_adaptor<Graph>& g)
{
    std::vector<typename undirected_adaptor<Graph>::EdgeDescriptor> removed_edges;
    auto edge_range = in_edges(v,g);
    for(auto iter = edge_range.first; iter != edge_range.second; ++iter)
        if (predicate(*iter))
            removed_edges.push_back(*iter);
    for(auto& e : removed_edges)
        remove_edge(e, g);
}


//==============================================================================
// Property maps
//==============================================================================

//==============================================================================
// vertex_property<undirected_adaptor>
//==============================================================================
template <class Graph>
class vertex_property<undirected_adaptor<Graph> >
{
public:
    typedef typename vertex_property<Graph>::type type;
};

//==============================================================================
// vertex_property_type<undirected_adaptor>
//==============================================================================
template <class Graph>
class vertex_property_type<undirected_adaptor<Graph> >
{
public:
    typedef typename vertex_property_type<Graph>::type type;
};

//==============================================================================
// edge_property<undirected_adaptor>
//==============================================================================
template <class Graph>
class edge_property<undirected_adaptor<Graph> >
{
public:
    typedef typename edge_property<Graph>::type type;
};

//==============================================================================
// edge_property_type<undirected_adaptor>
//==============================================================================
template <class Graph>
class edge_property_type<undirected_adaptor<Graph> >
{
public:
    typedef typename edge_property_type<Graph>::type type;
};

//==============================================================================
// property_map<UndirecterdAdaptor, PropertyTag>
//==============================================================================
template <class Graph, class PropertyTag>
class property_map<undirected_adaptor<Graph>, PropertyTag>
{
public:
    typedef typename property_map<Graph, PropertyTag>::type type;
    typedef typename property_map<Graph, PropertyTag>::const_type const_type;
};

//==============================================================================
// property_map<undirected_adaptor, T Bundle::*>
//==============================================================================
template <typename Graph, typename T, typename Bundle>
class property_map<undirected_adaptor<Graph>, T Bundle::*>
{
public:
    typedef typename property_map<Graph, T Bundle::*>::type type;
    typedef typename property_map<Graph, T Bundle::*>::const_type const_type;
};


//==============================================================================
// get(tag,g)
//==============================================================================
template <class PropertyTag, class Graph>
inline
typename property_map<undirected_adaptor<Graph>, PropertyTag>::type
get(PropertyTag tag, undirected_adaptor<Graph>& g)
{
    return get(tag, g.original_graph());
}

//==============================================================================
// const get(tag,g)
//==============================================================================
template <class PropertyTag, class Graph>
inline
typename property_map<undirected_adaptor<Graph>, PropertyTag>::const_type
get(PropertyTag tag, const undirected_adaptor<Graph>& g)
{
    return get(tag, g.original_graph());
}

//==============================================================================
// get(tag,g,v)
//==============================================================================
template <class PropertyTag, class Graph>
inline
typename property_traits
    <typename property_map<undirected_adaptor<Graph>,
                           PropertyTag>::const_type >::value_type
get(PropertyTag tag, const undirected_adaptor<Graph>& g,
    typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v)
{
    return get(tag, g.original_graph(), v);
}

//==============================================================================
// get(tag,g,e)
//==============================================================================
template <class PropertyTag, class Graph>
inline
typename property_traits
    <typename property_map<undirected_adaptor<Graph>,
                           PropertyTag>::const_type >::value_type
get(PropertyTag tag, const undirected_adaptor<Graph>& g,
    const typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor& e)
{
    return get(tag, g.original_graph(), e);
}

//==============================================================================
// put(tag, g, v, value)
//==============================================================================
template <class Graph, class PropertyTag, class Value>
inline
void put(PropertyTag tag, undirected_adaptor<Graph>& g,
         typename graph_traits<undirected_adaptor<Graph> >::vertex_descriptor v,
         const Value& value)
{
    put(tag, g.original_graph(), v, value);
}

//==============================================================================
// put(tag, g, e, value)
//==============================================================================
template <class Graph, class PropertyTag, class X, class Value>
inline
void put(PropertyTag tag, const undirected_adaptor<Graph>& g,
         const typename graph_traits<undirected_adaptor<Graph> >::edge_descriptor& e,
         const Value &value)
{
    put(tag, g.original_graph(), e, value);
}

//==============================================================================
// get_property(g,tag)
//==============================================================================
template <class Graph, class GraphProperties, class GraphPropertyTag>
inline
typename property_value<GraphProperties, GraphPropertyTag>::type&
get_property(undirected_adaptor<Graph>& g, GraphPropertyTag tag)
{
    get_property(g.original_graph(), tag);
}

//==============================================================================
// const get_property(g,tag)
//==============================================================================
template <class Graph, class GraphProperties, class GraphPropertyTag>
inline
const typename property_value<GraphProperties, GraphPropertyTag>::type&
get_property(const undirected_adaptor<Graph>& g, GraphPropertyTag tag)
{
    get_property(g.original_graph(), tag);
}

} // namespace boost


#endif // GRAPH_ADAPTOR_HH

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

//  (C) Copyright David Abrahams 2000.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef GRAPH_REVERSE
# define GRAPH_REVERSE

#include <boost/graph/adjacency_iterator.hpp>
#include <boost/graph/properties.hpp>
#include <boost/iterator/transform_iterator.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/type_traits.hpp>
#include <boost/mpl/if.hpp>
#include <functional>

#if BOOST_WORKAROUND(BOOST_MSVC, < 1300)
// Stay out of the way of the concept checking class
# define BidirectionalGraph BidirectionalGraph_
#endif

namespace boost {

struct reversed_graph_tag { };

template <class BidirectionalGraph, class GraphRef = const BidirectionalGraph&>
class reversed_graph {
    typedef reversed_graph<BidirectionalGraph, GraphRef> Self;
    typedef graph_traits<BidirectionalGraph> Traits;
 public:
    typedef BidirectionalGraph base_type;

    // Constructor
    reversed_graph(GraphRef g) : _g(g) {}

    // Graph requirements
    typedef typename Traits::vertex_descriptor vertex_descriptor;
    typedef typename Traits::edge_descriptor edge_descriptor;
    typedef typename Traits::directed_category directed_category;
    typedef typename Traits::edge_parallel_category edge_parallel_category;
    typedef typename Traits::traversal_category traversal_category;

    // IncidenceGraph requirements
    typedef typename Traits::in_edge_iterator out_edge_iterator;
    typedef typename Traits::degree_size_type degree_size_type;

    // BidirectionalGraph requirements
    typedef typename Traits::out_edge_iterator in_edge_iterator;

    typedef typename BidirectionalGraph::all_edge_iterator_reversed all_edge_iterator;
    typedef typename BidirectionalGraph::all_edge_iterator all_edge_iterator_reversed;

    // AdjacencyGraph requirements
    typedef typename BidirectionalGraph::in_adjacency_iterator adjacency_iterator;
    typedef typename graph_traits<BidirectionalGraph>::adjacency_iterator in_adjacency_iterator;

    // VertexListGraph requirements
    typedef typename Traits::vertex_iterator vertex_iterator;

    // EdgeListGraph requirements
    typedef typename Traits::edge_iterator edge_iterator;
    typedef typename Traits::vertices_size_type vertices_size_type;
    typedef typename Traits::edges_size_type edges_size_type;

    typedef reversed_graph_tag graph_tag;

    static vertex_descriptor null_vertex()
    { return Traits::null_vertex(); }

    // would be private, but template friends aren't portable enough.
 // private:
    GraphRef _g;
};


// These are separate so they are not instantiated unless used (see bug 1021)
template <class BidirectionalGraph, class GraphRef>
struct vertex_property_type<reversed_graph<BidirectionalGraph, GraphRef> > {
    typedef typename boost::vertex_property_type<BidirectionalGraph>::type type;
};

template <class BidirectionalGraph, class GraphRef>
struct edge_property_type<reversed_graph<BidirectionalGraph, GraphRef> > {
    typedef typename boost::edge_property_type<BidirectionalGraph>::type type;
};

template <class BidirectionalGraph, class GraphRef>
struct graph_property_type<reversed_graph<BidirectionalGraph, GraphRef> > {
    typedef typename boost::graph_property_type<BidirectionalGraph>::type type;
};

template <class BidirectionalGraph>
inline reversed_graph<BidirectionalGraph>
make_reversed_graph(const BidirectionalGraph& g)
{
    return reversed_graph<BidirectionalGraph>(g);
}

template <class BidirectionalGraph>
inline reversed_graph<BidirectionalGraph, BidirectionalGraph&>
make_reversed_graph(BidirectionalGraph& g)
{
    return reversed_graph<BidirectionalGraph, BidirectionalGraph&>(g);
}

template <class BidirectionalGraph, class GRef>
std::pair<typename reversed_graph<BidirectionalGraph>::vertex_iterator,
          typename reversed_graph<BidirectionalGraph>::vertex_iterator>
vertices(const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return vertices(g._g);
}

template <class BidirectionalGraph, class GRef>
std::pair<typename reversed_graph<BidirectionalGraph>::edge_iterator,
          typename reversed_graph<BidirectionalGraph>::edge_iterator>
edges(const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return edges(g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph>::out_edge_iterator,
                 typename reversed_graph<BidirectionalGraph>::out_edge_iterator>
out_edges(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
          const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return in_edges(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::vertices_size_type
num_vertices(const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return num_vertices(g._g);
}

template <class BidirectionalGraph, class GRef>
inline typename reversed_graph<BidirectionalGraph>::edges_size_type
num_edges(const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return num_edges(g._g);
}

template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::degree_size_type
out_degree(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
           const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return in_degree(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::vertex_descriptor
vertex(const typename graph_traits<BidirectionalGraph>::vertices_size_type v,
       const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return vertex(v, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph>::edge_descriptor,
                 bool>
edge(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
     const typename graph_traits<BidirectionalGraph>::vertex_descriptor v,
     const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return edge(v, u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph>::in_edge_iterator,
                 typename reversed_graph<BidirectionalGraph>::in_edge_iterator>
in_edges(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
         const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return out_edges(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph>::all_edge_iterator,
                 typename reversed_graph<BidirectionalGraph>::all_edge_iterator>
all_edges(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
          const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return _all_edges_reversed(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph,GRef>::adjacency_iterator,
                 typename reversed_graph<BidirectionalGraph,GRef>::adjacency_iterator>
out_neighbours(typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
               const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return in_neighbours(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph,GRef>::in_adjacency_iterator,
                 typename reversed_graph<BidirectionalGraph,GRef>::in_adjacency_iterator>
in_neighbours(typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
              const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return out_neighbours(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph,GRef>::adjacency_iterator,
                 typename reversed_graph<BidirectionalGraph,GRef>::adjacency_iterator>
all_neighbours(typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
               const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return all_neighbours(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph,GRef>::adjacency_iterator,
                 typename reversed_graph<BidirectionalGraph,GRef>::adjacency_iterator>
adjacent_vertices(typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
                  const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return out_neighbours(u, g);
}


template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::degree_size_type
in_degree(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
          const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return out_degree(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::degree_size_type
degree(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
       const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return degree(u, g._g);
}


template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::vertex_descriptor
source(const typename reversed_graph<BidirectionalGraph,GRef>::edge_descriptor& e,
       const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return target(e, g._g);
}

template <class BidirectionalGraph, class GRef>
inline typename graph_traits<BidirectionalGraph>::vertex_descriptor
target(const typename reversed_graph<BidirectionalGraph,GRef>::edge_descriptor& e,
       const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return source(e, g._g);
}

template <class BidirectionalGraph, class GRef>
inline
typename graph_traits<reversed_graph<BidirectionalGraph,GRef>>::vertex_descriptor
vertex(size_t i, const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return vertex(i, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph,GRef>::out_edge_iterator,
                 typename reversed_graph<BidirectionalGraph,GRef>::out_edge_iterator>
_all_edges_out(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
               const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return _all_edges_in(u, g._g);
}

template <class BidirectionalGraph, class GRef>
inline std::pair<typename reversed_graph<BidirectionalGraph,GRef>::in_edge_iterator,
                 typename reversed_graph<BidirectionalGraph,GRef>::in_edge_iterator>
_all_edges_in(const typename graph_traits<BidirectionalGraph>::vertex_descriptor u,
               const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return _all_edges_out(u, g._g);
}

template <class BidirectionalGraph, class GRef, class Pred>
inline void
clear_vertex(typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
                ::vertex_descriptor v,
             reversed_graph<BidirectionalGraph,GRef>& g, Pred&& pred)
{
    clear_vertex(v, const_cast<BidirectionalGraph&>(g._g), pred);
}

template <class BidirectionalGraph, class GRef>
inline
std::pair<typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
             ::edge_descriptor,bool>
add_edge(typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
             ::vertex_descriptor u,
         typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
             ::vertex_descriptor v,
         reversed_graph<BidirectionalGraph,GRef>& g)
{
    typedef typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
           ::edge_descriptor e_t;
    std::pair<typename boost::graph_traits<BidirectionalGraph>::edge_descriptor,
              bool> ret =
        add_edge(v, u, const_cast<BidirectionalGraph&>(g._g)); // insert reversed
    return std::make_pair(e_t(ret.first), ret.second);
}

template <class BidirectionalGraph, class GRef>
inline
void remove_edge(typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
                    ::edge_descriptor e,
                 reversed_graph<BidirectionalGraph,GRef>& g)
{
    return remove_edge(e,const_cast<BidirectionalGraph&>(g._g));
}

template <class BidirectionalGraph, class GRef>
inline
void remove_vertex(typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
                      ::vertex_descriptor v,
                   reversed_graph<BidirectionalGraph,GRef>& g)
{
    return remove_vertex(v,const_cast<BidirectionalGraph&>(g._g));
}

template <class BidirectionalGraph, class GRef>
inline
void remove_vertex_fast(typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
                            ::vertex_descriptor v,
                        reversed_graph<BidirectionalGraph,GRef>& g)
{
    return remove_vertex_fast(v,const_cast<BidirectionalGraph&>(g._g));
}

template <class BidirectionalGraph, class GRef>
inline
void clear_vertex(typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
                     ::vertex_descriptor v,
                  reversed_graph<BidirectionalGraph,GRef>& g)
{
    return clear_vertex(v,const_cast<BidirectionalGraph&>(g._g));
}

template <class BidirectionalGraph, class GRef>
inline
typename boost::graph_traits<reversed_graph<BidirectionalGraph,GRef>>
   ::vertex_descriptor
add_vertex(reversed_graph<BidirectionalGraph,GRef>& g)
{
    return add_vertex(const_cast<BidirectionalGraph&>(g._g));
}

//========================================================================
// Vertex and edge index property maps
//========================================================================

template <class BidirectionalGraph, class GRef, class Tag>
struct property_map<reversed_graph<BidirectionalGraph,GRef>, Tag>
{
    typedef typename property_map<BidirectionalGraph,Tag>::type type;
    typedef typename property_map<BidirectionalGraph,Tag>::const_type const_type;
};

template <class BidirectionalGraph, class GRef, class Tag>
struct property_map<const reversed_graph<BidirectionalGraph,GRef>, Tag>
{
    typedef typename property_map<const BidirectionalGraph,Tag>::type type;
    typedef typename property_map<const BidirectionalGraph,Tag>::const_type
        const_type;
};

template <class BidirectionalGraph, class GRef, class Tag>
inline auto
get(Tag t, reversed_graph<BidirectionalGraph,GRef>& g)
{
    return get(t, g._g);
}

template <class BidirectionalGraph, class GRef, class Tag>
inline auto
get(Tag t, const reversed_graph<BidirectionalGraph,GRef>& g)
{
    return get(t, g._g);
}

} // namespace boost

#endif

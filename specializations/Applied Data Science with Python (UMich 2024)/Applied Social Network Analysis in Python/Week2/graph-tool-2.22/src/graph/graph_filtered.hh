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

//=======================================================================
// Copyright 1997, 1998, 1999, 2000 University of Notre Dame.
// Authors: Andrew Lumsdaine, Lie-Quan Lee, Jeremy G. Siek
//
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//=======================================================================

#ifndef GRAPH_FILTERED_HH
#define GRAPH_FILTERED_HH

#include <boost/graph/graph_traits.hpp>
#include <boost/graph/properties.hpp>
#include <boost/graph/adjacency_iterator.hpp>
#include <boost/graph/detail/set_adaptor.hpp>
#include <boost/iterator/filter_iterator.hpp>
#include <boost/graph/filtered_graph.hpp> // for predicate classes

namespace boost {

namespace detail {

    template <typename EdgePredicate, typename VertexPredicate, typename Graph>
    struct out_edge_pred
    {
        out_edge_pred() { }
        out_edge_pred(EdgePredicate ep, VertexPredicate vp,
                      const Graph& g)
            : _edge_pred(ep), _vertex_pred(vp), _g(&g) { }

        template <typename Edge>
        bool operator()(const Edge& e) const
        {
            return _edge_pred(e) && _vertex_pred(target(e, *_g));
        }
        EdgePredicate _edge_pred;
        VertexPredicate _vertex_pred;
        const Graph* _g;
    };

    template <typename EdgePredicate, typename VertexPredicate, typename Graph>
    struct in_edge_pred
    {
        in_edge_pred() { }
        in_edge_pred(EdgePredicate ep, VertexPredicate vp,
                     const Graph& g)
            : _edge_pred(ep), _vertex_pred(vp), _g(&g) { }

        template <typename Edge>
        bool operator()(const Edge& e) const
        {
            return _edge_pred(e) && _vertex_pred(source(e, *_g));
        }
        EdgePredicate _edge_pred;
        VertexPredicate _vertex_pred;
        const Graph* _g;
    };

    template <typename EdgePredicate, typename VertexPredicate, typename Graph>
    struct edge_pred
    {
        edge_pred() { }
        edge_pred(EdgePredicate ep, VertexPredicate vp,
                  const Graph& g)
            : _edge_pred(ep), _vertex_pred(vp), _g(&g) { }

        template <typename Edge>
        bool operator()(const Edge& e) const
        {
            return _edge_pred(e)
                && _vertex_pred(source(e, *_g)) && _vertex_pred(target(e, *_g));
        }
        EdgePredicate _edge_pred;
        VertexPredicate _vertex_pred;
        const Graph* _g;
    };

} // namespace detail


//===========================================================================
// Filtered Graph

struct filt_graph_tag { };

// This base class is a stupid hack to change overload resolution
// rules for the source and target functions so that they are a
// worse match than the source and target functions defined for
// pairs in graph_traits.hpp. I feel dirty. -JGS
template <class G>
struct filt_graph_base
{
  typedef graph_traits<G> Traits;
  typedef typename Traits::vertex_descriptor          vertex_descriptor;
  typedef typename Traits::edge_descriptor            edge_descriptor;
  filt_graph_base(const G& g) : _g(g) { }
  //protected:
  const G& _g;
};

template <typename Graph,
          typename EdgePredicate,
          typename VertexPredicate = keep_all>
class filt_graph : public filt_graph_base<Graph>
{
    typedef filt_graph_base<Graph> Base;
    typedef graph_traits<Graph> Traits;
    typedef filt_graph self;
public:
    typedef Graph graph_type;
    typedef detail::out_edge_pred<EdgePredicate, VertexPredicate,
                                  Graph> OutEdgePred;
    typedef detail::in_edge_pred<EdgePredicate, VertexPredicate,
                                 Graph> InEdgePred;
    typedef detail::edge_pred<EdgePredicate, VertexPredicate, Graph>
        EdgePred;

    // Constructors
    filt_graph(const Graph& g, EdgePredicate ep)
        : Base(g), _edge_pred(ep),
          _out_edge_pred(_edge_pred, _vertex_pred, g),
          _in_edge_pred(_edge_pred, _vertex_pred, g),
          _all_edge_pred(_edge_pred, _vertex_pred, g) {}

    filt_graph(const Graph& g, EdgePredicate ep, VertexPredicate vp)
        : Base(g), _edge_pred(ep), _vertex_pred(vp),
          _out_edge_pred(_edge_pred, _vertex_pred, g),
          _in_edge_pred(_edge_pred, _vertex_pred, g),
          _all_edge_pred(_edge_pred, _vertex_pred, g) {}

    // Graph requirements
    typedef typename Traits::vertex_descriptor          vertex_descriptor;
    typedef typename Traits::edge_descriptor            edge_descriptor;
    typedef typename Traits::directed_category          directed_category;
    typedef typename Traits::edge_parallel_category     edge_parallel_category;
    typedef typename Traits::traversal_category         traversal_category;

    // IncidenceGraph requirements
    typedef filter_iterator<
        OutEdgePred, typename Traits::out_edge_iterator
        > out_edge_iterator;

    typedef typename Traits::degree_size_type          degree_size_type;

    // AdjacencyGraph requirements
    typedef typename adjacency_iterator_generator<self,
                                                  vertex_descriptor,
                                                  out_edge_iterator>::type
        adjacency_iterator;


    // BidirectionalGraph requirements
    typedef filter_iterator<
        InEdgePred, typename Traits::in_edge_iterator
        > in_edge_iterator;

    typedef filter_iterator<
        EdgePred, typename Graph::all_edge_iterator
        > all_edge_iterator;

    typedef filter_iterator<
        EdgePred, typename Graph::all_edge_iterator_reversed
        > all_edge_iterator_reversed;

    typedef typename adjacency_iterator_generator<self,
                                                  vertex_descriptor,
                                                  in_edge_iterator>::type
       in_adjacency_iterator;

    // VertexListGraph requirements
    typedef filter_iterator<
        VertexPredicate, typename Traits::vertex_iterator
        > vertex_iterator;
    typedef typename Traits::vertices_size_type        vertices_size_type;

    // EdgeListGraph requirements
    typedef filter_iterator<
        EdgePred, typename Traits::edge_iterator
        > edge_iterator;
    typedef typename Traits::edges_size_type           edges_size_type;

    typedef filt_graph_tag graph_tag;

    static vertex_descriptor null_vertex()
    { return Traits::null_vertex(); }

    //private:
    EdgePredicate _edge_pred;
    VertexPredicate _vertex_pred;

    OutEdgePred _out_edge_pred;
    InEdgePred _in_edge_pred;
    EdgePred _all_edge_pred;
};

// Do not instantiate these unless needed
template <typename Graph,
          typename EdgePredicate,
          typename VertexPredicate>
struct vertex_property_type<filt_graph<Graph, EdgePredicate, VertexPredicate> >:
    vertex_property_type<Graph> {};

template <typename Graph,
          typename EdgePredicate,
          typename VertexPredicate>
struct edge_property_type<filt_graph<Graph, EdgePredicate, VertexPredicate> >:
    edge_property_type<Graph> {};

template <typename Graph,
          typename EdgePredicate,
          typename VertexPredicate>
struct graph_property_type<filt_graph<Graph, EdgePredicate, VertexPredicate> >:
    graph_property_type<Graph> {};

template<typename Graph, typename EdgePredicate, typename VertexPredicate>
struct vertex_bundle_type<filt_graph<Graph, EdgePredicate,
                                       VertexPredicate> >
  : vertex_bundle_type<Graph> { };

template<typename Graph, typename EdgePredicate, typename VertexPredicate>
struct edge_bundle_type<filt_graph<Graph, EdgePredicate,
                                     VertexPredicate> >
  : edge_bundle_type<Graph> { };

template<typename Graph, typename EdgePredicate, typename VertexPredicate>
struct graph_bundle_type<filt_graph<Graph, EdgePredicate,
                                      VertexPredicate> >
  : graph_bundle_type<Graph> { };

//===========================================================================
// Non-member functions for the Filtered Edge Graph

// Helper functions
template <typename Graph, typename EdgePredicate>
inline filt_graph<Graph, EdgePredicate>
make_filt_graph(Graph& g, EdgePredicate ep)
{
    return filt_graph<Graph, EdgePredicate>(g, ep);
}
template <typename Graph, typename EdgePredicate, typename VertexPredicate>
inline filt_graph<Graph, EdgePredicate, VertexPredicate>
make_filt_graph(Graph& g, EdgePredicate ep, VertexPredicate vp)
{
    return filt_graph<Graph, EdgePredicate, VertexPredicate>(g, ep, vp);
}

template <typename Graph, typename EdgePredicate>
inline filt_graph<const Graph, EdgePredicate>
make_filt_graph(const Graph& g, EdgePredicate ep)
{
    return filt_graph<const Graph, EdgePredicate>(g, ep);
}
template <typename Graph, typename EdgePredicate, typename VertexPredicate>
inline filt_graph<const Graph, EdgePredicate, VertexPredicate>
make_filt_graph(const Graph& g, EdgePredicate ep, VertexPredicate vp)
{
    return filt_graph<const Graph, EdgePredicate, VertexPredicate>(g, ep, vp);
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline))
std::pair<typename filt_graph<G, EP, VP>::vertex_iterator,
        typename filt_graph<G, EP, VP>::vertex_iterator>
vertices(const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typename graph_traits<G>::vertex_iterator f, l;
    boost::tie(f, l) = vertices(g._g);
    typedef typename Graph::vertex_iterator iter;
    return std::make_pair(iter(g._vertex_pred, f, l),
                          iter(g._vertex_pred, l, l));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline))
std::pair<typename filt_graph<G, EP, VP>::edge_iterator,
        typename filt_graph<G, EP, VP>::edge_iterator>
edges(const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typename graph_traits<G>::edge_iterator f, l;
    boost::tie(f, l) = edges(g._g);
    typedef typename Graph::edge_iterator iter;
    return std::make_pair(iter(g._all_edge_pred, f, l),
                          iter(g._all_edge_pred, l, l));
}

// An alternative for num_vertices() and num_edges() would be to
// count the number in the filtered graph. This is problematic
// because of the interaction with the vertex indices...  they would
// no longer go from 0 to num_vertices(), which would cause trouble
// for algorithms allocating property storage in an array. We could
// try to create a mapping to new recalibrated indices, but I don't
// see an efficient way to do this.
//
// However, the current solution is still unsatisfactory because
// the following semantic constraints no longer hold:
// boost::tie(vi, viend) = vertices(g);
// assert(std::distance(vi, viend) == num_vertices(g));

template <typename G, typename EP, typename VP>
inline
typename filt_graph<G, EP, VP>::vertices_size_type
num_vertices(const filt_graph<G, EP, VP>& g)
{
    return num_vertices(g._g);
}

template <typename G, typename EP, typename VP>
inline
typename filt_graph<G, EP, VP>::edges_size_type
num_edges(const filt_graph<G, EP, VP>& g)
{
    return num_edges(g._g);
}

template <class G, class EP, class VP>
inline
typename filt_graph_base<G>::vertex_descriptor
vertex(size_t i, const filt_graph<G,EP,VP>& g)
{
    auto v = vertex(i, g._g);
    if (g._vertex_pred(v))
        return v;
    else
        return graph_traits<G>::null_vertex();
}

template <typename G>
inline
typename filt_graph_base<G>::vertex_descriptor
source(const typename filt_graph_base<G>::edge_descriptor& e,
       const filt_graph_base<G>& g)
{
    return source(e, g._g);
}

template <typename G>
inline
typename filt_graph_base<G>::vertex_descriptor
target(const typename filt_graph_base<G>::edge_descriptor& e,
       const filt_graph_base<G>& g)
{
    return target(e, g._g);
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::out_edge_iterator,
          typename filt_graph<G, EP, VP>::out_edge_iterator>
out_edges(typename filt_graph<G, EP, VP>::vertex_descriptor u,
          const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::out_edge_iterator iter;
    auto range = out_edges(u, g._g);
    return std::make_pair(iter(g._out_edge_pred, range.first, range.second),
                          iter(g._out_edge_pred, range.second, range.second));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::out_edge_iterator,
          typename filt_graph<G, EP, VP>::out_edge_iterator>
_all_edges_out(typename filt_graph<G, EP, VP>::vertex_descriptor u,
               const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::out_edge_iterator iter;
    auto range = _all_edges_out(u, g._g);
    return std::make_pair(iter(g._out_edge_pred, range.first, range.second),
                          iter(g._out_edge_pred, range.second, range.second));
}

template <typename G, typename EP, typename VP>
inline
typename filt_graph<G, EP, VP>::degree_size_type
out_degree(typename filt_graph<G, EP, VP>::vertex_descriptor u,
           const filt_graph<G, EP, VP>& g)
{
  typename filt_graph<G, EP, VP>::degree_size_type n = 0;
  for (auto range = out_edges(u, g); range.first != range.second;
       ++range.first)
      ++n;
  return n;
}

template <typename G, typename EP, typename VP>
inline
typename filt_graph<G, EP, VP>::degree_size_type
degree(typename filt_graph<G, EP, VP>::vertex_descriptor u,
       const filt_graph<G, EP, VP>& g)
{
    return in_degree(u, g) + out_degree(u, g);
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::adjacency_iterator,
          typename filt_graph<G, EP, VP>::adjacency_iterator>
out_neighbours(typename filt_graph<G, EP, VP>::vertex_descriptor u,
               const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::adjacency_iterator adjacency_iterator;
    auto range = out_edges(u, g);
    return std::make_pair(adjacency_iterator(range.first, const_cast<Graph*>(&g)),
                          adjacency_iterator(range.second, const_cast<Graph*>(&g)));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::in_adjacency_iterator,
          typename filt_graph<G, EP, VP>::in_adjacency_iterator>
in_neighbours(typename filt_graph<G, EP, VP>::vertex_descriptor u,
              const filt_graph<G, EP, VP>& g)
{
  typedef filt_graph<G, EP, VP> Graph;
  typedef typename Graph::in_adjacency_iterator adjacency_iterator;
  auto range = in_edges(u, g);
  return std::make_pair(adjacency_iterator(range.first, const_cast<Graph*>(&g)),
                        adjacency_iterator(range.second, const_cast<Graph*>(&g)));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::adjacency_iterator,
          typename filt_graph<G, EP, VP>::adjacency_iterator>
all_neighbours(typename filt_graph<G, EP, VP>::vertex_descriptor u,
               const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::adjacency_iterator adjacency_iterator;
    auto range = _all_edges_out(u, g);
    return std::make_pair(adjacency_iterator(range.first, const_cast<Graph*>(&g)),
                          adjacency_iterator(range.second, const_cast<Graph*>(&g)));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::adjacency_iterator,
          typename filt_graph<G, EP, VP>::adjacency_iterator>
adjacent_vertices(typename filt_graph<G, EP, VP>::vertex_descriptor u,
                  const filt_graph<G, EP, VP>& g)
{
    return out_neighbours(u, g);
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::in_edge_iterator,
        typename filt_graph<G, EP, VP>::in_edge_iterator>
in_edges(typename filt_graph<G, EP, VP>::vertex_descriptor u,
       const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::in_edge_iterator iter;
    auto range = in_edges(u, g._g);
    return std::make_pair(iter(g._in_edge_pred, range.first, range.second),
                          iter(g._in_edge_pred, range.second, range.second));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::in_edge_iterator,
        typename filt_graph<G, EP, VP>::in_edge_iterator>
_all_edges_in(typename filt_graph<G, EP, VP>::vertex_descriptor u,
            const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::in_edge_iterator iter;
    auto range = _all_edges_in(u, g._g);
    return std::make_pair(iter(g._in_edge_pred, range.first, range.second),
                          iter(g._in_edge_pred, range.second, range.second));
}

template <typename G, typename EP, typename VP>
inline
typename filt_graph<G, EP, VP>::degree_size_type
in_degree(typename filt_graph<G, EP, VP>::vertex_descriptor u,
          const filt_graph<G, EP, VP>& g)
{
    typename filt_graph<G, EP, VP>::degree_size_type n = 0;
    for (auto range = in_edges(u, g); range.first != range.second;
         ++range.first)
        ++n;
    return n;
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename filt_graph<G, EP, VP>::all_edge_iterator,
          typename filt_graph<G, EP, VP>::all_edge_iterator>
all_edges(typename filt_graph<G, EP, VP>::vertex_descriptor u,
          const filt_graph<G, EP, VP>& g)
{
    typedef typename filt_graph<G, EP, VP>::all_edge_iterator iter;
    auto range = all_edges(u, g._g);
    return std::make_pair(iter(g._all_edge_pred, range.first, range.second),
                          iter(g._all_edge_pred, range.second, range.second));
}


template <typename G, typename EP, typename VP>
inline
std::pair<typename filt_graph<G, EP, VP>::edge_descriptor, bool>
edge(typename filt_graph<G, EP, VP>::vertex_descriptor u,
     typename filt_graph<G, EP, VP>::vertex_descriptor v,
     const filt_graph<G, EP, VP>& g)
{
    typename graph_traits<G>::edge_descriptor e;
    bool exists;
    boost::tie(e, exists) = edge(u, v, g._g);
    return std::make_pair(e, exists && g._edge_pred(e));
}

template <typename G, typename EP, typename VP>
inline __attribute__((always_inline))
std::pair<typename filt_graph<G, EP, VP>::out_edge_iterator,
          typename filt_graph<G, EP, VP>::out_edge_iterator>
edge_range(typename filt_graph<G, EP, VP>::vertex_descriptor u,
           typename filt_graph<G, EP, VP>::vertex_descriptor v,
           const filt_graph<G, EP, VP>& g)
{
    typedef filt_graph<G, EP, VP> Graph;
    typedef typename Graph::out_edge_iterator iter;
    typename graph_traits<G>::out_edge_iterator f, l;
    boost::tie(f, l) = edge_range(u, v, g._g);
    return std::make_pair(iter(g._out_edge_pred, f, l),
                          iter(g._out_edge_pred, l, l));
}

template <class G, class EP, class VP>
inline
std::pair<typename graph_traits
            <filt_graph<G,EP,VP>>::edge_descriptor, bool>
add_edge(typename graph_traits
             <filt_graph<G,EP,VP>>::vertex_descriptor u,
         typename graph_traits
             <filt_graph<G,EP,VP>>::vertex_descriptor v,
         filt_graph<G,EP,VP>& g)
{
    auto ret = add_edge(u, v, const_cast<G&>(g._g));
    auto filt = g._edge_pred.get_filter().get_checked();
    filt[ret.first] = !g._edge_pred.is_inverted();
    return ret;
}

template <class G, class EP, class VP, class Pred>
inline void
clear_vertex(typename boost::graph_traits
             <filt_graph<G,EP,VP>>::vertex_descriptor v,
             filt_graph<G,EP,VP>& g, Pred&& pred)
{
    clear_vertex(v, const_cast<G&>(g._g),
                 [&](auto&& e){ return (((g._edge_pred(e) &&
                                          g._vertex_pred(source(e, g._g)) &&
                                          g._vertex_pred(target(e, g._g)))) &&
                                        pred(e)); });
}

template <class G, class EP, class VP>
inline void
clear_vertex(typename boost::graph_traits
                 <filt_graph<G,EP,VP>>::vertex_descriptor v,
             filt_graph<G,EP,VP>& g)
{
    clear_vertex(v, g, [&](auto&&){ return true; });
}

template <class G, class EP, class VP>
inline
void remove_edge(const typename boost::graph_traits
                   <filt_graph<G,EP,VP>>::edge_descriptor& e,
                 filt_graph<G,EP,VP>& g)
{
    return remove_edge(e, const_cast<G&>(g._g));
}

template <class G, class EP, class VP>
inline
void remove_vertex(typename boost::graph_traits
                     <filt_graph<G,EP,VP>>::vertex_descriptor v,
                  filt_graph<G,EP,VP>& g)
{
    auto& filt = g._vertex_pred.get_filter();
    for (size_t i = v; i < num_vertices(g) - 1; ++i)
        filt[i] = filt[i + 1];
    return remove_vertex(v,const_cast<G&>(g._g));
}

template <class G, class EP, class VP>
inline
void remove_vertex_fast(typename boost::graph_traits
                          <filt_graph<G,EP,VP>>::vertex_descriptor v,
                       filt_graph<G,EP,VP>& g)
{
   size_t back = num_vertices(g) - 1;
   auto& filt = g._vertex_pred.get_filter();
   filt[v] = filt[back];
   return remove_vertex_fast(v,const_cast<G&>(g._g));
}

template <class G, class EP, class VP>
inline
typename boost::graph_traits<filt_graph<G,EP,VP>>::vertex_descriptor
add_vertex(filt_graph<G,EP,VP>& g)
{
    auto filt = g._vertex_pred.get_filter().get_checked();
    auto v = add_vertex(const_cast<G&>(g._g));
    filt[v] = !g._vertex_pred.is_inverted();
    return v;
}

//===========================================================================
// Property map

template <typename G, typename EP, typename VP, typename Property>
struct property_map<filt_graph<G, EP, VP>, Property>
    : property_map<G, Property> {};

template <typename G, typename EP, typename VP, typename Property>
inline
typename property_map<G, Property>::type
get(Property p, filt_graph<G, EP, VP>& g)
{
    return get(p, const_cast<G&>(g._g));
}

template <typename G, typename EP, typename VP,typename Property>
inline
typename property_map<G, Property>::const_type
get(Property p, const filt_graph<G, EP, VP>& g)
{
    return get(p, (const G&)g._g);
}

template <typename G, typename EP, typename VP, typename Property,
          typename Key>
inline
auto&&
get(Property p, const filt_graph<G, EP, VP>& g, const Key& k)
{
    return get(p, (const G&)g._g, k);
}

template <typename G, typename EP, typename VP, typename Property,
          typename Key, typename Value>
inline
void
put(Property p, const filt_graph<G, EP, VP>& g, const Key& k,
    const Value& val)
{
    put(p, const_cast<G&>(g._g), k, val);
}

} // namespace boost


#endif // GRAPH_FILTERED_HH

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

#ifndef GRAPH_SELECTORS_HH
#define GRAPH_SELECTORS_HH

#include <utility>
#include <type_traits>
#include <boost/mpl/pair.hpp>
#include <boost/mpl/map.hpp>
#include <boost/mpl/at.hpp>
#include <boost/mpl/vector.hpp>
#include <boost/mpl/find.hpp>
#include <boost/mpl/not.hpp>
#include <boost/mpl/logical.hpp>

#include "graph_adaptor.hh"
#include "graph_properties.hh"
#include "graph.hh"

namespace graph_tool
{

// This file contain selector for degree types for different types of
// graphs. Namely, they will return the in degree, out degree, and total degree
// for both directed and undirected graphs. There is also an scalar selector,
// which will return a specific scalar property

// This file also contains selectors for in_edge iterators of graphs, which
// return an empty range for undirected graphs

namespace detail
{
    struct no_weightS {};

    template <class Weight>
    struct get_weight_type
    {
        typedef typename boost::property_traits<typename std::remove_reference<Weight>::type>::value_type type;
    };

    template <>
    struct get_weight_type<no_weightS&>
    {
        typedef size_t type;
    };

    template <>
    struct get_weight_type<no_weightS>
    {
        typedef size_t type;
    };
}

struct in_degreeS
{
    typedef size_t value_type;

    in_degreeS() {}

    template <class Graph>
    inline __attribute__((always_inline))
    auto operator()(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph& g) const
    {
        return in_degreeS::operator()(v, g, detail::no_weightS());
    }

    template <class Graph, class Weight>
    inline  __attribute__((always_inline))
    auto operator()(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph& g, Weight&& weight) const
    {
        typedef typename std::is_convertible
            <typename boost::graph_traits<Graph>::directed_category,
             boost::directed_tag>::type is_directed;
        return get_in_degree(v, g, is_directed(), std::forward<Weight>(weight));
    }

    template <class Graph>
    inline __attribute__((always_inline))
    auto get_in_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                       const Graph& g, std::true_type,
                       detail::no_weightS) const
    {
        return in_degree(v, g);
    }

    template <class Graph, class Key, class Value>
    auto get_in_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                       const Graph& g, std::true_type,
                       const ConstantPropertyMap<Value, Key>& weight) const
    {
        return in_degree(v, g) * weight.c;
    }

    template <class Graph, class Key, class Value>
    auto get_in_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                       const Graph& g, std::true_type,
                       const UnityPropertyMap<Value, Key>&) const
    {
        return in_degree(v, g);
    }

    template <class Graph, class Weight>
    auto get_in_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                       const Graph& g, std::true_type, Weight& weight) const
    {
        typedef typename boost::property_traits<Weight>::value_type val_t;
        val_t d = val_t();
        typename boost::graph_traits<Graph>::in_edge_iterator e, e_end;
        for (std::tie(e, e_end) = in_edges(v, g); e != e_end; ++e)
            d += get(weight, *e);
        return d;
    }

    template <class Graph, class Weight>
    inline __attribute__((always_inline))
    auto get_in_degree(const typename boost::graph_traits<Graph>::vertex_descriptor&,
                       const Graph&, std::false_type, Weight&&)  const
    {
        return 0;
    }
};

struct out_degreeS
{
    typedef size_t value_type;

    out_degreeS() {}

    template <class Graph>
    inline __attribute__((always_inline))
    auto operator()(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph& g) const
    {
        return out_degreeS::operator()(v, g, detail::no_weightS());
    }

    template <class Graph, class Weight>
    inline __attribute__((always_inline))
    auto operator()(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph& g, Weight&& weight) const
    {
        return get_out_degree(v, g, std::forward<Weight>(weight));
    }

    template <class Graph, class Key, class Value>
    auto get_out_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                        const Graph& g,
                        const ConstantPropertyMap<Value, Key>& weight) const
    {
        return out_degree(v, g) * weight.c;
    }

    template <class Graph, class Key, class Value>
    auto get_out_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                        const Graph& g,
                        const UnityPropertyMap<Value, Key>&) const
    {
        return out_degree(v, g);
    }

    template <class Graph, class Weight>
    inline
    auto get_out_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                        const Graph& g, const Weight& weight) const
    {
        typedef typename boost::property_traits<Weight>::value_type val_t;
        val_t d = val_t();
        typename boost::graph_traits<Graph>::out_edge_iterator e, e_end;
        for (std::tie(e, e_end) = out_edges(v, g); e != e_end; ++e)
            d += get(weight, *e);
        return d;
    }

    template <class Graph>
    inline __attribute__((always_inline))
    auto get_out_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                        const Graph& g, detail::no_weightS) const
    {
        return out_degree(v, g);
    }
};

struct total_degreeS
{
    typedef size_t value_type;

    total_degreeS() {}
    template <class Graph>
    inline __attribute__((always_inline))
    auto operator()(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph& g) const
    {
        return total_degreeS::operator()(v, g, detail::no_weightS());
    }

    template <class Graph, class Weight>
    inline __attribute__((always_inline))
    auto operator()(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph& g, Weight&& weight) const
    {
        typedef typename std::is_convertible
            <typename boost::graph_traits<Graph>::directed_category,
             boost::directed_tag>::type is_directed;
        return get_total_degree(v, g, is_directed(),
                                std::forward<Weight>(weight));
    }

    template <class Graph, class Weight>
    inline __attribute__((always_inline))
    auto get_total_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                          const Graph& g, std::true_type,
                          Weight&& weight) const
    {
        return in_degreeS()(v, g, std::forward<Weight>(weight)) +
            out_degreeS()(v, g, std::forward<Weight>(weight));
    }

    template <class Graph, class Weight>
    inline __attribute__((always_inline))
    auto get_total_degree(typename boost::graph_traits<Graph>::vertex_descriptor v,
                          const Graph& g, std::false_type, Weight&& weight) const
    {
        return out_degreeS()(v, g, std::forward<Weight>(weight));
    }
};


template <class PropertyMap>
struct scalarS
{
    typedef typename boost::property_traits<PropertyMap>::value_type value_type;

    scalarS() {}
    scalarS(PropertyMap pmap): _pmap(pmap) {}

    template <class Descriptor, class Graph>
    inline __attribute__((always_inline))
    auto operator()(const Descriptor& d, const Graph&) const
    {
        return get(_pmap, d);
    }

    PropertyMap _pmap;
};

struct get_degree_selector
{
    typedef boost::mpl::map
        <boost::mpl::pair<in_degreeS,
                          boost::mpl::int_<GraphInterface::IN_DEGREE> >,
         boost::mpl::pair<out_degreeS,
                          boost::mpl::int_<GraphInterface::OUT_DEGREE> >,
         boost::mpl::pair<total_degreeS,
                          boost::mpl::int_<GraphInterface::TOTAL_DEGREE> > >
        degree_selector_index;

    template <class Selector>
    void operator()(Selector, int deg_index, boost::any& deg) const
    {
        if (boost::mpl::at<degree_selector_index, Selector>::type::value == deg_index)
            deg = Selector();
    }
};

struct get_scalar_selector
{
    template <class PropertyMap>
    void operator()(PropertyMap, boost::any prop, boost::any& sec, bool& found)
        const
    {
        try
        {
            PropertyMap map = boost::any_cast<PropertyMap>(prop);
            sec = scalarS<PropertyMap>(map);
            found = true;
        }
        catch (boost::bad_any_cast&) {}
    }
};

struct scalar_selector_type
{
    template <class PropertyMap>
    struct apply
    {
        typedef scalarS<PropertyMap> type;
    };
};

struct selectors:
    boost::mpl::vector<out_degreeS, in_degreeS, total_degreeS> {};

// retrieves the appropriate degree selector
boost::any degree_selector(GraphInterface::deg_t deg);

// helper types for in_edge_iteratorS

template <class Graph, class IsDirected>
struct get_in_edges
{
    BOOST_MPL_ASSERT((std::is_same<IsDirected,std::true_type>));
    BOOST_MPL_ASSERT((std::is_convertible
                      <typename boost::graph_traits<Graph>::directed_category,
                      boost::directed_tag>));
    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    typedef typename boost::graph_traits<Graph>::in_edge_iterator type;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_edges(vertex_descriptor v,
                                          const Graph& g)
    {
        return in_edges(v, g);
    }
};

template <class Graph>
struct get_in_edges<Graph,std::false_type>
{
    BOOST_MPL_ASSERT((std::is_convertible
                      <typename boost::graph_traits<Graph>::directed_category,
                      boost::undirected_tag>));
    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    typedef typename boost::graph_traits<Graph>::out_edge_iterator type;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_edges(vertex_descriptor,
                                          const Graph&)
    {
        return std::make_pair(type(), type());
    }
};

// this in-edge iterator selector returns the in-edge range for directed graphs
// and an empty out-edge range for undirected graphs. The iterator type is given
// by in_edge_iteratorS<Graph>::type.
template <class Graph>
struct in_edge_iteratorS
{
    typedef typename boost::graph_traits<Graph>::directed_category
        directed_category;
    typedef typename std::is_convertible<directed_category,
                                         boost::directed_tag>::type is_directed;
    typedef typename get_in_edges<Graph,is_directed>::type type;

    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_edges(vertex_descriptor v,
                                          const Graph& g)
    {
        return get_in_edges<Graph,is_directed>::get_edges(v, g);
    }
};

// out edges selector for completeness
template <class Graph>
struct out_edge_iteratorS
{
    typedef typename boost::graph_traits<Graph>::out_edge_iterator type;

    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_edges(vertex_descriptor v,
                                          const Graph& g)
    {
        return out_edges(v, g);
    }
};

// this "all edges" iterator selector returns the in-edge + out-edge ranges for
// directed graphs and the out-edge range for undirected graphs. The
// iterator type is given by all_edges_iteratorS<Graph>::type.
template <class Graph>
struct all_edges_iteratorS
{
    typedef typename Graph::all_edge_iterator type;

    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    inline __attribute__((always_inline))
    static std::pair<type, type> get_edges(vertex_descriptor v, const Graph& g)
    {
        return all_edges(v, g);
    }
};

// this "in or out" iterator selector returns the in-edge range for directed
// graphs and the out-edge range for undirected graphs. The iterator type is
// given by in_or_out_edges_iteratorS<Graph>::type
template <class Graph>
struct in_or_out_edge_iteratorS
    : public std::conditional
          <std::is_convertible
               <typename boost::graph_traits<Graph>::directed_category,
                boost::directed_tag>::value,
           in_edge_iteratorS<Graph>,
           out_edge_iteratorS<Graph>>::type
{};

// helper types for in_neighbour_iteratorS

template <class Graph, class IsDirected>
struct get_in_neighbours
{
    BOOST_MPL_ASSERT((std::is_same<IsDirected,std::true_type>));
    BOOST_MPL_ASSERT((std::is_convertible
                      <typename boost::graph_traits<Graph>::directed_category,
                      boost::directed_tag>));
    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    typedef typename boost::graph_traits<Graph>::in_neighbour_iterator type;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_edges(vertex_descriptor v,
                                          const Graph& g)
    {
        return in_neighbours(v, g);
    }
};

template <class Graph>
struct get_in_neighbours<Graph,std::false_type>
{
    BOOST_MPL_ASSERT((std::is_convertible
                      <typename boost::graph_traits<Graph>::directed_category,
                      boost::undirected_tag>));
    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    typedef typename boost::graph_traits<Graph>::out_neighbours_iterator type;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_neighbours(vertex_descriptor,
                                               const Graph&)
    {
        return make_pair(type(), type());
    }
};

// this in-neighbour iterator selector returns the in-neighbour range for
// directed graphs and an empty out-neighbour range for undirected graphs. The
// iterator type is given by in_neighbour_iteratorS<Graph>::type.
template <class Graph>
struct in_neighbour_iteratorS
{
    typedef typename boost::graph_traits<Graph>::directed_category
        directed_category;
    typedef typename std::is_convertible<directed_category,
                                         boost::directed_tag>::type is_directed;
    typedef typename get_in_edges<Graph,is_directed>::type type;

    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_neighbours(vertex_descriptor v,
                                               const Graph& g)
    {
        return get_in_neighbours<Graph,is_directed>::get_neighbours(v, g);
    }
};

// out edges selector for completeness
template <class Graph>
struct out_neighbour_iteratorS
{
    typedef typename boost::graph_traits<Graph>::out_neighbours_iterator type;

    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_neighbours(vertex_descriptor v,
                                               const Graph& g)
    {
        return out_neighbours(v, g);
    }
};

// this "all neighbours" iterator selector returns the in-neighbours +
// out-neighbours ranges for directed graphs and the out-neighbours range for
// undirected graphs. The iterator type is given by
// all_neighbours_iteratorS<Graph>::type.
template <class Graph>
struct all_neighbours_iteratorS
{
    typedef typename boost::graph_traits<Graph>::adjacency_iterator type;
    typedef typename boost::graph_traits<Graph>::vertex_descriptor
        vertex_descriptor;
    inline __attribute__((always_inline))
    static std::pair<type,type> get_neighbours(vertex_descriptor v,
                                               const Graph& g)
    {
        return all_neighbours(v, g);
    }
};

// this "in or out" iterator selector returns the in-neighbour range for
// directed graphs and the out-neighbour range for undirected graphs. The
// iterator type is given by in_or_adjacency_iteratorS<Graph>::type
template <class Graph>
struct in_or_out_neighbours_iteratorS
    : public std::conditional
          <std::is_convertible
               <typename boost::graph_traits<Graph>::directed_category,
                boost::directed_tag>::value,
           in_neighbour_iteratorS<Graph>,
           out_neighbour_iteratorS<Graph>>::type
{};

// range adaptors

template <class Iter>
class IterRange
{
public:
    explicit IterRange(std::pair<Iter, Iter>&& range)
        : _range(std::forward<std::pair<Iter, Iter>>(range)) {}
    const Iter& begin() { return _range.first; }
    const Iter& end() { return _range.second; }
private:
    std::pair<Iter, Iter> _range;
};

template <class Iter>
inline __attribute__((always_inline))
auto mk_range(std::pair<Iter, Iter>&& range)
{
    return IterRange<Iter>(std::forward<std::pair<Iter, Iter>>(range));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto vertices_range(const Graph& g)
{
    return mk_range(vertices(g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto edges_range(const Graph& g)
{
    return mk_range(edges(g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto adjacent_vertices_range(typename boost::graph_traits<Graph>::vertex_descriptor v,
                             const Graph& g)
{
    return mk_range(adjacent_vertices(v, g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto out_edges_range(typename out_edge_iteratorS<Graph>::vertex_descriptor v,
                     const Graph& g)
{
    return mk_range(out_edge_iteratorS<Graph>::get_edges(v, g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto out_neighbours_range(typename boost::graph_traits<Graph>::vertex_descriptor v,
                          const Graph& g)
{
    return mk_range(out_neighbours(v, g));
}


template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto in_edges_range(typename in_edge_iteratorS<Graph>::vertex_descriptor v,
                    const Graph& g)
{
    return mk_range(in_edge_iteratorS<Graph>::get_edges(v, g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto in_neighbours_range(typename boost::graph_traits<Graph>::vertex_descriptor v,
                         const Graph& g)
{
    return mk_range(in_neighbours(v, g));
}


template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto all_edges_range(typename all_edges_iteratorS<Graph>::vertex_descriptor v,
                     const Graph& g)
{
    return mk_range(all_edges(v, g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto all_neighbours_range(typename all_neighbours_iteratorS<Graph>::vertex_descriptor v,
                          const Graph& g)
{
    return mk_range(all_neighbours(v, g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto in_or_out_edges_range(typename in_or_out_edge_iteratorS<Graph>::vertex_descriptor v,
                           const Graph& g)
{
    return mk_range(in_or_out_edge_iteratorS<Graph>::get_edges(v, g));
}

template <class Graph>
inline __attribute__((always_inline)) __attribute__((flatten))
auto in_or_out_neighbours_range(typename in_or_out_edge_iteratorS<Graph>::vertex_descriptor v,
                                const Graph& g)
{
    return mk_range(in_or_out_edge_iteratorS<Graph>::get_neighbours(v, g));
}

// useful type lists

struct degree_selectors:
        boost::mpl::vector<in_degreeS, out_degreeS, total_degreeS> {};

struct vertex_properties:
        property_map_types::apply<value_types,
                                  GraphInterface::vertex_index_map_t>::type {};

struct writable_vertex_properties:
        property_map_types::apply<value_types,
                                  GraphInterface::vertex_index_map_t,
                                  boost::mpl::bool_<false> >::type {};
struct edge_properties:
        property_map_types::apply<value_types,
                                  GraphInterface::edge_index_map_t>::type {};

struct writable_edge_properties:
        property_map_types::apply<value_types,
                                  GraphInterface::edge_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct vertex_scalar_properties:
        property_map_types::apply<scalar_types,
                                  GraphInterface::vertex_index_map_t>::type {};

struct writable_vertex_scalar_properties:
        property_map_types::apply<scalar_types,
                                  GraphInterface::vertex_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct vertex_integer_properties:
        property_map_types::apply<integer_types,
                                  GraphInterface::vertex_index_map_t>::type {};

struct vertex_floating_properties:
        property_map_types::apply<floating_types,
                                  GraphInterface::vertex_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct vertex_scalar_vector_properties:
        property_map_types::apply<scalar_vector_types,
                                  GraphInterface::vertex_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct vertex_integer_vector_properties:
        property_map_types::apply<integer_vector_types,
                                  GraphInterface::vertex_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct vertex_floating_vector_properties:
        property_map_types::apply<floating_vector_types,
                                  GraphInterface::vertex_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct edge_scalar_properties:
        property_map_types::apply<scalar_types,
                                  GraphInterface::edge_index_map_t>::type {};

struct writable_edge_scalar_properties:
        property_map_types::apply<scalar_types,
                                  GraphInterface::edge_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct edge_integer_properties:
        property_map_types::apply<integer_types,
                                  GraphInterface::edge_index_map_t>::type {};

struct edge_floating_properties:
        property_map_types::apply<floating_types,
                                  GraphInterface::edge_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct edge_scalar_vector_properties:
        property_map_types::apply<scalar_vector_types,
                                  GraphInterface::edge_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct edge_integer_vector_properties:
        property_map_types::apply<integer_vector_types,
                                  GraphInterface::edge_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct edge_floating_vector_properties:
        property_map_types::apply<floating_vector_types,
                                  GraphInterface::edge_index_map_t,
                                  boost::mpl::bool_<false> >::type {};

struct vertex_scalar_selectors:
        boost::mpl::transform<vertex_scalar_properties,
                              scalar_selector_type>::type {};

struct all_selectors:
        boost::mpl::transform<vertex_properties,
                              scalar_selector_type,
                              boost::mpl::back_inserter<degree_selectors> >::type {};

struct scalar_selectors:
        boost::mpl::transform<vertex_scalar_properties,
                              scalar_selector_type,
                              boost::mpl::back_inserter<degree_selectors> >::type {};

} //namespace graph_tool

#endif

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

#ifndef GRAPH_ADJACENCY_HH
#define GRAPH_ADJACENCY_HH

#include <vector>
#include <deque>
#include <utility>
#include <numeric>
#include <iostream>
#include <tuple>
#include <functional>
#include <boost/iterator.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/range/irange.hpp>
#include <boost/property_map/property_map.hpp>
#include <boost/graph/properties.hpp>
#include <boost/iterator/transform_iterator.hpp>
#include <boost/iterator/iterator_facade.hpp>

#include "transform_iterator.hh"

namespace boost
{

// ========================================================================
// Forward declarations
// ========================================================================

template <class Vertex>
class adj_list;

// forward declaration of manipulation functions
template <class Vertex>
std::pair<typename adj_list<Vertex>::vertex_iterator,
          typename adj_list<Vertex>::vertex_iterator>
vertices(const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::edge_iterator,
          typename adj_list<Vertex>::edge_iterator>
edges(const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::edge_descriptor, bool>
edge(Vertex s, Vertex t, const adj_list<Vertex>& g);

template <class Vertex>
size_t out_degree(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
size_t in_degree(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
size_t degree(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::out_edge_iterator,
          typename adj_list<Vertex>::out_edge_iterator>
out_edges(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::in_edge_iterator,
          typename adj_list<Vertex>::in_edge_iterator>
in_edges(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::out_edge_iterator,
          typename adj_list<Vertex>::out_edge_iterator>
_all_edges_out(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::in_edge_iterator,
          typename adj_list<Vertex>::in_edge_iterator>
_all_edges_in(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::all_edge_iterator,
          typename adj_list<Vertex>::all_edge_iterator>
all_edges(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::all_edge_iterator_reversed,
          typename adj_list<Vertex>::all_edge_iterator_reversed>
_all_edges_reversed(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
adjacent_vertices(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
out_neighbours(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
in_neighbours(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
all_neighbours(Vertex v, const adj_list<Vertex>& g);

template <class Vertex>
size_t num_vertices(const adj_list<Vertex>& g);

template <class Vertex>
size_t num_edges(const adj_list<Vertex>& g);

template <class Vertex>
Vertex add_vertex(adj_list<Vertex>& g);

template <class Vertex>
void clear_vertex(Vertex v, adj_list<Vertex>& g);

template <class Vertex, class Pred>
void clear_vertex(Vertex v, adj_list<Vertex>& g, Pred&& pred);

template <class Vertex>
void remove_vertex(Vertex v, adj_list<Vertex>& g);

template <class Vertex>
void remove_vertex_fast(Vertex v, adj_list<Vertex>& g);

template <class Vertex>
std::pair<typename adj_list<Vertex>::edge_descriptor, bool>
add_edge(Vertex s, Vertex t, adj_list<Vertex>& g);

template <class Vertex>
void remove_edge(Vertex s, Vertex t, adj_list<Vertex>& g);

template <class Vertex>
void remove_edge(const typename adj_list<Vertex>::edge_descriptor& e,
                 adj_list<Vertex>& g);

// ========================================================================
// adj_list<Vertex>
// ========================================================================
//
// adj_list is a very simple adjacency list implementation for bidirectional
// graphs based on std::vector, meant to be reasonably efficient both
// memory-wise and computationally. It maintains a list of in and out-edges for
// each vertex, and each edge has a built-in index (which is replicated in both
// lists). For each edge, a total of 4 integers is necessary: the source and
// target vertices, in the in_edges and out_edges lists, respectively, and the
// (same) edge index in both lists. The integer type is given by the Vertex
// template parameter. It achieves about half as much memory as
// boost::adjacency_list with an edge index property map and the same integer
// type.

// The complexity guarantees and iterator invalidation rules are the same as
// boost::adjacency_list with vector storage selectors for both vertex and edge
// lists.

namespace detail
{
template <class Vertex>
struct adj_edge_descriptor
{
    adj_edge_descriptor()
        : s(std::numeric_limits<Vertex>::max()),
          t(std::numeric_limits<Vertex>::max()),
          idx(std::numeric_limits<Vertex>::max()) {};
    adj_edge_descriptor(Vertex s, Vertex t, Vertex idx)
        : s(s), t(t), idx(idx) {}

    bool operator==(const adj_edge_descriptor& other) const
    {
        return idx == other.idx;
    }
    bool operator!=(const adj_edge_descriptor& other) const
    {
        return idx != other.idx;
    }
    bool operator<(const adj_edge_descriptor& other) const
    {
        return idx < other.idx;
    }

    Vertex s, t, idx;
};
} // namespace detail

template <class Vertex = size_t>
class adj_list
{
public:
    struct graph_tag {};
    typedef Vertex vertex_t;

    typedef detail::adj_edge_descriptor<Vertex> edge_descriptor;

    typedef std::vector<std::pair<vertex_t, vertex_t> > edge_list_t;
    typedef std::vector<std::pair<size_t, edge_list_t>> vertex_list_t;
    typedef typename integer_range<Vertex>::iterator vertex_iterator;

    adj_list(): _n_edges(0), _edge_index_range(0), _keep_epos(false) {}

    struct get_vertex
    {
        get_vertex() {}
        typedef Vertex result_type;
        __attribute__((always_inline))
        Vertex operator()(const std::pair<vertex_t, vertex_t>& v) const
        { return v.first; }
    };

    typedef transform_random_access_iterator<get_vertex,
                                             typename edge_list_t::const_iterator>
        adjacency_iterator;

    typedef adjacency_iterator in_adjacency_iterator;

    template <class Deference>
    struct base_edge_iterator:
        public boost::iterator_facade<base_edge_iterator<Deference>,
                                      edge_descriptor,
                                      std::random_access_iterator_tag,
                                      edge_descriptor>
    {
        base_edge_iterator() {}
        base_edge_iterator(vertex_t v, typename edge_list_t::const_iterator&& iter)
            : _v(v), _iter(std::forward<typename edge_list_t::const_iterator>(iter))
        {}

    private:
        friend class boost::iterator_core_access;
        void increment() { ++_iter; }
        void decrement() { --_iter; }
        template <class Distance>
        void advance(Distance n) { _iter += n; }
        auto distance_to(base_edge_iterator const& other) const
        {
            return other._iter - _iter;
        }

        bool equal(base_edge_iterator const& other) const
        {
            return _iter == other._iter;
        }

        __attribute__((always_inline)) __attribute__((flatten))
        edge_descriptor dereference() const
        {
            return Deference::def(_v, *_iter, *this);
        }

    protected:
        vertex_t _v;
        typename edge_list_t::const_iterator _iter;
    };

    struct make_out_edge
    {
        template <class Iter>
        static edge_descriptor def(vertex_t src,
                                   const std::pair<vertex_t, vertex_t>& v,
                                   Iter&&)
        { return edge_descriptor(src, v.first, v.second); }

        static edge_descriptor def(vertex_t src,
                                   const std::pair<vertex_t, vertex_t>& v)
        { return def(src, v, nullptr); }
    };

    struct make_in_edge
    {
        template <class Iter>
        static edge_descriptor def(vertex_t tgt,
                                   const std::pair<vertex_t, vertex_t>& v,
                                   Iter&&)
        { return edge_descriptor(v.first, tgt, v.second); }

        static edge_descriptor def(vertex_t tgt,
                                   const std::pair<vertex_t, vertex_t>& v)
        { return def(tgt, v, nullptr); }
    };

    typedef base_edge_iterator<make_out_edge> out_edge_iterator;
    typedef base_edge_iterator<make_in_edge> in_edge_iterator;


    template <class Iter, bool reversed>
    struct make_in_or_out_edge
    {
        template <class I>
        static edge_descriptor def(vertex_t u,
                                   const std::pair<vertex_t, vertex_t>& v,
                                   const I& i)
        {
            const Iter& iter = reinterpret_cast<const Iter&>(i);
            if ((iter._iter < iter._pos) != reversed)
                return edge_descriptor(u, v.first, v.second);
            else
                return edge_descriptor(v.first, u, v.second);
        }
    };

    template <bool reversed>
    struct all_edge_iterator_base:
        public base_edge_iterator<make_in_or_out_edge<all_edge_iterator_base<reversed>,
                                                      reversed>>
    {
        all_edge_iterator_base() {}
        all_edge_iterator_base(vertex_t v,
                               typename edge_list_t::const_iterator&& iter,
                               const typename edge_list_t::const_iterator& pos)
            : base_edge_iterator<make_in_or_out_edge<all_edge_iterator_base,
                                                     reversed>>
                  (v, std::forward<typename edge_list_t::const_iterator>(iter)),
              _pos(pos)
        {}

    private:
        friend struct make_in_or_out_edge<all_edge_iterator_base<reversed>,
                                          reversed>;
        typename edge_list_t::const_iterator _pos;
    };

    typedef all_edge_iterator_base<false> all_edge_iterator;
    typedef all_edge_iterator_base<true>  all_edge_iterator_reversed;

    class edge_iterator:
        public boost::iterator_facade<edge_iterator,
                                      edge_descriptor,
                                      boost::forward_traversal_tag,
                                      edge_descriptor>
    {
    public:
        edge_iterator() {}
        explicit edge_iterator(const typename vertex_list_t::const_iterator& vi_begin,
                               const typename vertex_list_t::const_iterator& vi_end,
                               const typename vertex_list_t::const_iterator& vi,
                               const typename edge_list_t::const_iterator& ei)
            : _vi_begin(vi_begin), _vi_end(vi_end), _vi(vi), _ei(ei)
        {
            // move position to first edge
            skip();
        }

    private:
        friend class boost::iterator_core_access;

        void skip()
        {
            //skip empty vertices
            while (_vi != _vi_end &&
                   _ei == _vi->second.begin() + _vi->first)
            {
                ++_vi;
                if (_vi != _vi_end)
                    _ei = _vi->second.begin();
            }
        }

        void increment()
        {
            ++_ei;
            skip();
        }

        bool equal(edge_iterator const& other) const
        {
            if (_vi_begin == _vi_end)
                return _vi == other._vi;
            return _vi == other._vi && _ei == other._ei;
        }

        edge_descriptor dereference() const
        {
            return edge_descriptor(vertex_t(_vi - _vi_begin),
                                   _ei->first, _ei->second);
        }

        typename vertex_list_t::const_iterator _vi_begin;
        typename vertex_list_t::const_iterator _vi_end;
        typename vertex_list_t::const_iterator _vi;
        typename edge_list_t::const_iterator _ei;
    };

    void reindex_edges()
    {
        _free_indexes.clear();
        _edge_index_range = 0;
        for (auto& es : _edges)
            es.second.resize(es.first);
        for (size_t i = 0; i < _edges.size(); ++i)
        {
            auto pos = _edges[i].first;
            auto& es = _edges[i].second;
            for (size_t j = 0; j < pos; ++j)
            {
                auto& oe = es[j];
                Vertex v = oe.first;
                oe.second = _edge_index_range;
                _edges[v].second.emplace_back(i, _edge_index_range);
                _edge_index_range++;
            }
        }

        if (_keep_epos)
            rebuild_epos();
    }

    void set_keep_epos(bool keep)
    {
        if (keep)
        {
            if (!_keep_epos)
                rebuild_epos();
        }
        else
        {
            _epos.clear();
        }
        _keep_epos = keep;
    }

    bool get_keep_epos()
    {
        return _keep_epos;
    }

    size_t get_edge_index_range() const { return _edge_index_range; }

    static Vertex null_vertex() { return std::numeric_limits<Vertex>::max(); }

    void shrink_to_fit()
    {
        _edges.shrink_to_fit();
        std::for_each(_edges.begin(), _edges.end(),
                      [](auto &es){es.second.shrink_to_fit();});
        auto erange = boost::edges(*this);
        auto iter = std::max_element(erange.first, erange.second,
                                     [](const auto &a, const auto& b) -> bool
                                     {return a.idx < b.idx;});
        if (iter == erange.second)
            _edge_index_range = 0;
        else
            _edge_index_range = iter->idx + 1;
        auto iter_idx = std::remove_if(_free_indexes.begin(),
                                       _free_indexes.end(),
                                       [&](auto idx) -> bool
                                       {return idx > _edge_index_range;});
        _free_indexes.erase(iter_idx, _free_indexes.end());
        _free_indexes.shrink_to_fit();
        if (_keep_epos)
            _epos.resize(_edge_index_range);
        _epos.shrink_to_fit();
    }

private:
    vertex_list_t _edges;
    size_t _n_edges;
    size_t _edge_index_range;
    std::deque<size_t> _free_indexes; // indexes of deleted edges to be used up
                                      // for new edges to avoid very large
                                      // indexes, and unnecessary property map
                                      // memory use
    bool _keep_epos;
    std::vector<std::pair<uint32_t, uint32_t>> _epos; // out, in

    void rebuild_epos()
    {
        _epos.resize(_edge_index_range);
        for (auto& pes : _edges)
        {
            auto pos = pes.first;
            auto& es = pes.second;
            for (size_t j = 0; j < es.size(); ++j)
            {
                size_t idx = es[j].second;
                if (j < pos)
                    _epos[idx].first = j;
                else
                    _epos[idx].second = j;
            }
        }
        //check_epos();
    }

    void check_epos()
    {
#ifndef NDEBUG
        for (auto& pes : _edges)
        {
            auto pos = pes.first;
            auto& es = pes.second;
            for (size_t j = 0; j < es.size(); ++j)
            {
                assert(es[j].second < _epos.size());
                if (j < pos)
                    assert(_epos[es[j].second].first == j);
                else
                    assert(_epos[es[j].second].second == j);
            }
        }
#endif
    }

    // manipulation functions
    friend std::pair<vertex_iterator, vertex_iterator>
    vertices<>(const adj_list<Vertex>& g);

    friend std::pair<edge_iterator, edge_iterator>
    edges<>(const adj_list<Vertex>& g);

    friend std::pair<edge_descriptor, bool>
    edge<>(Vertex s, Vertex t, const adj_list<Vertex>& g);

    friend size_t out_degree<>(Vertex v, const adj_list<Vertex>& g);

    friend size_t in_degree<>(Vertex v, const adj_list<Vertex>& g);

    friend size_t degree<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<out_edge_iterator, out_edge_iterator>
    out_edges<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<in_edge_iterator, in_edge_iterator>
    in_edges<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<out_edge_iterator, out_edge_iterator>
    _all_edges_out<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<in_edge_iterator, in_edge_iterator>
    _all_edges_in<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<all_edge_iterator, all_edge_iterator>
    all_edges<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<all_edge_iterator_reversed, all_edge_iterator_reversed>
    _all_edges_reversed<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<adjacency_iterator, adjacency_iterator>
    adjacent_vertices<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<adjacency_iterator, adjacency_iterator>
    out_neighbours<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<adjacency_iterator, adjacency_iterator>
    in_neighbours<>(Vertex v, const adj_list<Vertex>& g);

    friend std::pair<adjacency_iterator, adjacency_iterator>
    all_neighbours<>(Vertex v, const adj_list<Vertex>& g);

    friend size_t num_vertices<>(const adj_list<Vertex>& g);

    friend size_t num_edges<>(const adj_list<Vertex>& g);

    friend Vertex add_vertex<>(adj_list<Vertex>& g);

    template <class V, class Pred>
    friend void clear_vertex(V v, adj_list<V>& g, Pred&& pred);

    friend void remove_vertex<>(Vertex v, adj_list<Vertex>& g);

    friend void remove_vertex_fast<>(Vertex v, adj_list<Vertex>& g);

    friend std::pair<edge_descriptor, bool>
    add_edge<>(Vertex s, Vertex t, adj_list<Vertex>& g);

    friend void remove_edge<>(Vertex s, Vertex t, adj_list<Vertex>& g);

    friend void remove_edge<>(const edge_descriptor& e, adj_list<Vertex>& g);
};

//========================================================================
// Graph traits and BGL scaffolding
//========================================================================

struct adj_list_traversal_tag
    : public vertex_list_graph_tag,
      public edge_list_graph_tag,
      public adjacency_graph_tag,
      public bidirectional_graph_tag,
      public adjacency_matrix_tag {};

template <class Vertex>
struct graph_traits<adj_list<Vertex> >
{
    typedef Vertex vertex_descriptor;
    typedef typename adj_list<Vertex>::edge_descriptor edge_descriptor;
    typedef typename adj_list<Vertex>::edge_iterator edge_iterator;
    typedef typename adj_list<Vertex>::adjacency_iterator adjacency_iterator;

    typedef typename adj_list<Vertex>::out_edge_iterator out_edge_iterator;
    typedef typename adj_list<Vertex>::in_edge_iterator in_edge_iterator;

    typedef typename adj_list<Vertex>::vertex_iterator vertex_iterator;

    typedef bidirectional_tag directed_category;
    typedef allow_parallel_edge_tag edge_parallel_category;
    typedef adj_list_traversal_tag traversal_category;

    typedef Vertex vertices_size_type;
    typedef Vertex edges_size_type;
    typedef size_t degree_size_type;

    static Vertex null_vertex() { return adj_list<Vertex>::null_vertex(); }

private:
    BOOST_STATIC_ASSERT((is_convertible<typename std::iterator_traits<out_edge_iterator>::iterator_category,
                                        std::random_access_iterator_tag>::value));
    BOOST_STATIC_ASSERT((is_convertible<typename std::iterator_traits<in_edge_iterator>::iterator_category,
                                        std::random_access_iterator_tag>::value));
    BOOST_STATIC_ASSERT((is_convertible<typename std::iterator_traits<adjacency_iterator>::iterator_category,
                                        std::random_access_iterator_tag>::value));
};

template <class Vertex>
struct graph_traits<const adj_list<Vertex> >
    : public graph_traits<adj_list<Vertex> >
{
};


template <class Vertex>
struct edge_property_type<adj_list<Vertex> >
{
    typedef void type;
};

template <class Vertex>
struct vertex_property_type<adj_list<Vertex> >
{
    typedef void type;
};

template <class Vertex>
struct graph_property_type<adj_list<Vertex> >
{
    typedef void type;
};

//========================================================================
// Graph access and manipulation functions
//========================================================================

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::vertex_iterator,
          typename adj_list<Vertex>::vertex_iterator>
vertices(const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::vertex_iterator vi_t;
    return {vi_t(0), vi_t(g._edges.size())};
}


template <class Vertex>
inline  __attribute__((flatten))
std::pair<typename adj_list<Vertex>::edge_iterator,
          typename adj_list<Vertex>::edge_iterator>
edges(const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::edge_list_t::const_iterator ei_t;
    typedef typename adj_list<Vertex>::vertex_list_t::const_iterator vi_t;
    ei_t ei_begin, ei_end;
    vi_t last_vi;
    if (g._edges.empty())
    {
        last_vi = g._edges.end();
    }
    else
    {
        ei_begin = g._edges[0].second.begin();
        last_vi = g._edges.end() - 1;
        ei_end = last_vi->second.begin() + last_vi->first;
    }
    typename adj_list<Vertex>::edge_iterator ebegin(g._edges.begin(),
                                                    g._edges.end(),
                                                    g._edges.begin(),
                                                    ei_begin);
    typename adj_list<Vertex>::edge_iterator eend(g._edges.begin(),
                                                  g._edges.end(),
                                                  last_vi,
                                                  ei_end);
    return {ebegin, eend};
}

template <class Vertex>
inline __attribute__((always_inline))
Vertex vertex(size_t i, const adj_list<Vertex>&)
{
    return i;
}

template <class Vertex>
inline
std::pair<typename adj_list<Vertex>::edge_descriptor, bool>
edge(Vertex s, Vertex t, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::edge_descriptor edge_descriptor;
    const auto& pes = g._edges[s];
    auto pos = pes.first;
    const auto& es = pes.second;
    auto end = es.begin() + pos;
    auto iter = std::find_if(es.begin(), end,
                             [&](const auto& e) -> bool {return e.first == t;});
    if (iter != end)
        return {edge_descriptor(s, t, iter->second), true};
    return {edge_descriptor(), false};
}

template <class Vertex>
inline __attribute__((always_inline))
size_t out_degree(Vertex v, const adj_list<Vertex>& g)
{
    const auto& pes = g._edges[v];
    return pes.first;
}

template <class Vertex>
inline __attribute__((always_inline))
size_t in_degree(Vertex v, const adj_list<Vertex>& g)
{
    const auto& pes = g._edges[v];
    auto pos = pes.first;
    auto& es = pes.second;
    return es.size() - pos;
}

template <class Vertex>
inline __attribute__((always_inline))
size_t degree(Vertex v, const adj_list<Vertex>& g)
{
    return g._edges[v].second.size();
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::out_edge_iterator,
          typename adj_list<Vertex>::out_edge_iterator>
out_edges(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::out_edge_iterator ei_t;
    const auto& pes = g._edges[v];
    auto pos = pes.first;
    auto& es = pes.second;
    return {ei_t(v, es.begin()), ei_t(v, es.begin() + pos)};
}

template <class Vertex>
inline  __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::in_edge_iterator,
          typename adj_list<Vertex>::in_edge_iterator>
in_edges(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::in_edge_iterator ei_t;
    const auto& pes = g._edges[v];
    auto pos = pes.first;
    auto& es = pes.second;
    return {ei_t(v, es.begin() + pos), ei_t(v, es.end())};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::out_edge_iterator,
          typename adj_list<Vertex>::out_edge_iterator>
_all_edges_out(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::out_edge_iterator ei_t;
    const auto& pes = g._edges[v];
    auto& es = pes.second;
    return {ei_t(v, es.begin()), ei_t(v, es.end())};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::in_edge_iterator,
          typename adj_list<Vertex>::in_edge_iterator>
_all_edges_in(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::in_edge_iterator ei_t;
    const auto& pes = g._edges[v];
    auto& es = pes.second;
    return {ei_t(v, es.begin()), ei_t(v, es.end())};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::all_edge_iterator,
          typename adj_list<Vertex>::all_edge_iterator>
all_edges(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::all_edge_iterator ei_t;
    const auto& pes = g._edges[v];
    auto& es = pes.second;
    auto pos = es.begin() + pes.first;
    return {ei_t(v, es.begin(), pos), ei_t(v, es.end(), pos)};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::all_edge_iterator_reversed,
          typename adj_list<Vertex>::all_edge_iterator_reversed>
_all_edges_reversed(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::all_edge_iterator_reversed ei_t;
    const auto& pes = g._edges[v];
    auto& es = pes.second;
    auto pos = es.begin() + pes.first;
    return {ei_t(v, es.begin(), pos), ei_t(v, es.end(), pos)};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
out_neighbours(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::adjacency_iterator ai_t;
    const auto& pes = g._edges[v];
    auto pos = pes.first;
    auto& es = pes.second;
    return {ai_t(es.begin()), ai_t(es.begin() + pos)};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
in_neighbours(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::adjacency_iterator ai_t;
    const auto& pes = g._edges[v];
    auto pos = pes.first;
    auto& es = pes.second;
    return {ai_t(es.begin() + pos), ai_t(es.end())};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
all_neighbours(Vertex v, const adj_list<Vertex>& g)
{
    typedef typename adj_list<Vertex>::adjacency_iterator ai_t;
    const auto& pes = g._edges[v];
    auto& es = pes.second;
    return {ai_t(es.begin()), ai_t(es.end())};
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
std::pair<typename adj_list<Vertex>::adjacency_iterator,
          typename adj_list<Vertex>::adjacency_iterator>
adjacent_vertices(Vertex v, const adj_list<Vertex>& g)
{
    return out_neighbours(v, g);
}


template <class Vertex>
inline __attribute__((always_inline))
size_t num_vertices(const adj_list<Vertex>& g)
{
    return g._edges.size();
}

template <class Vertex>
inline __attribute__((always_inline))
size_t num_edges(const adj_list<Vertex>& g)
{
    return g._n_edges;
}


template <class Vertex>
typename std::pair<typename adj_list<Vertex>::edge_descriptor, bool>
add_edge(Vertex s, Vertex t, adj_list<Vertex>& g)
{
    // get index from free list, if available
    Vertex idx;
    if (g._free_indexes.empty())
    {
        idx = g._edge_index_range++;
    }
    else
    {
        idx = g._free_indexes.front();
        g._free_indexes.pop_front();
    }

    // put target on back of source's out-list (middle of total list)
    auto& s_pes = g._edges[s];
    auto& s_pos = s_pes.first;
    auto& s_es = s_pes.second;

    if (s_pos < s_es.size())
    {
        //in-list is not empty: push first element to the back
        s_es.push_back(s_es[s_pos]);
        s_es[s_pos] = {t, idx};
        if (g._keep_epos)
            g._epos[s_es.back().second].second = s_es.size() - 1;
    }
    else
    {
        s_es.emplace_back(t, idx);
    }
    s_pos++;

    // put source on back of target's in-list
    auto& t_es = g._edges[t].second;
    t_es.emplace_back(s, idx);

    g._n_edges++;

    if (g._keep_epos)
    {
        if (idx >= g._epos.size())
            g._epos.resize(idx + 1);
        auto& ei = g._epos[idx];
        ei.first = s_pos - 1;         // out
        ei.second = t_es.size() - 1;  // in

        assert(g._edges[s].second[ei.first].first == t);
        assert(g._edges[t].second[ei.second].first == s);
        //g.check_epos();
    }

    typedef typename adj_list<Vertex>::edge_descriptor edge_descriptor;
    return {edge_descriptor(s, t, idx), true};
}

template <class Vertex>
void remove_edge(Vertex s, Vertex t, adj_list<Vertex>& g)
{
    remove_edge(edge(s, t, g).first, g);
}

template <class Vertex>
void remove_edge(const typename adj_list<Vertex>::edge_descriptor& e,
                 adj_list<Vertex>& g)
{
    auto s = e.s;
    auto t = e.t;
    auto idx = e.idx;
    auto& s_pes = g._edges[s];
    auto& s_pos = s_pes.first;
    auto& s_es  = s_pes.second;
    auto& t_pes = g._edges[t];
    auto& t_pos = t_pes.first;
    auto& t_es  = t_pes.second;

    bool found = false;
    if (!g._keep_epos) // O(k_s + k_t)
    {
        // remove and shift
        auto remove_e = [&] (auto& elist, auto&& begin, auto&& end, auto v)
            {
                auto iter = std::find_if(begin, end,
                                         [&] (const auto& ei) -> bool
                                         { return v == ei.first &&
                                                  idx == ei.second; });
                if (iter != end)
                {
                    elist.erase(iter);
                    found = true;
                }
            };

        remove_e(s_es, s_es.begin(), s_es.begin() + s_pos, t);
        if (found)
            s_pos--;
        remove_e(t_es, t_es.begin() + t_pos, t_es.end(), s);
    }
    else // O(1)
    {
        //g.check_epos();

        if (idx >= g._epos.size())
            return;
        auto& i = g._epos[idx];
        if (i.first >= s_es.size() || s_es[i.first].first != t ||
            i.second >= t_es.size() || t_es[i.second].first != s)
            return;

        // swap with back, and pop back
        auto remove_e = [&] (auto& elist, auto&& begin, auto&& end,
                             auto&& get_pos, bool swap_back)
        {
            auto back_iter = begin + ((end - begin) - 1);
            auto& back = *back_iter;
            auto j = get_pos(idx);
            assert(j < elist.size());
            elist[j] = back;
            get_pos(back.second) = j;
            if (swap_back && end != elist.end())
            {
                // in-edge list; swap middle with very back
                back = elist.back();
                g._epos[back.second].second = back_iter - elist.begin();
            }
            elist.pop_back();
        };

        remove_e(s_es, s_es.begin(), s_es.begin() + s_pos,
                 [&](size_t i) -> auto& {return g._epos[i].first;}, true);
        s_pos--;
        remove_e(t_es, t_es.begin() + t_pos, t_es.end(),
                 [&](size_t i) -> auto& {return g._epos[i].second;}, false);

        found = true;
        //g.check_epos();
    }

    if (found)
    {
        g._free_indexes.push_back(idx);
        g._n_edges--;
    }
}

template <class Vertex>
inline __attribute__((always_inline)) __attribute__((flatten))
Vertex add_vertex(adj_list<Vertex>& g)
{
    g._edges.emplace_back();
    return g._edges.size() - 1;
}

template <class Vertex, class Pred>
void clear_vertex(Vertex v, adj_list<Vertex>& g, Pred&& pred)
{
    typename adj_list<Vertex>::make_out_edge mk_out_edge;
    typename adj_list<Vertex>::make_in_edge mk_in_edge;

    if (!g._keep_epos)
    {
        auto& pos = g._edges[v].first;
        auto& es  = g._edges[v].second;
        for (size_t i = 0; i < es.size(); ++i)
        {
            auto u = es[i].first;
            if (u == v)
                continue;
            auto& u_pos = g._edges[u].first;
            auto& u_es = g._edges[u].second;
            if (i < pos)
            {
                if (!pred(mk_out_edge.def(v, es[i])))
                    continue;

                auto iter =
                    std::remove_if(u_es.begin() + u_pos,
                                   u_es.end(),
                                   [&](auto& e)
                                   {
                                       if (!pred(mk_in_edge.def(v, e)))
                                           return false;
                                       return e.first == v;
                                   });
                u_es.erase(iter, u_es.end());
            }
            else
            {
                if (!pred(mk_in_edge.def(v, es[i])))
                    continue;

                auto iter = std::remove_if(u_es.begin(),
                                           u_es.begin() + u_pos,
                                           [&](auto& e)
                                           {
                                               if (!pred(mk_out_edge.def(v, e)))
                                                   return false;
                                               return e.first == v;
                                           });
                u_es.erase(iter, u_es.begin() + u_pos);
                u_pos = iter - u_es.begin();
            }
        }
        auto iter =
            std::remove_if(es.begin() + pos, es.end(),
                           [&](auto& e)
                           {
                               return pred(mk_in_edge.def(v, e));
                           });
        es.erase(iter, es.end());
        iter =
            std::remove_if(es.begin(), es.begin() + pos,
                           [&](auto& e)
                           {
                               return pred(mk_out_edge.def(v, e));
                           });
        es.erase(iter, es.begin() + pos);
        pos = iter - es.begin();
    }
    else
    {
        auto& pos = g._edges[v].first;
        auto& es = g._edges[v].second;
        std::vector<typename adj_list<Vertex>::edge_descriptor> res;
        res.reserve(es.size());
        for (size_t j = 0; j < es.size(); ++j)
        {
            auto& e = es[j];
            auto ed = (j < pos) ?
                mk_out_edge.def(v, e) :
                mk_in_edge.def(v, e);
            if (!pred(ed) || (j >= pos && e.first == v))
                continue;
            res.push_back(ed);
        }
        for (auto& ed : res)
            remove_edge(ed, g);
        //g.check_epos();
    }
}

template <class Vertex>
void clear_vertex(Vertex v, adj_list<Vertex>& g)
{
    clear_vertex(v, g, [](auto&&){ return true; });
}


// O(V + E)
template <class Vertex>
void remove_vertex(Vertex v, adj_list<Vertex>& g)
{
    clear_vertex(v, g);
    g._edges.erase(g._edges.begin() + v);

    size_t N = g._edges.size();
    #pragma omp parallel for schedule(runtime) if (N > 100)
    for (size_t i = 0; i < N; ++i)
    {
        for (auto& e : g._edges[i].second)
        {
            if (e.first > v)
                e.first--;
        }
    }
}

// O(k + k_last)
template <class Vertex>
void remove_vertex_fast(Vertex v, adj_list<Vertex>& g)
{
    Vertex back = g._edges.size() - 1;

    clear_vertex(v, g);
    if (v < back)
    {
        g._edges[v] = g._edges[back];

        auto pos = g._edges[v].first;
        auto& es = g._edges[v].second;
        for (size_t i = 0; i < es.size(); ++i)
        {
            auto& eu = es[i];
            Vertex u = eu.first;
            if (u == back)
            {
                eu.first = v; // self-loop
            }
            else
            {
                // change label in adjacent lists
                if (!g._keep_epos)
                {
                    auto u_pos = g._edges[u].first;
                    auto& u_es = g._edges[u].second;
                    size_t begin = (i < pos) ? u_pos : 0;
                    size_t end = (i < pos) ? u_es.size() : u_pos;
                    for (size_t j = begin; j < end; ++j)
                    {
                        auto& e = u_es[j];
                        if (e.first == back)
                            e.first = v;
                    }
                }
                else
                {
                    size_t idx = eu.second;
                    auto u_pos = (i < pos) ?
                        g._epos[idx].second :
                        g._epos[idx].first;
                    assert(g._edges[u].second[u_pos].first == back);
                    g._edges[u].second[u_pos].first = v;
                }
            }
        }
    }
    g._edges.pop_back();
}



template <class Vertex>
inline
Vertex source(const typename adj_list<Vertex>::edge_descriptor& e,
              const adj_list<Vertex>&)
{
    return e.s;
}

template <class Vertex>
inline
Vertex target(const typename adj_list<Vertex>::edge_descriptor& e,
              const adj_list<Vertex>&)
{
    return e.t;
}

//========================================================================
// Vertex and edge index property maps
//========================================================================

template <class Vertex>
struct property_map<adj_list<Vertex>, vertex_index_t>
{
    typedef identity_property_map type;
    typedef type const_type;
};

template <class Vertex>
struct property_map<const adj_list<Vertex>, vertex_index_t>
{
    typedef identity_property_map type;
    typedef type const_type;
};

template <class Vertex>
inline identity_property_map
get(vertex_index_t, adj_list<Vertex>&)
{
    return identity_property_map();
}

template <class Vertex>
inline identity_property_map
get(vertex_index_t, const adj_list<Vertex>&)
{
    return identity_property_map();
}

template<class Vertex>
class adj_edge_index_property_map:
    public put_get_helper<Vertex, adj_edge_index_property_map<Vertex> >
{
public:
    typedef typename adj_list<Vertex>::edge_descriptor key_type;
    typedef Vertex reference;
    typedef Vertex value_type;
    typedef boost::readable_property_map_tag category;

    reference operator[](const key_type& k) const {return k.idx;}
};

template <class Vertex>
struct property_map<adj_list<Vertex>, edge_index_t>
{
    typedef adj_edge_index_property_map<Vertex> type;
    typedef type const_type;

};

template <class Vertex>
inline adj_edge_index_property_map<Vertex>
get(edge_index_t, const adj_list<Vertex>&)
{
    return adj_edge_index_property_map<Vertex>();
}

} // namespace boost

// hashing of edge descriptors

namespace std
{

template <class Vertex>
struct hash<boost::detail::adj_edge_descriptor<Vertex>>
{
    template <class Edge>
    std::size_t operator()(Edge const& e) const
    {
        return _h(e.idx);
    }
    std::hash<Vertex> _h;
};

} // namespace std


#endif //GRAPH_ADJACENCY_HH

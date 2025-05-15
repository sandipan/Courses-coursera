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

#ifndef GRAPH_UTIL_HH
#define GRAPH_UTIL_HH

// allow boost::python to bind to std::functions
#include <boost/mpl/vector.hpp>
#include <functional>
namespace boost { namespace python { namespace detail {
    template <class R_, class... PS_, class T=void>
    boost::mpl::vector<R_, PS_...>
    get_signature(std::function<R_ (PS_...)>&, T* = nullptr)
    {
        return boost::mpl::vector<R_, PS_...>();
    }
} } }

#include <boost/graph/graph_traits.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/type_traits/is_convertible.hpp>
#include <string>

#include <boost/functional/hash.hpp>

#include <functional>
#include <random>

#include "graph_selectors.hh"
#include "graph_reverse.hh"
#include "graph_filtered.hh"

namespace graph_tool
{

//
// Metaprogramming
// ===============

// useful metafunction to determine whether a graph is directed or not

struct is_directed
{
    template <class Graph>
    struct apply
    {
        typedef std::is_convertible<typename boost::graph_traits<Graph>::directed_category,
                                    boost::directed_tag> type;
    };
};


// This will count "by hand" the number of vertices on a graph. Always O(V).
struct HardNumVertices
{
    template <class Graph>
    size_t operator()(Graph& g) const
    {
        size_t n = 0;
        typename boost::graph_traits<Graph>::vertex_iterator v_iter, v_begin, v_end;
        std::tie(v_begin, v_end) = vertices(g);
        for (v_iter = v_begin; v_iter != v_end; ++v_iter)
            n++;
        return n;
    }
};

// This will return the number of vertices on a graph, as given by
// num_vertices. Can be O(1).
struct SoftNumVertices
{
    template <class Graph>
    size_t operator()(Graph& g) const { return num_vertices(g); }
};

// This will count "by hand" the number of edges on a graph. Always O(E).
struct HardNumEdges
{
    template <class Graph>
    size_t operator()(Graph& g) const
    {
        size_t n = 0;
        typename boost::graph_traits<Graph>::edge_iterator e_iter, e_begin, e_end;
        std::tie(e_begin, e_end) = edges(g);
        for (e_iter = e_begin; e_iter != e_end; ++e_iter)
            n++;
        return n;
    }
};

// This will return the number of edges on a graph, as given by num_edges. Can
// be O(1).
struct SoftNumEdges
{
    template <class Graph>
    size_t operator()(Graph& g) const { return num_edges(g); }
};

// returns true if vertices u and v are adjacent. This is O(k(u)).
template <class Graph>
bool is_adjacent(typename boost::graph_traits<Graph>::vertex_descriptor u,
                 typename boost::graph_traits<Graph>::vertex_descriptor v,
                 const Graph& g )
{
    for (const auto& e : out_edges_range(u, g))
    {
        if (target(e, g) == v)
            return true;
    }
    return false;
}

// computes the out-degree of a graph, ignoring self-edges
template <class Graph>
inline size_t
out_degree_no_loops(typename boost::graph_traits<Graph>::vertex_descriptor v,
                    const Graph &g)
{
    size_t k = 0;
    typename boost::graph_traits<Graph>::adjacency_iterator a,a_end;
    for (std::tie(a,a_end) = adjacent_vertices(v,g); a != a_end; ++a)
        if (*a != v)
            k++;
    return k;
}

// computes the out-degree of a graph, ignoring self-edges
template <class Graph, class Weights>
inline typename boost::property_traits<Weights>::value_type
out_degree_no_loops_weighted(typename boost::graph_traits<Graph>::vertex_descriptor v,
                             Weights w, const Graph &g)
{
    typename boost::property_traits<Weights>::value_type k = 0;
    typename boost::graph_traits<Graph>::out_edge_iterator e, e_end;
    for (std::tie(e, e_end) = out_edges(v, g); e != e_end; ++e)
        if (target(*e, g) != v)
            k += get(w, *e);
    return k;
}


template <class GraphOrig, class GraphTarget>
void graph_copy(const GraphOrig& g, GraphTarget& gt)
{
    typename boost::property_map<GraphOrig, boost::vertex_index_t>::type index = get(boost::vertex_index, g);
    typedef typename boost::graph_traits<GraphTarget>::vertex_descriptor tvertex_t;
    std::vector<tvertex_t> vmap(num_vertices(g));
    typename boost::graph_traits<GraphOrig>::vertex_iterator v, v_end;
    for (std::tie(v, v_end) = vertices(g); v != v_end; ++v)
        vmap[index[*v]] = add_vertex(gt);

    typename boost::graph_traits<GraphOrig>::edge_iterator e, e_end;
    for (std::tie(e, e_end) = edges(g); e != e_end; ++e)
        add_edge(vmap[index[source(*e, g)]], vmap[index[target(*e, g)]], gt);
}


//
// Parallel loops
// ==============

template <class Graph, class F, size_t thres = OPENMP_MIN_THRESH>
void parallel_vertex_loop_no_spawn(const Graph& g, F&& f)
{
    size_t N = num_vertices(g);
    #pragma omp for schedule(runtime)
    for (size_t i = 0; i < N; ++i)
    {
        auto v = vertex(i, g);
        if (!is_valid_vertex(v, g))
            continue;
        f(v);
    }
}

template <class Graph, class F, size_t thres = OPENMP_MIN_THRESH>
void parallel_vertex_loop(const Graph& g, F&& f)
{
    #pragma omp parallel if (num_vertices(g) > thres)
    {
        parallel_vertex_loop_no_spawn<Graph, F, thres>(g, std::forward<F>(f));
    }
}

template <class Graph>
const auto& get_dir(const Graph& g, std::true_type)
{ return g; }

template <class Graph>
const auto& get_dir(const Graph& g, std::false_type)
{ return g.original_graph(); }

template <class Graph, class EPred, class VPred>
auto get_dir(const boost::filt_graph<Graph, EPred, VPred>& g,
             std::false_type)
{
    typedef typename
        std::remove_reference<decltype(g._g.original_graph())>::type g_t;
    return boost::filt_graph<g_t, EPred, VPred>(g._g.original_graph(),
                                                g._edge_pred,
                                                g._vertex_pred);
}

template <class Graph, class F, size_t thres = OPENMP_MIN_THRESH>
void parallel_edge_loop_no_spawn(const Graph& g, F&& f)
{
    auto&& u = get_dir(g, typename is_directed::apply<Graph>::type());
    typedef typename std::remove_const
        <typename std::remove_reference<decltype(u)>::type>::type graph_t;
    static_assert(is_directed::apply<graph_t>::type::value,
                  "graph must be directed at this point");
    auto dispatch =
        [&](auto v)
        {
             for (auto e : out_edges_range(v, u))
                 f(e);
        };
    typedef decltype(dispatch) dispatch_t;
    parallel_vertex_loop_no_spawn<graph_t, dispatch_t&, thres>(u, dispatch);
}

template <class Graph, class F, size_t thres = OPENMP_MIN_THRESH>
void parallel_edge_loop(const Graph& g, F&& f)
{
    #pragma omp parallel if (num_vertices(g) > thres)
    {
        parallel_edge_loop_no_spawn<Graph, F, thres>(g, std::forward<F>(f));
    }
}

template <class Container, class F, size_t thres = OPENMP_MIN_THRESH>
void parallel_loop_no_spawn(Container&& v, F&& f)
{
    size_t N = v.size();
    #pragma omp for schedule(runtime)
    for (size_t i = 0; i < N; ++i)
        f(i, v[i]);
}

template <class Container, class F, size_t thres = OPENMP_MIN_THRESH>
void parallel_loop(Container&& v, F&& f)
{
    #pragma omp parallel if (v.size() > thres)
    {
        parallel_loop_no_spawn<Container, F, thres>(std::forward<Container>(v),
                                                    std::forward<F>(f));
    }
}

} // namespace graph_tool

namespace std
{
// STL omission?
inline bool max(const bool& a, const bool& b) { return a || b; }
}

//
// Data type string representation
// ===============================
//
// String representation of individual data types. We have to take care
// specifically that no information is lost with floating point I/O.
//
// These are implemented in graph_io.cc.

namespace boost
{

template <>
std::string lexical_cast<std::string,uint8_t>(const uint8_t& val);
template <>
uint8_t lexical_cast<uint8_t,std::string>(const std::string& val);
template <>
std::string lexical_cast<std::string,double>(const double& val);
template <>
double lexical_cast<double,std::string>(const std::string& val);
template <>
std::string lexical_cast<std::string,long double>(const long double& val);
template <>
long double lexical_cast<long double,std::string>(const std::string& val);
}

// std::vector<> stream i/o
namespace std
{
template <class Type>
ostream& operator<<(ostream& out, const std::vector<Type>& vec)
{
    for (size_t i = 0; i < vec.size(); ++i)
    {
        out << boost::lexical_cast<std::string>(vec[i]);
        if (i < vec.size() - 1)
            out << ", ";
    }
    return out;
}

template <class Type>
istream& operator>>(istream& in, std::vector<Type>& vec)
{
    using namespace boost;
    using namespace boost::algorithm;

    vec.clear();
    std::string data;
    getline(in, data);
    if (data == "")
        return in; // empty std::strings are OK
    std::vector<std::string> split_data;
    split(split_data, data, is_any_of(","));
    for (size_t i = 0; i < split_data.size(); ++i)
    {
        trim(split_data[i]);
        vec.push_back(lexical_cast<Type>(split_data[i]));
    }
    return in;
}

// std::string vectors need special attention, since separators must be properly
// escaped.
template <>
ostream& operator<<(ostream& out, const std::vector<std::string>& vec);

template <>
istream& operator>>(istream& in, std::vector<std::string>& vec);

} // std namespace

// This will iterate over a random permutation of a random access sequence, by
// swapping the values of the sequence as it iterates
template <class RandomAccessIterator, class RNG,
          class RandomDist = std::uniform_int_distribution<size_t>>
class random_permutation_iterator : public
    std::iterator<std::input_iterator_tag, typename RandomAccessIterator::value_type>
{
public:
    random_permutation_iterator(RandomAccessIterator begin,
                                RandomAccessIterator end, RNG& rng)
        : _i(begin), _end(end), _rng(&rng)
    {
        if(_i != _end)
        {
            RandomDist random(0,  _end - _i - 1);
            std::iter_swap(_i, _i + random(*_rng));
        }
    }

    typename RandomAccessIterator::value_type operator*()
    {
        return *_i;
    }

    random_permutation_iterator& operator++()
    {
        ++_i;
        if(_i != _end)
        {
            RandomDist random(0,  _end - _i - 1);
            std::iter_swap(_i, _i + random(*_rng));
        }
        return *this;
    }

    bool operator==(const random_permutation_iterator& ri)
    {
        return _i == ri._i;
    }

    bool operator!=(const random_permutation_iterator& ri)
    {
        return _i != ri._i;
    }

    size_t operator-(const random_permutation_iterator& ri)
    {
        return _i - ri._i;
    }

private:
    RandomAccessIterator _i, _end;
    RNG* _rng;
};


//
// Useful hash<> specializations
//

namespace std
{

template <class Val>
void _hash_combine(size_t& seed, const Val& hash)
{
    seed ^= std::hash<Val>()(hash) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

template <size_t pos, class... T>
struct tuple_combine
{
    void operator()(size_t& seed, const std::tuple<T...>& v) const
    {
        std::_hash_combine(seed, std::get<pos-1>(v));
        tuple_combine<pos-1, T...>()(seed, v);
    }
};

template <class... T>
struct tuple_combine<0, T...>
{
    void operator()(size_t&, const std::tuple<T...>&) const {}
};

template <class... T>
struct hash<std::tuple<T...>>
{
    size_t operator()(std::tuple<T...> const& v) const
    {
        std::size_t seed = 0;
        tuple_combine<sizeof...(T), T...>()(seed, v);
        return seed;
    }
};

template <class T1, class T2>
struct hash<std::pair<T1, T2>>
{
    size_t operator()(std::pair<T1, T2> const& v) const
    {
        std::size_t seed = 0;
        std::_hash_combine(seed, v.first);
        std::_hash_combine(seed, v.second);
        return seed;
    }
};

template <class Value, class Allocator>
struct hash<std::vector<Value, Allocator>>
{
    size_t operator()(const std::vector<Value, Allocator>& v) const
    {
        size_t seed = 0;
        for (const auto& x : v)
            std::_hash_combine(seed, x);
        return seed;
    }
};

}

#endif // GRAPH_UTIL_HH

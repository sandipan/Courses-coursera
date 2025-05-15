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
#include "graph_python_interface.hh"

#include <boost/python.hpp>
#include <boost/graph/dijkstra_shortest_paths_no_color_map.hpp>

#include "graph.hh"
#include "graph_selectors.hh"
#include "graph_util.hh"

#include "coroutine.hh"
#include "graph_python_interface.hh"

using namespace std;
using namespace boost;
using namespace graph_tool;


class DJKVisitorWrapper
{
public:
    DJKVisitorWrapper(GraphInterface& gi, python::object vis)
        : _gi(gi), _vis(vis) {}

    template <class Vertex, class Graph>
    void initialize_vertex(Vertex u, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("initialize_vertex")(PythonVertex<Graph>(gp, u));
    }

    template <class Vertex, class Graph>
    void discover_vertex(Vertex u, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("discover_vertex")(PythonVertex<Graph>(gp, u));
    }

    template <class Vertex, class Graph>
    void examine_vertex(Vertex u, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("examine_vertex")(PythonVertex<Graph>(gp, u));
    }

    template <class Edge, class Graph>
    void examine_edge(Edge e, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("examine_edge")(PythonEdge<Graph>(gp, e));
    }

    template <class Edge, class Graph>
    void edge_relaxed(Edge e, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("edge_relaxed")(PythonEdge<Graph>(gp, e));
    }

    template <class Edge, class Graph>
    void edge_not_relaxed(Edge e, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("edge_not_relaxed")(PythonEdge<Graph>(gp, e));
    }

    template <class Vertex, class Graph>
    void finish_vertex(Vertex u, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _vis.attr("finish_vertex")(PythonVertex<Graph>(gp, u));
    }

private:
    GraphInterface& _gi;
    boost::python::object _vis;
};


class DJKCmp
{
public:
    DJKCmp() {}
    DJKCmp(python::object cmp): _cmp(cmp) {}

    template <class Value1, class Value2>
    bool operator()(const Value1& v1, const Value2& v2) const
    {
        return python::extract<bool>(_cmp(v1, v2));
    }

private:
    python::object _cmp;
};

class DJKCmb
{
public:
    DJKCmb() {}
    DJKCmb(python::object cmb): _cmb(cmb) {}

    template <class Value1, class Value2 >
    Value1 operator()(const Value1& v1, const Value2& v2) const
    {
        return python::extract<Value1>(_cmb(v1, v2));
    }

private:
    python::object _cmb;
};

struct do_djk_search
{
    template <class Graph, class DistanceMap, class PredMap, class Visitor>
    void operator()(const Graph& g, size_t s, DistanceMap dist,
                    PredMap pred_map, boost::any aweight,
                    Visitor vis, const DJKCmp& cmp, const DJKCmb& cmb,
                    pair<python::object, python::object> range) const
    {
        typedef typename property_traits<DistanceMap>::value_type dtype_t;
        dtype_t z = python::extract<dtype_t>(range.first);
        dtype_t i = python::extract<dtype_t>(range.second);
        typedef typename graph_traits<Graph>::edge_descriptor edge_t;
        DynamicPropertyMapWrap<dtype_t, edge_t> weight(aweight,
                                                       edge_properties());

        if (vertex(s, g) == graph_traits<Graph>::null_vertex())
        {
            for (auto u : vertices_range(g))
            {
                vis.initialize_vertex(u, g);
                put(dist, u, i);
                put(pred_map, u, u);
            }
            for (auto u : vertices_range(g))
            {
                if (dist[u] != i)
                    continue;
                dist[u] = z;
                dijkstra_shortest_paths_no_color_map_no_init
                    (g, u, pred_map, dist, weight, get(vertex_index_t(), g),
                     cmp, cmb, i, z, vis);
            }
        }
        else
        {
            dijkstra_shortest_paths_no_color_map
                (g, vertex(s, g), visitor(vis).weight_map(weight).
                 predecessor_map(pred_map).
                 distance_map(dist).distance_compare(cmp).
                 distance_combine(cmb).distance_inf(i).distance_zero(z));
        }
    }
};

struct do_djk_search_fast
{
    template <class Graph, class DistanceMap, class WeightMap, class Visitor>
    void operator()(const Graph& g, size_t s, DistanceMap dist,
                    WeightMap weight, Visitor vis,
                    pair<python::object, python::object> range) const
    {
        typedef typename property_traits<DistanceMap>::value_type dtype_t;
        dtype_t z = python::extract<dtype_t>(range.first);
        dtype_t i = python::extract<dtype_t>(range.second);

        if (vertex(s, g) == graph_traits<Graph>::null_vertex())
        {
            for (auto u : vertices_range(g))
            {
                vis.initialize_vertex(u, g);
                put(dist, u, i);
            }
            for (auto u : vertices_range(g))
            {
                if (dist[u] != i)
                    continue;
                dist[u] = z;
                dijkstra_shortest_paths_no_color_map_no_init
                    (g, u, dummy_property_map(), dist, weight,
                     get(vertex_index_t(), g), std::less<dtype_t>(),
                     boost::closed_plus<dtype_t>(), i, z, vis);
            }
        }
        else
        {
            dijkstra_shortest_paths_no_color_map
                (g, vertex(s, g), visitor(vis).weight_map(weight).
                 distance_map(dist).distance_inf(i).distance_zero(z));
        }
    }
};


void dijkstra_search(GraphInterface& g, size_t source, boost::any dist_map,
                     boost::any pred_map, boost::any weight, python::object vis,
                     python::object cmp, python::object cmb,
                     python::object zero, python::object inf)
{
    typedef typename property_map_type::
        apply<int64_t, GraphInterface::vertex_index_map_t>::type pred_t;
    pred_t pred = any_cast<pred_t>(pred_map);
    run_action<graph_tool::all_graph_views, mpl::true_>()
        (g, std::bind(do_djk_search(), std::placeholders::_1, source,
                      std::placeholders::_2, pred, weight,
                      DJKVisitorWrapper(g, vis), DJKCmp(cmp), DJKCmb(cmb),
                      make_pair(zero, inf)),
         writable_vertex_properties())(dist_map);
}

#ifdef HAVE_BOOST_COROUTINE

class DJKGeneratorVisitor : public dijkstra_visitor<>
{
public:
    DJKGeneratorVisitor(GraphInterface& gi,
                        coro_t::push_type& yield)
        : _gi(gi), _yield(yield) {}

    template <class Edge, class Graph>
    void edge_relaxed(const Edge& e, Graph& g)
    {
        auto gp = retrieve_graph_view<Graph>(_gi, g);
        _yield(boost::python::object(PythonEdge<Graph>(gp, e)));
    }

private:
    GraphInterface& _gi;
    coro_t::push_type& _yield;
};

#endif // HAVE_BOOST_COROUTINE

boost::python::object dijkstra_search_generator(GraphInterface& g,
                                                size_t source,
                                                boost::any dist_map,
                                                boost::any weight,
                                                python::object cmp,
                                                python::object cmb,
                                                python::object zero,
                                                python::object inf)
{
#ifdef HAVE_BOOST_COROUTINE
    auto dispatch = [&](auto& yield)
        {
            DJKGeneratorVisitor vis(g, yield);
            run_action<graph_tool::all_graph_views, mpl::true_>()
            (g, std::bind(do_djk_search(), std::placeholders::_1, source,
                          std::placeholders::_2, dummy_property_map(), weight,
                          vis, DJKCmp(cmp), DJKCmb(cmb),
                          make_pair(zero, inf)),
             writable_vertex_properties())(dist_map);
        };
    return boost::python::object(CoroGenerator(dispatch));
#else
    throw GraphException("This functionality is not available because boost::coroutine was not found at compile-time");
#endif
}

boost::python::object dijkstra_search_generator_fast(GraphInterface& g,
                                                     size_t source,
                                                     boost::any dist_map,
                                                     boost::any weight,
                                                     python::object zero, python::object inf)
{
#ifdef HAVE_BOOST_COROUTINE
    auto dispatch = [&](auto& yield)
        {
            DJKGeneratorVisitor vis(g, yield);
            run_action<graph_tool::all_graph_views, mpl::true_>()
            (g, std::bind(do_djk_search_fast(), std::placeholders::_1, source,
                          std::placeholders::_2, std::placeholders::_3,
                          vis, make_pair(zero, inf)),
             writable_vertex_scalar_properties(),
             edge_scalar_properties())(dist_map, weight);
        };
    return boost::python::object(CoroGenerator(dispatch));
#else
    throw GraphException("This functionality is not available because boost::coroutine was not found at compile-time");
#endif
}

class DJKArrayVisitor: public dijkstra_visitor<>
{
public:
    DJKArrayVisitor(std::vector<std::array<size_t, 2>>& edges)
        : _edges(edges) {}

    template <class Edge, class Graph>
    void edge_relaxed(const Edge& e, Graph& g)
    {
        _edges.push_back({source(e, g), target(e,g)});
    }

private:
    std::vector<std::array<size_t, 2>>& _edges;
};


boost::python::object dijkstra_search_array(GraphInterface& g,
                                            size_t source,
                                            boost::any dist_map,
                                            boost::any weight,
                                            python::object cmp,
                                            python::object cmb,
                                            python::object zero,
                                            python::object inf)
{
    std::vector<std::array<size_t, 2>> edges;
    DJKArrayVisitor vis(edges);
    run_action<graph_tool::all_graph_views, mpl::true_>()
        (g, std::bind(do_djk_search(), std::placeholders::_1, source,
                      std::placeholders::_2, dummy_property_map(), weight,
                      vis, DJKCmp(cmp), DJKCmb(cmb),
                      make_pair(zero, inf)),
         writable_vertex_properties())(dist_map);
    return wrap_vector_owned<size_t,2>(edges);
}

boost::python::object dijkstra_search_array_fast(GraphInterface& g,
                                                 size_t source,
                                                 boost::any dist_map,
                                                 boost::any weight,
                                                 python::object zero,
                                                 python::object inf)
{
    std::vector<std::array<size_t, 2>> edges;
    DJKArrayVisitor vis(edges);
    run_action<graph_tool::all_graph_views, mpl::true_>()
        (g, std::bind(do_djk_search_fast(), std::placeholders::_1, source,
                      std::placeholders::_2, std::placeholders::_3,
                      vis, make_pair(zero, inf)),
         writable_vertex_scalar_properties(),
         edge_scalar_properties())(dist_map, weight);
    return wrap_vector_owned<size_t,2>(edges);
}

void export_dijkstra()
{
    using namespace boost::python;
    def("dijkstra_search", &dijkstra_search);
    def("dijkstra_generator", &dijkstra_search_generator);
    def("dijkstra_generator_fast", &dijkstra_search_generator_fast);
    def("dijkstra_array", &dijkstra_search_array);
    def("dijkstra_array_fast", &dijkstra_search_array_fast);
}

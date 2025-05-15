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

#include "graph.hh"
#include "graph_filtering.hh"
#include "random.hh"
#include "coroutine.hh"

#include <boost/graph/vf2_sub_graph_iso.hpp>
#include <graph_python_interface.hh>

using namespace graph_tool;
using namespace boost;
using namespace std;

struct ListMatch
{
    template <class Graph1, class Graph2, class VertexMap>
    struct GetMatch
    {
        GetMatch(const Graph1& sub, const Graph2& g, vector<VertexMap>& vmaps,
                 size_t max_n) : _sub(sub), _g(g), _vmaps(vmaps), _max_n(max_n)
        {}

        template <class CorrespondenceMap1To2,
                  class CorrespondenceMap2To1>
        bool operator()(const CorrespondenceMap1To2& f,
                        const CorrespondenceMap2To1&)
        {
            VertexMap c_vmap(get(vertex_index, _sub));
            auto vmap = c_vmap.get_unchecked(num_vertices(_sub));
            for (auto v : vertices_range(_sub))
            {
                auto w = f[v];
                if (w == graph_traits<Graph2>::null_vertex())
                    return true;
                vmap[v] = w;
            }
            _vmaps.push_back(c_vmap);
            if (_max_n > 0 && _vmaps.size() >= _max_n)
                return false;
            return true;
        }

        const Graph1& _sub;
        const Graph2& _g;

        vector<VertexMap>& _vmaps;
        size_t _max_n;
    };

    template <class Graph1, class Graph2, class VertexMap>
    GetMatch<Graph1, Graph2, VertexMap> get_match(const Graph1& sub,
                                                  const Graph2& g,
                                                  vector<VertexMap>& vmaps,
                                                  size_t max_n)
    {
        return GetMatch<Graph1, Graph2, VertexMap>(sub, g, vmaps, max_n);
    }
};

#ifdef HAVE_BOOST_COROUTINE

typedef graph_tool::coroutines::asymmetric_coroutine<boost::python::object> coro_t;

struct GenMatch
{
    GenMatch(coro_t::push_type& yield): _yield(yield) {}

    template <class Graph1, class Graph2, class VertexMap>
    struct GetMatch
    {
        GetMatch(const Graph1& sub, const Graph2& g,
                 coro_t::push_type& yield)
            : _sub(sub), _g(g), _yield(yield)
        {}

        template <class CorrespondenceMap1To2,
                  class CorrespondenceMap2To1>
        bool operator()(const CorrespondenceMap1To2& f,
                        const CorrespondenceMap2To1&)
        {
            VertexMap c_vmap(get(vertex_index, _sub));
            auto vmap = c_vmap.get_unchecked(num_vertices(_sub));
            for (auto v : vertices_range(_sub))
            {
                auto w = f[v];
                if (w == graph_traits<Graph2>::null_vertex())
                    return true;
                vmap[v] = w;
            }
            _yield(boost::python::object(PythonPropertyMap<VertexMap>(c_vmap)));
            return true;
        }

        const Graph1& _sub;
        const Graph2& _g;
        coro_t::push_type& _yield;
    };

    template <class Graph1, class Graph2, class VertexMap>
    GetMatch<Graph1, Graph2, VertexMap> get_match(const Graph1& sub,
                                                  const Graph2& g,
                                                  vector<VertexMap>&,
                                                  size_t)
    {
        return GetMatch<Graph1, Graph2, VertexMap>(sub, g, _yield);
    }

    coro_t::push_type& _yield;
};

#endif // HAVE_BOOST_COROUTINE

struct get_subgraphs
{
    template <class Graph1, class Graph2, class VertexLabel,
              class EdgeLabel, class VertexMap, class Matcher>
    void operator()(const Graph1& sub, const Graph2& g,
                    VertexLabel vertex_label1, boost::any avertex_label2,
                    EdgeLabel edge_label1, boost::any aedge_label2,
                    vector<VertexMap>& vmaps, size_t max_n, bool induced,
                    bool iso, Matcher m) const
    {
        VertexLabel vertex_label2 = any_cast<VertexLabel>(avertex_label2);
        EdgeLabel edge_label2 = any_cast<EdgeLabel>(aedge_label2);

        auto matcher = m.get_match(sub, g, vmaps,max_n);

        typedef typename graph_traits<Graph1>::vertex_descriptor vertex_t;
        vector<vertex_t> vorder;
        std::copy(vertices(sub).first, vertices(sub).second, std::back_inserter(vorder));
        auto cmp = [&](vertex_t u, vertex_t v) -> bool
            {return make_pair(in_degree(u, sub), out_degree(u, sub)) <
                    make_pair(in_degree(v, sub), out_degree(v, sub));};
        std::sort(vorder.begin(), vorder.end(), cmp);

        if (iso)
        {
            vf2_graph_iso(sub, g, matcher, vorder,
                          edges_equivalent(make_property_map_equivalent(edge_label1, edge_label2)).
                          vertices_equivalent(make_property_map_equivalent(vertex_label1, vertex_label2)));
        }
        else
        {
            if (induced)
            {
                vf2_subgraph_iso(sub, g, matcher, vorder,
                                 edges_equivalent(make_property_map_equivalent(edge_label1, edge_label2)).
                                 vertices_equivalent(make_property_map_equivalent(vertex_label1, vertex_label2)));
            }
            else
            {
                vf2_subgraph_mono(sub, g, matcher, vorder,
                                  edges_equivalent(make_property_map_equivalent(edge_label1, edge_label2)).
                                  vertices_equivalent(make_property_map_equivalent(vertex_label1, vertex_label2)));
            }
        }
    }

};

boost::python::object
subgraph_isomorphism(GraphInterface& gi1, GraphInterface& gi2,
                     boost::any vertex_label1, boost::any vertex_label2,
                     boost::any edge_label1, boost::any edge_label2,
                     size_t max_n, bool induced, bool iso, bool generator)
{
    // typedef mpl::push_back<vertex_properties,
    //                        UnityPropertyMap<bool,GraphInterface::vertex_t> >
    //     ::type vertex_props_t;

    // typedef mpl::push_back<edge_properties,
    //                        UnityPropertyMap<bool,GraphInterface::edge_t> >
    //     ::type edge_props_t;

    typedef vprop_map_t<int64_t>::type vlabel_t;
    typedef mpl::vector2<typename vlabel_t::unchecked_t,
                         UnityPropertyMap<bool,
                                          GraphInterface::vertex_t> > vertex_props_t;

    typedef eprop_map_t<int64_t>::type elabel_t;
    typedef mpl::vector2<typename elabel_t::unchecked_t,
                         UnityPropertyMap<bool,
                                          GraphInterface::edge_t> > edge_props_t;


    if (gi1.get_directed() != gi2.get_directed())
        return boost::python::object();

    if (vertex_label1.empty() || vertex_label2.empty())
    {
        vertex_label1 = vertex_label2 =
            UnityPropertyMap<bool,GraphInterface::vertex_t>();
    }
    else
    {
        vertex_label1 = any_cast<vlabel_t>(vertex_label1).get_unchecked(num_vertices(gi1.get_graph()));
        vertex_label2 = any_cast<vlabel_t>(vertex_label2).get_unchecked(num_vertices(gi2.get_graph()));
    }

    if (edge_label1.empty() || edge_label2.empty())
    {
        edge_label1 = edge_label2 =
            UnityPropertyMap<bool,GraphInterface::edge_t>();
    }
    else
    {
        edge_label1 = any_cast<elabel_t>(edge_label1).get_unchecked(gi1.get_edge_index_range());
        edge_label2 = any_cast<elabel_t>(edge_label2).get_unchecked(gi2.get_edge_index_range());
    }

    vector<vlabel_t> vmaps;
    if (!generator)
    {
        gt_dispatch<>()
            (std::bind(get_subgraphs(), std::placeholders::_1, std::placeholders::_2,
                       std::placeholders::_3, vertex_label2, std::placeholders::_4,
                       edge_label2, std::ref(vmaps), max_n, induced, iso,
                       ListMatch()),
             all_graph_views(), all_graph_views(), vertex_props_t(),
             edge_props_t())
            (gi1.get_graph_view(), gi2.get_graph_view(), vertex_label1,
             edge_label1);

        python::list vmapping;
        for (auto& vmap: vmaps)
            vmapping.append(PythonPropertyMap<vlabel_t>(vmap));
        return vmapping;
    }
    else
    {
#ifdef HAVE_BOOST_COROUTINE
        auto dispatch = [&](auto& yield)
            {
                run_action<>()
                    (gi1, std::bind(get_subgraphs(), std::placeholders::_1, std::placeholders::_2,
                                    std::placeholders::_3, vertex_label2, std::placeholders::_4,
                                    edge_label2, std::ref(vmaps), max_n, induced, iso,
                                    GenMatch(yield)),
                     all_graph_views(), vertex_props_t(),
                     edge_props_t())(gi2.get_graph_view(),
                                     vertex_label1, edge_label1);
            };
        CoroGenerator gen(dispatch);
        return boost::python::object(gen);
#else
        throw GraphException("This functionality is not available because boost::coroutine was not found at compile-time");
#endif
    }
}

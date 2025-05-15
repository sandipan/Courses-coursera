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
#include "graph_util.hh"
#include "graph_python_interface.hh"

#include <boost/python.hpp>
#include <boost/python/stl_iterator.hpp>
#include <set>


using namespace std;
using namespace boost;
using namespace graph_tool;

namespace graph_tool
{

struct get_vertex_iterator
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi,
                    python::object& iter) const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        typedef typename graph_traits<Graph>::vertex_iterator vertex_iterator;
        iter = python::object(PythonIterator<Graph, PythonVertex<Graph>,
                                             vertex_iterator>(gp, vertices(g)));
    }
};

python::object get_vertices(GraphInterface& gi)
{
    python::object iter;
    run_action<>()(gi, std::bind(get_vertex_iterator(),
                                 std::placeholders::_1,
                                 std::ref(gi),
                                 std::ref(iter)))();
    return iter;
}

struct get_vertex_soft
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi, size_t i, python::object& v) const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        if (i < num_vertices(g))
            v = python::object(PythonVertex<Graph>(gp, vertex(i, g)));
        else
            v = python::object(PythonVertex<Graph>(gp,
                                                   graph_traits<Graph>::null_vertex()));
    }
};

struct get_vertex_hard
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi, size_t i, python::object& v) const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        size_t c = 0;
        for (auto vi : vertices_range(g))
        {
            if (c == i)
            {
                v = python::object(PythonVertex<Graph>(gp, vi));
                return;
            }
            ++c;
        }
        v = python::object(PythonVertex<Graph>(gp,
                                               graph_traits<Graph>::null_vertex()));
    }
};

python::object get_vertex(GraphInterface& gi, size_t i, bool use_index)
{
    python::object v;
    if (!use_index)
        run_action<>()(gi,
                       std::bind(get_vertex_hard(), std::placeholders::_1,
                                 std::ref(gi), i, std::ref(v)))();
    else
        run_action<>()(gi,
                       std::bind(get_vertex_soft(), std::placeholders::_1,
                                 std::ref(gi), i, std::ref(v)))();
    return v;
}

struct get_edge_iterator
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi, python::object& iter)
        const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        typedef typename graph_traits<Graph>::edge_iterator edge_iterator;
        iter = python::object(PythonIterator<Graph, PythonEdge<Graph>,
                                             edge_iterator>(gp, edges(g)));
    }
};

python::object get_edges(GraphInterface& gi)
{
    python::object iter;
    run_action<>()(gi, std::bind(get_edge_iterator(), std::placeholders::_1,
                                 std::ref(gi), std::ref(iter)))();
    return iter;
}

struct add_new_vertex
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi, size_t n,
                    python::object& new_v) const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        if (n != 1)
        {
            for (size_t i = 0; i < n; ++i)
                add_vertex(g);
            new_v = python::object();
        }
        else
        {
            new_v = python::object(PythonVertex<Graph>(gp, add_vertex(g)));
        }
    }
};


python::object add_vertex(GraphInterface& gi, size_t n)
{
    python::object v;
    run_action<>()(gi, std::bind(add_new_vertex(), std::placeholders::_1,
                                 std::ref(gi), n, std::ref(v)))();
    return v;
}


void remove_vertex_array(GraphInterface& gi, const python::object& oindex, bool fast)
{
    boost::multi_array_ref<int64_t,1> index = get_array<int64_t,1>(oindex);
    auto& g = gi.get_graph();
    if (fast)
    {
        for (auto v : index)
            remove_vertex_fast(vertex(v, g), g);
    }
    else
    {
        for (auto v : index)
            remove_vertex(vertex(v, g), g);
    }
}

void remove_vertex(GraphInterface& gi, size_t v, bool fast)
{
    auto& g = gi.get_graph();
    if (fast)
    {
        remove_vertex_fast(vertex(v, g), g);
    }
    else
    {
        remove_vertex(vertex(v, g), g);
    }
}

struct do_clear_vertex
{
    template <class Graph>
    void operator()(Graph& g, size_t v) const
    {
        clear_vertex(vertex(v, g), g);
    }
};

void clear_vertex(GraphInterface& gi, size_t v)
{
    run_action<>()(gi, std::bind(do_clear_vertex(), std::placeholders::_1, v))();
}

struct add_new_edge
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi, size_t s, size_t t,
                    python::object& new_e) const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        auto e = add_edge(vertex(s, g), vertex(t, g), g).first;
        new_e = python::object(PythonEdge<Graph>(gp, e));
    }
};

python::object add_edge(GraphInterface& gi, size_t s, size_t t)
{
    python::object new_e;
    run_action<>()(gi, std::bind(add_new_edge(), std::placeholders::_1, std::ref(gi),
                                 s, t, std::ref(new_e)))();
    return new_e;
}

struct get_edge_descriptor
{
    template <class Graph>
    void operator()(const Graph&, const python::object& e,
                    typename GraphInterface::edge_t& edge,
                    bool& found)  const
    {
        PythonEdge<Graph>& pe = python::extract<PythonEdge<Graph>&>(e);
        pe.check_valid();
        edge = pe.get_descriptor();
        found = true;
    }
};

void remove_edge(GraphInterface& gi, const python::object& e)
{
    GraphInterface::edge_t de;
    bool found = false;
    run_action<>()(gi, std::bind(get_edge_descriptor(), std::placeholders::_1,
                                 std::ref(e), std::ref(de), std::ref(found)))();
    remove_edge(de, gi.get_graph());
    if (!found)
        throw ValueException("invalid edge descriptor");
}

struct get_edge_dispatch
{
    template <class Graph>
    void operator()(Graph& g, GraphInterface& gi, size_t s, size_t t,
                    bool all_edges, boost::python::list& es) const
    {
        auto gp = retrieve_graph_view<Graph>(gi, g);
        size_t k_t = is_directed::apply<Graph>::type::value ?
            in_degreeS()(t, g) : out_degree(t, g);
        if (out_degree(s, g) <= k_t)
        {
            for (auto e : out_edges_range(vertex(s, g), g))
            {
                if (target(e, g) == vertex(t, g))
                {
                    es.append(PythonEdge<Graph>(gp, e));
                    if (!all_edges)
                        break;
                }
            }
        }
        else
        {
            for (auto e : in_or_out_edges_range(vertex(t, g), g))
            {
                auto w = is_directed::apply<Graph>::type::value ?
                    source(e, g) : target(e, g);
                if (w == vertex(s, g))
                {
                    if (!is_directed::apply<Graph>::type::value && e.s != s)
                        std::swap(e.s, e.t);
                    es.append(PythonEdge<Graph>(gp, e));
                    if (!all_edges)
                        break;
                }
            }
        }
    }
};

python::object get_edge(GraphInterface& gi, size_t s, size_t t, bool all_edges)
{
    python::list es;
    run_action<>()(gi, std::bind(get_edge_dispatch(), std::placeholders::_1,
                                 std::ref(gi), s, t, all_edges,
                                 std::ref(es)))();
    return es;
}


struct get_degree_map
{
    template <class Graph, class DegS, class Weight>
    void operator()(const Graph& g, python::object& odeg_map, DegS deg, Weight weight) const
    {
        typedef typename detail::get_weight_type<Weight>::type weight_t;
        typedef typename mpl::if_<std::is_same<weight_t, size_t>, int32_t, weight_t>::type deg_t;

        typedef typename vprop_map_t<deg_t>::type map_t;

        map_t cdeg_map(get(vertex_index, g));
        typename map_t::unchecked_t deg_map = cdeg_map.get_unchecked(num_vertices(g));

        parallel_vertex_loop
            (g,
             [&](auto v)
             {
                 deg_map[v] = deg(v, g, weight);
             });

        odeg_map = python::object(PythonPropertyMap<map_t>(cdeg_map));
    }
};

python::object GraphInterface::degree_map(string deg, boost::any weight) const
{

    python::object deg_map;

    typedef mpl::push_back<edge_scalar_properties,
                           detail::no_weightS>::type weight_t;
    if (weight.empty())
        weight = detail::no_weightS();

    if (deg == "in")
        run_action<>()(const_cast<GraphInterface&>(*this),
                       std::bind(get_degree_map(), std::placeholders::_1,
                                 std::ref(deg_map), in_degreeS(), std::placeholders::_2), weight_t())
            (weight);
    else if (deg == "out")
        run_action<>()(const_cast<GraphInterface&>(*this),
                       std::bind(get_degree_map(), std::placeholders::_1,
                                 std::ref(deg_map), out_degreeS(), std::placeholders::_2), weight_t())
            (weight);
    else if (deg == "total")
        run_action<>()(const_cast<GraphInterface&>(*this),
                       std::bind(get_degree_map(), std::placeholders::_1,
                                 std::ref(deg_map), total_degreeS(), std::placeholders::_2), weight_t())
            (weight);
    return deg_map;
}

python::object get_vertex_list(GraphInterface& gi)
{
    std::vector<size_t> vlist;
    vlist.reserve(gi.get_num_vertices());
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       for (auto v: vertices_range(g))
                           vlist.push_back(v);
                   })();
    return wrap_vector_owned(vlist);
}

python::object get_edge_list(GraphInterface& gi)
{
    std::vector<size_t> elist;
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       auto edge_index = get(edge_index_t(), g);
                       for (auto e: edges_range(g))
                       {
                           elist.push_back(source(e, g));
                           elist.push_back(target(e, g));
                           elist.push_back(edge_index[e]);
                       }
                   })();
    return wrap_vector_owned(elist);
}

python::object get_out_edge_list(GraphInterface& gi, size_t v)
{
    std::vector<size_t> elist;
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       if (!is_valid_vertex(v, g))
                           throw ValueException("invalid vertex: " +
                                                lexical_cast<string>(v));
                       auto edge_index = get(edge_index_t(), g);
                       elist.reserve(3 * out_degree(v, g));
                       for (auto e: out_edges_range(v, g))
                       {
                           elist.push_back(source(e, g));
                           elist.push_back(target(e, g));
                           elist.push_back(edge_index[e]);
                       }
                   })();
    return wrap_vector_owned(elist);
}

python::object get_in_edge_list(GraphInterface& gi, size_t v)
{
    std::vector<size_t> elist;
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       if (!is_valid_vertex(v, g))
                           throw ValueException("invalid vertex: " +
                                                lexical_cast<string>(v));
                       auto edge_index = get(edge_index_t(), g);
                       elist.reserve(3 * in_degree(v, g));
                       for (auto e: in_edges_range(v, g))
                       {
                           elist.push_back(source(e, g));
                           elist.push_back(target(e, g));
                           elist.push_back(edge_index[e]);
                       }
                   })();
    return wrap_vector_owned(elist);
}

python::object get_out_neighbours_list(GraphInterface& gi, size_t v)
{
    std::vector<size_t> vlist;
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       if (!is_valid_vertex(v, g))
                           throw ValueException("invalid vertex: " +
                                                lexical_cast<string>(v));
                       vlist.reserve(out_degree(v, g));
                       for (auto u: out_neighbours_range(v, g))
                           vlist.push_back(u);
                   })();
    return wrap_vector_owned(vlist);
}

python::object get_in_neighbours_list(GraphInterface& gi, size_t v)
{
    std::vector<size_t> vlist;
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       if (!is_valid_vertex(v, g))
                           throw ValueException("invalid vertex: " +
                                                lexical_cast<string>(v));
                       vlist.reserve(in_degree(v, g));
                       for (auto u: in_neighbours_range(v, g))
                           vlist.push_back(u);
                   })();
    return wrap_vector_owned(vlist);
}

python::object get_degree_list(GraphInterface& gi, python::object ovlist,
                               boost::any eprop, bool out)
{
    python::object ret;
    auto vlist = get_array<uint64_t,1>(ovlist);

    typedef UnityPropertyMap<size_t,
                             graph_traits<GraphInterface::multigraph_t>::edge_descriptor>
        empty_t;
    if (eprop.empty())
    {
        eprop = empty_t();
    }
    else
    {
        if (!belongs<edge_scalar_properties>()(eprop))
            throw ValueException("edge weight property map must be of scalar type");
    }

    typedef mpl::push_back<edge_scalar_properties,
                           empty_t>::type eprops_t;

    auto get_degs = [&](auto deg)
        {
            run_action<>()(gi,
                           [&](auto& g, auto& ew)
                           {
                               typedef typename std::remove_reference
                                   <decltype(ew)>::type::value_type val_t;
                               std::vector<val_t> dlist;
                               dlist.reserve(vlist.size());
                               for (auto v : vlist)
                               {
                                   if (!is_valid_vertex(v, g))
                                       throw ValueException("invalid vertex: " +
                                                            lexical_cast<string>(v));
                                   dlist.push_back(val_t(deg(v, g, ew)));
                               }
                               ret = wrap_vector_owned(dlist);
                           }, eprops_t())(eprop);
        };

    if (out)
        get_degs(out_degreeS());
    else
        get_degs(in_degreeS());

    return ret;
}

//
// Below are the functions with will properly register all the types to python,
// for every filter, type, etc.
//

// this will register all the Vertex/Edge classes to python
struct export_python_interface
{
    template <class Graph, class GraphViews>
    void operator()(Graph* gp, python::list vclasses,
                    python::list eclasses, GraphViews) const
    {
        using namespace boost::python;

        class_<PythonVertex<Graph>, bases<VertexBase>> vclass("Vertex", no_init);
        vclass
            .def("__in_degree", &PythonVertex<Graph>::get_in_degree,
                 "Return the in-degree.")
            .def("__weighted_in_degree", &PythonVertex<Graph>::get_weighted_in_degree,
                 "Return the weighted in-degree.")
            .def("__out_degree", &PythonVertex<Graph>::get_out_degree,
                 "Return the out-degree.")
            .def("__weighted_out_degree", &PythonVertex<Graph>::get_weighted_out_degree,
                 "Return the weighted out-degree.")
            .def("in_edges", &PythonVertex<Graph>::in_edges,
                 "Return an iterator over the in-edges.")
            .def("out_edges", &PythonVertex<Graph>::out_edges,
                 "Return an iterator over the out-edges.")
            .def("is_valid", &PythonVertex<Graph>::is_valid,
                 "Return whether the vertex is valid.")
            .def("graph_ptr", &PythonVertex<Graph>::get_graph_ptr)
            .def("graph_type", &PythonVertex<Graph>::get_graph_type)
            .def("__str__", &PythonVertex<Graph>::get_string)
            .def("__int__", &PythonVertex<Graph>::get_index)
            .def("__hash__", &PythonVertex<Graph>::get_hash);

        vclasses.append(vclass);

        class_<PythonEdge<Graph>, bases<EdgeBase>> eclass("Edge", no_init);
        eclass
            .def("source", &PythonEdge<Graph>::get_source,
                 "Return the source vertex.")
            .def("target", &PythonEdge<Graph>::get_target,
                 "Return the target vertex.")
            .def("is_valid", &PythonEdge<Graph>::is_valid,
                 "Return whether the edge is valid.")
            .def("graph_ptr", &PythonEdge<Graph>::get_graph_ptr)
            .def("graph_type", &PythonEdge<Graph>::get_graph_type)
            .def("__str__", &PythonEdge<Graph>::get_string)
            .def("__hash__", &PythonEdge<Graph>::get_hash);

        boost::mpl::for_each<GraphViews>(std::bind(export_python_interface(),
                                                   gp, std::placeholders::_1,
                                                   std::ref(eclass)));

        eclasses.append(eclass);

        typedef typename graph_traits<Graph>::vertex_iterator vertex_iterator;
        class_<PythonIterator<Graph, PythonVertex<Graph>, vertex_iterator> >
            ("VertexIterator", no_init)
            .def("__iter__", objects::identity_function())
            .def("__next__", &PythonIterator<Graph, PythonVertex<Graph>,
                                             vertex_iterator>::next)
            .def("next", &PythonIterator<Graph, PythonVertex<Graph>,
                                         vertex_iterator>::next);

        typedef typename graph_traits<Graph>::edge_iterator edge_iterator;
        class_<PythonIterator<Graph, PythonEdge<Graph>,
                              edge_iterator> >("EdgeIterator", no_init)
            .def("__iter__", objects::identity_function())
            .def("__next__", &PythonIterator<Graph, PythonEdge<Graph>,
                                             edge_iterator>::next)
            .def("next", &PythonIterator<Graph, PythonEdge<Graph>,
                                         edge_iterator>::next);

        typedef typename graph_traits<Graph>::out_edge_iterator
            out_edge_iterator;
        class_<PythonIterator<Graph, PythonEdge<Graph>,
                              out_edge_iterator> >("OutEdgeIterator", no_init)
            .def("__iter__", objects::identity_function())
            .def("__next__", &PythonIterator<Graph, PythonEdge<Graph>,
                                             out_edge_iterator>::next)
            .def("next", &PythonIterator<Graph, PythonEdge<Graph>,
                                         out_edge_iterator>::next);

        typedef typename graph_traits<Graph>::directed_category
            directed_category;
        typedef typename std::is_convertible<directed_category,
                                             boost::directed_tag>::type is_directed;
        if (is_directed::value)
        {
            typedef typename in_edge_iteratorS<Graph>::type in_edge_iterator;
            class_<PythonIterator<Graph, PythonEdge<Graph>,
                                  in_edge_iterator> >("InEdgeIterator", no_init)
                .def("__iter__", objects::identity_function())
                .def("__next__", &PythonIterator<Graph, PythonEdge<Graph>,
                                                 in_edge_iterator>::next)
                .def("next", &PythonIterator<Graph, PythonEdge<Graph>,
                                             in_edge_iterator>::next);
        }
    }

    template <class Graph, class OGraph, class Eclass>
    void operator()(Graph*, OGraph*, Eclass& eclass) const
    {
        std::function<bool(const PythonEdge<Graph>&,
                           const PythonEdge<OGraph>&)> eq =
            [] (const PythonEdge<Graph>& e1,
                const PythonEdge<OGraph>& e2) -> bool { return e1 == e2; };
        std::function<bool(const PythonEdge<Graph>& e1,
                           const PythonEdge<OGraph>&)> ne =
            [] (const PythonEdge<Graph>& e1,
                const PythonEdge<OGraph>& e2) -> bool { return e1 != e2; };
        std::function<bool(const PythonEdge<Graph>&,
                           const PythonEdge<OGraph>&)> gt =
            [] (const PythonEdge<Graph>& e1,
                const PythonEdge<OGraph>& e2) -> bool { return e1 > e2; };
        std::function<bool(const PythonEdge<Graph>&,
                           const PythonEdge<OGraph>&)> lt =
            [] (const PythonEdge<Graph>& e1,
                const PythonEdge<OGraph>& e2) -> bool { return e1 < e2; };
        std::function<bool(const PythonEdge<Graph>&,
                           const PythonEdge<OGraph>&)> ge =
            [] (const PythonEdge<Graph>& e1,
                const PythonEdge<OGraph>& e2) -> bool { return e1 >= e2; };
        std::function<bool(const PythonEdge<Graph>&,
                           const PythonEdge<OGraph>&)> le =
            [] (const PythonEdge<Graph>& e1,
                const PythonEdge<OGraph>& e2) -> bool { return e1 <= e2; };

        eclass
            .def("__eq__", eq)
            .def("__ne__", ne)
            .def("__lt__", lt)
            .def("__gt__", gt)
            .def("__le__", le)
            .def("__ge__", ge);
    }
};

PythonPropertyMap<GraphInterface::vertex_index_map_t>
get_vertex_index(GraphInterface& g)
{
    return PythonPropertyMap<GraphInterface::vertex_index_map_t>
        (g.get_vertex_index());
}

PythonPropertyMap<GraphInterface::edge_index_map_t>
do_get_edge_index(GraphInterface& g)
{
    return PythonPropertyMap<GraphInterface::edge_index_map_t>
        (g.get_edge_index());
}

void do_add_edge_list(GraphInterface& gi, python::object aedge_list,
                      python::object eprops);

void do_add_edge_list_hashed(GraphInterface& gi, python::object aedge_list,
                             boost::any& vertex_map, bool is_str,
                             python::object eprops);

void do_add_edge_list_iter(GraphInterface& gi, python::object edge_list,
                           python::object eprops);

} // namespace graph_tool

// register everything

void export_python_properties();

python::list* _vlist(0);
python::list* _elist(0);

python::list get_vlist()
{
    if (_vlist == nullptr)
        _vlist = new python::list();
    return *_vlist;
}

python::list get_elist()
{
    if (_elist == nullptr)
        _elist = new python::list();
    return *_elist;
}

void export_python_interface()
{
    using namespace boost::python;

    class_<VertexBase>("VertexBase", no_init);
    class_<EdgeBase>("EdgeBase", no_init);

    typedef boost::mpl::transform<graph_tool::all_graph_views,
                                  boost::mpl::quote1<std::add_const> >::type const_graph_views;
    typedef boost::mpl::transform<graph_tool::all_graph_views,
                                  boost::mpl::quote1<std::add_pointer> >::type all_graph_views;
    typedef boost::mpl::transform<const_graph_views,
                                  boost::mpl::quote1<std::add_pointer> >::type all_const_graph_views;
    typedef boost::mpl::joint_view<all_graph_views, all_const_graph_views>::type graph_views;
    boost::mpl::for_each<graph_views>(std::bind(graph_tool::export_python_interface(),
                                                std::placeholders::_1, get_vlist(),
                                                get_elist(), graph_views()));
    export_python_properties();
    def("new_vertex_property",
        &new_property<GraphInterface::vertex_index_map_t>);
    def("new_edge_property", &new_property<GraphInterface::edge_index_map_t>);
    def("new_graph_property",
        &new_property<ConstantPropertyMap<size_t,graph_property_tag> >);

    def("get_vertex", get_vertex);
    def("get_vertices", get_vertices);
    def("get_edges", get_edges);
    def("add_vertex", graph_tool::add_vertex);
    def("add_edge", graph_tool::add_edge);
    def("remove_vertex", graph_tool::remove_vertex);
    def("remove_vertex_array", graph_tool::remove_vertex_array);
    def("clear_vertex", graph_tool::clear_vertex);
    def("remove_edge", graph_tool::remove_edge);
    def("add_edge_list", graph_tool::do_add_edge_list);
    def("add_edge_list_hashed", graph_tool::do_add_edge_list_hashed);
    def("add_edge_list_iter", graph_tool::do_add_edge_list_iter);
    def("get_edge", get_edge);

    def("get_vertex_list", get_vertex_list);
    def("get_edge_list", get_edge_list);
    def("get_out_edge_list", get_out_edge_list);
    def("get_in_edge_list", get_in_edge_list);
    def("get_out_neighbours_list", get_out_neighbours_list);
    def("get_in_neighbours_list", get_in_neighbours_list);
    def("get_degree_list", get_degree_list);

    def("get_vertex_index", get_vertex_index);
    def("get_edge_index", do_get_edge_index);

    def("get_vlist", get_vlist);
    def("get_elist", get_elist);

#ifdef HAVE_BOOST_COROUTINE
    class_<CoroGenerator>("CoroGenerator", no_init)
        .def("__iter__", objects::identity_function())
        .def("next", &CoroGenerator::next)
        .def("__next__", &CoroGenerator::next);
#endif
}

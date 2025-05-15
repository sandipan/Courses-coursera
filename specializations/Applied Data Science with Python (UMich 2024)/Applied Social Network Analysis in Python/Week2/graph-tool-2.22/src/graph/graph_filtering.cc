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
#include "demangle.hh"

using namespace graph_tool;
using namespace graph_tool::detail;
using namespace boost;
using namespace std;

bool graph_tool::graph_filtering_enabled()
{
    return true;
}

// Whenever no implementation is called, the following exception is thrown
graph_tool::ActionNotFound::ActionNotFound(const type_info& action,
                                           const vector<const type_info*>& args)
    : GraphException(""), _action(action), _args(args)
{
    _error =
        "No static implementation was found for the desired routine. "
        "This is a graph_tool bug. :-( Please submit a bug report at "
        PACKAGE_BUGREPORT ". What follows is debug information.\n\n";

    _error += "Action: " + name_demangle(_action.name()) + "\n\n";
    for (size_t i = 0; i < _args.size(); ++i)
    {
        _error += "Arg " + lexical_cast<string>(i+1) + ": " +
            name_demangle(_args[i]->name()) + "\n\n";
    }
}


// this will check whether a graph is filtered and return the proper view
// encapsulated
template <class Graph, class EdgeFilter, class VertexFilter>
boost::any
check_filtered(const Graph& g, const EdgeFilter& edge_filter,
               const bool& e_invert, bool e_active, size_t max_eindex,
               const VertexFilter& vertex_filter, const bool& v_invert,
               bool v_active, GraphInterface& gi, bool reverse, bool directed)
{

    auto check_filt = [&](auto&& u) -> boost::any
        {
            typedef typename std::remove_const<
                typename std::remove_reference<decltype(u)>::type>::type g_t;
            if (e_active || v_active)
            {
                MaskFilter<EdgeFilter>
                    e_filter(const_cast<EdgeFilter&>(edge_filter),
                             const_cast<bool&>(e_invert));
                MaskFilter<VertexFilter>
                    v_filter(const_cast<VertexFilter&>(vertex_filter),
                             const_cast<bool&>(v_invert));
                if (max_eindex > 0)
                    edge_filter.reserve(max_eindex);
                if (num_vertices(g) > 0)
                    vertex_filter.reserve(num_vertices(g));

                typedef filt_graph<g_t,
                                       MaskFilter<EdgeFilter>,
                                       MaskFilter<VertexFilter>> fg_t;

                fg_t init(u, e_filter, v_filter);
                fg_t& fg = *retrieve_graph_view(gi, init);
                return std::ref(fg);
            }
            else
            {
                return std::ref(const_cast<g_t&>(u));
            }
        };

    auto check_reverse = [&](auto&& u) -> boost::any
        {
            typedef typename std::remove_const<
                typename std::remove_reference<decltype(u)>::type>::type g_t;
            if (reverse)
            {
                typedef typename
                    std::conditional<std::is_const<g_t>::value,
                                     const reversed_graph<typename std::remove_const<g_t>::type>,
                                     reversed_graph<g_t> >::type
                    reversed_graph_t;
                reversed_graph_t rg(u);
                return check_filt(*retrieve_graph_view(gi, rg));
            }
            return check_filt(u);
        };

    auto check_directed = [&](auto&& u) -> boost::any
        {
            typedef typename std::remove_const<
                typename std::remove_reference<decltype(u)>::type>::type g_t;
            if (directed)
                return check_reverse(u);
            typedef undirected_adaptor<g_t> ug_t;
            ug_t ug(u);
            return check_filt(*retrieve_graph_view(gi, ug));
        };

    return check_directed(g);
}

// gets the correct graph view at run time
boost::any GraphInterface::get_graph_view() const
{
    boost::any graph =
        check_filtered(*_mg, _edge_filter_map, _edge_filter_invert,
                       _edge_filter_active, _mg->get_edge_index_range(),
                       _vertex_filter_map, _vertex_filter_invert,
                       _vertex_filter_active,
                       const_cast<GraphInterface&>(*this), _reversed,
                       _directed);
    return graph;
}

// these test whether or not the vertex and edge filters are active
bool GraphInterface::is_vertex_filter_active() const
{ return _vertex_filter_active; }

bool GraphInterface::is_edge_filter_active() const
{ return _edge_filter_active; }


// this function will reindex all the edges, in the order in which they are
// found
void GraphInterface::re_index_edges()
{
    _mg->reindex_edges();
}

// this will definitively remove all the edges from the graph, which are being
// currently filtered out. This will also disable the edge filter
void GraphInterface::purge_edges()
{
    if (!is_edge_filter_active())
        return;

    MaskFilter<edge_filter_t> filter(_edge_filter_map, _edge_filter_invert);
    vector<graph_traits<multigraph_t>::edge_descriptor> deleted_edges;
    for (auto v : vertices_range(*_mg))
    {
        for (auto e : out_edges_range(v, *_mg))
            if (!filter(e))
                deleted_edges.push_back(e);
        for (auto& e  : deleted_edges)
            remove_edge(e, *_mg);
        deleted_edges.clear();
    }
}


// this will definitively remove all the vertices from the graph, which are
// being currently filtered out. This will also disable the vertex filter
void GraphInterface::purge_vertices(boost::any aold_index)
{
    if (!is_vertex_filter_active())
        return;

    typedef vprop_map_t<int32_t>::type index_prop_t;
    index_prop_t old_index = any_cast<index_prop_t>(aold_index);

    MaskFilter<vertex_filter_t> filter(_vertex_filter_map,
                                       _vertex_filter_invert);
    size_t N = num_vertices(*_mg);
    vector<bool> deleted(N, false);
    for (size_t i = 0; i < N; ++i)
        deleted[i] = !filter(vertex(i, *_mg));
    vector<int> old_indexes;

    vector<graph_traits<multigraph_t>::edge_descriptor> edges;

    //remove vertices
    for (int i = N-1; i >= 0; --i)
    {
        if (deleted[i])
        {
            graph_traits<multigraph_t>::vertex_descriptor v =
                vertex(i, *_mg);
            remove_vertex(v, *_mg);
        }
        else
        {
            old_indexes.push_back(i);
        }
    }

    N = old_indexes.size();
    for (int64_t i = N-1; i >= 0; --i)
        old_index[vertex((N - 1) - i, *_mg)] = old_indexes[i];
}

void GraphInterface::set_vertex_filter_property(boost::any property, bool invert)
{
    try
    {
        _vertex_filter_map =
            any_cast<vertex_filter_t::checked_t>(property).get_unchecked();
        _vertex_filter_invert = invert;
        _vertex_filter_active = true;
    }
    catch(bad_any_cast&)
    {
        if (!property.empty())
            throw GraphException("Invalid vertex filter property!");
        _vertex_filter_active = false;
    }
}

void GraphInterface::set_edge_filter_property(boost::any property, bool invert)
{
    try
    {
        _edge_filter_map =
            any_cast<edge_filter_t::checked_t>(property).get_unchecked();
        _edge_filter_invert = invert;
        _edge_filter_active = true;
    }
    catch(bad_any_cast&)
    {
        if (!property.empty())
            throw GraphException("Invalid edge filter property!");
        _edge_filter_active = false;
    }
}

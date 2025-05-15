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

template <class ValueList>
struct add_edge_list
{
    template <class Graph>
    void operator()(Graph& g, python::object aedge_list,
                    python::object& eprops, bool& found) const
    {
        boost::mpl::for_each<ValueList>(std::bind(dispatch(), std::ref(g),
                                                  std::ref(aedge_list),
                                                  std::ref(eprops),
                                                  std::ref(found),
                                                  std::placeholders::_1));
    }

    struct dispatch
    {
        template <class Graph, class Value>
        void operator()(Graph& g, python::object& aedge_list,
                        python::object& oeprops, bool& found, Value) const
        {
            if (found)
                return;
            try
            {
                boost::multi_array_ref<Value, 2> edge_list = get_array<Value, 2>(aedge_list);

                if (edge_list.shape()[1] < 2)
                    throw GraphException("Second dimension in edge list must be of size (at least) two");

                typedef typename graph_traits<Graph>::edge_descriptor edge_t;
                vector<DynamicPropertyMapWrap<Value, edge_t>> eprops;
                python::stl_input_iterator<boost::any> iter(oeprops), end;
                for (; iter != end; ++iter)
                    eprops.emplace_back(*iter, writable_edge_properties());

                size_t n_props = std::min(eprops.size(), edge_list.shape()[1] - 2);

                for (const auto& e : edge_list)
                {
                    size_t s = e[0];
                    size_t t = e[1];
                    while (s >= num_vertices(g) || t >= num_vertices(g))
                        add_vertex(g);
                    auto ne = add_edge(vertex(s, g), vertex(t, g), g).first;
                    for (size_t i = 0; i < n_props; ++i)
                    {
                        try
                        {
                            put(eprops[i], ne, e[i + 2]);
                        }
                        catch(bad_lexical_cast&)
                        {
                            throw ValueException("Invalid edge property value: " +
                                                 lexical_cast<string>(e[i + 2]));
                        }
                    }
                }
                found = true;
            }
            catch (InvalidNumpyConversion& e) {}
        }
    };
};

void do_add_edge_list(GraphInterface& gi, python::object aedge_list,
                      python::object eprops)
{
    typedef mpl::vector<bool, char, uint8_t, uint16_t, uint32_t, uint64_t,
                        int8_t, int16_t, int32_t, int64_t, uint64_t, double,
                        long double> vals_t;
    bool found = false;
    run_action<>()(gi, std::bind(add_edge_list<vals_t>(), std::placeholders::_1,
                                 aedge_list, std::ref(eprops),
                                 std::ref(found)))();
    if (!found)
        throw GraphException("Invalid type for edge list; must be two-dimensional with a scalar type");
}

template <class ValueList>
struct add_edge_list_hash
{
    template <class Graph, class VProp>
    void operator()(Graph& g, python::object aedge_list, VProp vmap,
                    bool& found, bool use_str, python::object& eprops) const
    {
        boost::mpl::for_each<ValueList>(std::bind(dispatch(), std::ref(g),
                                                  std::ref(aedge_list), std::ref(vmap),
                                                  std::ref(found), std::ref(eprops),
                                                  std::placeholders::_1));
        if (!found)
        {
            if (use_str)
                dispatch()(g, aedge_list, vmap, found, eprops, std::string());
            else
                dispatch()(g, aedge_list, vmap, found, eprops, python::object());
        }
    }

    struct dispatch
    {
        template <class Graph, class VProp, class Value>
        void operator()(Graph& g, python::object& aedge_list, VProp& vmap,
                        bool& found, python::object& oeprops, Value) const
        {
            if (found)
                return;
            try
            {
                boost::multi_array_ref<Value, 2> edge_list = get_array<Value, 2>(aedge_list);
                unordered_map<Value, size_t> vertices;

                if (edge_list.shape()[1] < 2)
                    throw GraphException("Second dimension in edge list must be of size (at least) two");

                typedef typename graph_traits<Graph>::edge_descriptor edge_t;
                vector<DynamicPropertyMapWrap<Value, edge_t>> eprops;
                python::stl_input_iterator<boost::any> iter(oeprops), end;
                for (; iter != end; ++iter)
                    eprops.emplace_back(*iter, writable_edge_properties());

                auto get_vertex = [&] (const Value& r) -> size_t
                    {
                        auto iter = vertices.find(r);
                        if (iter == vertices.end())
                        {
                            auto v = add_vertex(g);
                            vertices[r] = v;
                            vmap[v] = lexical_cast<typename property_traits<VProp>::value_type>(r);
                            return v;
                        }
                        return iter->second;
                    };

                for (const auto& e : edge_list)
                {
                    size_t s = get_vertex(e[0]);
                    size_t t = get_vertex(e[1]);
                    auto ne = add_edge(vertex(s, g), vertex(t, g), g).first;
                    for (size_t i = 0; i < e.size() - 2; ++i)
                    {
                        try
                        {
                            put(eprops[i], ne, e[i + 2]);
                        }
                        catch(bad_lexical_cast&)
                        {
                            throw ValueException("Invalid edge property value: " +
                                                 lexical_cast<string>(e[i + 2]));
                        }
                    }
                }
                found = true;
            }
            catch (InvalidNumpyConversion& e) {}
        }

        template <class Graph, class VProp>
        void operator()(Graph& g, python::object& edge_list, VProp& vmap,
                        bool& found, python::object& oeprops, std::string) const
        {
            if (found)
                return;
            try
            {
                unordered_map<std::string, size_t> vertices;

                typedef typename graph_traits<Graph>::edge_descriptor edge_t;
                vector<DynamicPropertyMapWrap<python::object, edge_t>> eprops;
                python::stl_input_iterator<boost::any> piter(oeprops), pend;
                for (; piter != pend; ++piter)
                    eprops.emplace_back(*piter, writable_edge_properties());

                auto get_vertex = [&] (const std::string& r) -> size_t
                    {
                        auto iter = vertices.find(r);
                        if (iter == vertices.end())
                        {
                            auto v = add_vertex(g);
                            vertices[r] = v;
                            vmap[v] = lexical_cast<typename property_traits<VProp>::value_type>(r);
                            return v;
                        }
                        return iter->second;
                    };

                python::stl_input_iterator<python::object> iter(edge_list), end;
                for (; iter != end; ++iter)
                {
                    const auto& row = *iter;

                    python::stl_input_iterator<python::object> eiter(row), eend;

                    size_t s = 0;
                    size_t t = 0;

                    typename graph_traits<Graph>::edge_descriptor e;
                    size_t i = 0;
                    for(; eiter != eend; ++eiter)
                    {
                        if (i >= eprops.size() + 2)
                            break;
                        const auto& val = *eiter;
                        switch (i)
                        {
                        case 0:
                            s = get_vertex(python::extract<std::string>(val));
                            while (s >= num_vertices(g))
                                add_vertex(g);
                            break;
                        case 1:
                            t = get_vertex(python::extract<std::string>(val));
                            while (t >= num_vertices(g))
                                add_vertex(g);
                            e = add_edge(vertex(s, g), vertex(t, g), g).first;
                            break;
                        default:
                            try
                            {
                                put(eprops[i - 2], e, val);
                            }
                            catch(bad_lexical_cast&)
                            {
                                throw ValueException("Invalid edge property value: " +
                                                     python::extract<string>(python::str(val))());
                            }
                        }
                        i++;
                    }
                }
                found = true;
            }
            catch (InvalidNumpyConversion& e) {}
        }

        template <class Graph, class VProp>
        void operator()(Graph& g, python::object& edge_list, VProp& vmap,
                        bool& found, python::object& oeprops, python::object) const
        {
            if (found)
                return;
            try
            {
                unordered_map<python::object, size_t> vertices;

                typedef typename graph_traits<Graph>::edge_descriptor edge_t;
                vector<DynamicPropertyMapWrap<python::object, edge_t>> eprops;
                python::stl_input_iterator<boost::any> piter(oeprops), pend;
                for (; piter != pend; ++piter)
                    eprops.emplace_back(*piter, writable_edge_properties());

                auto get_vertex = [&] (const python::object& r) -> size_t
                    {
                        auto iter = vertices.find(r);
                        if (iter == vertices.end())
                        {
                            auto v = add_vertex(g);
                            vertices[r] = v;
                            vmap[v] = python::extract<typename property_traits<VProp>::value_type>(r);
                            return v;
                        }
                        return iter->second;
                    };

                python::stl_input_iterator<python::object> iter(edge_list), end;
                for (; iter != end; ++iter)
                {
                    const auto& row = *iter;

                    python::stl_input_iterator<python::object> eiter(row), eend;

                    size_t s = 0;
                    size_t t = 0;

                    typename graph_traits<Graph>::edge_descriptor e;
                    size_t i = 0;
                    for(; eiter != eend; ++eiter)
                    {
                        if (i >= eprops.size() + 2)
                            break;
                        const auto& val = *eiter;
                        switch (i)
                        {
                        case 0:
                            s = get_vertex(val);
                            while (s >= num_vertices(g))
                                add_vertex(g);
                            break;
                        case 1:
                            t = get_vertex(val);
                            while (t >= num_vertices(g))
                                add_vertex(g);
                            e = add_edge(vertex(s, g), vertex(t, g), g).first;
                            break;
                        default:
                            try
                            {
                                put(eprops[i - 2], e, val);
                            }
                            catch(bad_lexical_cast&)
                            {
                                throw ValueException("Invalid edge property value: " +
                                                     python::extract<string>(python::str(val))());
                            }
                        }
                        i++;
                    }
                }
                found = true;
            }
            catch (InvalidNumpyConversion& e) {}
        }
    };
};

void do_add_edge_list_hashed(GraphInterface& gi, python::object aedge_list,
                             boost::any& vertex_map, bool is_str,
                             python::object eprops)
{
    typedef mpl::vector<bool, char, uint8_t, uint16_t, uint32_t, uint64_t,
                        int8_t, int16_t, int32_t, int64_t, uint64_t, double,
                        long double> vals_t;
    bool found = false;
    run_action<graph_tool::all_graph_views, boost::mpl::true_>()
        (gi, std::bind(add_edge_list_hash<vals_t>(), std::placeholders::_1,
                       aedge_list, std::placeholders::_2, std::ref(found),
                       is_str, std::ref(eprops)),
         writable_vertex_properties())(vertex_map);
}


struct add_edge_list_iter
{
    template <class Graph>
    void operator()(Graph& g, python::object& edge_list,
                    python::object& oeprops) const
    {
        typedef typename graph_traits<Graph>::edge_descriptor edge_t;
        vector<DynamicPropertyMapWrap<python::object, edge_t>> eprops;
        python::stl_input_iterator<boost::any> piter(oeprops), pend;
        for (; piter != pend; ++piter)
            eprops.emplace_back(*piter, writable_edge_properties());

        python::stl_input_iterator<python::object> iter(edge_list), end;
        for (; iter != end; ++iter)
        {
            const auto& row = *iter;
            python::stl_input_iterator<python::object> eiter(row), eend;

            size_t s = 0;
            size_t t = 0;

            typename graph_traits<Graph>::edge_descriptor e;
            size_t i = 0;
            for(; eiter != eend; ++eiter)
            {
                if (i >= eprops.size() + 2)
                    break;
                const auto& val = *eiter;
                switch (i)
                {
                case 0:
                    s = python::extract<size_t>(val);
                    while (s >= num_vertices(g))
                        add_vertex(g);
                    break;
                case 1:
                    t = python::extract<size_t>(val);
                    while (t >= num_vertices(g))
                        add_vertex(g);
                    e = add_edge(vertex(s, g), vertex(t, g), g).first;
                    break;
                default:
                    try
                    {
                        put(eprops[i - 2], e, val);
                    }
                    catch(bad_lexical_cast&)
                    {
                        throw ValueException("Invalid edge property value: " +
                                             python::extract<string>(python::str(val))());
                    }
                }
                i++;
            }
        }
    }
};

void do_add_edge_list_iter(GraphInterface& gi, python::object edge_list,
                           python::object eprops)
{
    run_action<>()
        (gi, std::bind(add_edge_list_iter(), std::placeholders::_1,
                       std::ref(edge_list), std::ref(eprops)))();
}


} // namespace graph_tool

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

#include "graph_python_interface.hh"
#include "graph.hh"
#include "graph_properties.hh"
#include "graph_filtering.hh"
#include "graph_selectors.hh"
#include "graph_util.hh"

#ifdef USING_OPENMP
#include <omp.h>
#endif

using namespace std;
using namespace boost;
using namespace graph_tool;

template <class Val1, class Val2>
void operator+=(std::vector<Val1>& v1, const std::vector<Val2>& v2)
{
    if (v2.size() > v1.size())
        v1.resize(v2.size());
    for (size_t i = 0; i < v2.size(); ++i)
        v1[i] += v2[i];
}

void operator*=(std::string&, const std::string&)
{
    throw GraphException("Cannot multiply strings.");
}

template <class Val1, class Val2>
void operator*=(std::vector<Val1>& v1, const std::vector<Val2>& v2)
{
    if (v2.size() > v1.size())
        v1.resize(v2.size());
    for (size_t i = 0; i < v2.size(); ++i)
        v1[i] *= v2[i];
}

template <class Val1, class Val2>
bool operator<(const std::vector<Val1>& v1, const std::vector<Val2>& v2)
{
    if (v1.size() != v2.size())
        return v1.size() < v2.size();
    for (size_t i = 0; i < v2.size(); ++i)
    {
        if (v1[i] < v2[i])
            return true;
    }
    return false;
}

struct SumOp
{
    template <class Graph, class Vertex, class EProp, class VProp>
    void operator()(Vertex v, EProp& eprop, VProp& vprop, Graph& g) const
    {
        typedef typename property_traits<EProp>::value_type eval_t;
        typedef typename property_traits<VProp>::value_type vval_t;

        convert<vval_t, eval_t> conv;
        size_t count = 0;
        for (const auto& e : out_edges_range(v, g))
        {
            if (count == 0)
                vprop[v] = conv(eprop[e]);
            else
                vprop[v] += conv(eprop[e]);
            ++count;
        }
    }
};

struct ProdOp
{
    template <class Graph, class Vertex, class EProp, class VProp>
    void operator()(Vertex v, EProp& eprop, VProp& vprop, Graph& g) const
    {
        typedef typename property_traits<EProp>::value_type eval_t;
        typedef typename property_traits<VProp>::value_type vval_t;

        convert<vval_t, eval_t> conv;
        size_t count = 0;
        for (const auto& e : out_edges_range(v, g))
        {
            if (count == 0)
                vprop[v] = conv(eprop[e]);
            else
                vprop[v] *= conv(eprop[e]);
            ++count;
        }
    }
};


struct MinOp
{
    template <class Graph, class Vertex, class EProp, class VProp>
    void operator()(Vertex v, EProp& eprop, VProp& vprop, Graph& g) const
    {
        typedef typename property_traits<EProp>::value_type eval_t;
        typedef typename property_traits<VProp>::value_type vval_t;

        convert<vval_t, eval_t> conv;

        for (const auto& e : out_edges_range(v, g))
        {
            vprop[v] = conv(eprop[e]);
            break;
        }

        for (const auto& e : out_edges_range(v, g))
            vprop[v] = std::min(vprop[v], conv(eprop[e]));
    }
};

struct MaxOp
{
    template <class Graph, class Vertex, class EProp, class VProp>
    void operator()(Vertex v, EProp& eprop, VProp& vprop, Graph& g) const
    {
        typedef typename property_traits<EProp>::value_type eval_t;
        typedef typename property_traits<VProp>::value_type vval_t;

        convert<vval_t, eval_t> conv;

        for (const auto& e : out_edges_range(v, g))
        {
            vprop[v] = conv(eprop[e]);
            break;
        }

        for (const auto& e : out_edges_range(v, g))
            vprop[v] = std::max(vprop[v], conv(eprop[e]));
    }
};

struct do_out_edges_op
{
    template <class Graph, class EProp, class OP>
    void operator()(Graph& g, EProp eprop, boost::any avprop, OP op) const
    {
        typedef typename property_traits<EProp>::value_type eval_t;
        typedef typename property_map_type::apply<
            typename mpl::if_<std::is_same<eval_t, size_t>,
                              int64_t, eval_t>::type,
            GraphInterface::vertex_index_map_t>::type VProp;

        auto vprop = boost::any_cast<VProp>(avprop).get_unchecked(num_vertices(g));

        #ifdef USING_OPENMP
        size_t __attribute__ ((unused)) nt = omp_get_num_threads();
        if (std::is_convertible<eval_t,python::object>::value)
            nt = 1; // python is not thread-safe
        #endif

        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            num_threads(nt)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 op(v, eprop, vprop, g);
             });
    }
};

void out_edges_op(GraphInterface& gi, boost::any eprop, boost::any vprop,
                  std::string op)
{
    if (op == "sum")
    {
        run_action<>()(gi, std::bind(do_out_edges_op(), std::placeholders::_1,
                                     std::placeholders::_2, vprop, SumOp()),
                       edge_properties())
            (eprop);
    }
    else if (op == "prod")
    {
        run_action<>()(gi, std::bind(do_out_edges_op(), std::placeholders::_1,
                                     std::placeholders::_2, vprop, ProdOp()),
                       edge_properties())
            (eprop);
    }
    else if (op == "min")
    {
        run_action<>()(gi, std::bind(do_out_edges_op(), std::placeholders::_1,
                                     std::placeholders::_2, vprop, MinOp()),
                       edge_properties())
            (eprop);
    }
    else if (op == "max")
    {
        run_action<>()(gi, std::bind(do_out_edges_op(), std::placeholders::_1,
                                     std::placeholders::_2, vprop, MaxOp()),
                       edge_properties())
            (eprop);
    }
}

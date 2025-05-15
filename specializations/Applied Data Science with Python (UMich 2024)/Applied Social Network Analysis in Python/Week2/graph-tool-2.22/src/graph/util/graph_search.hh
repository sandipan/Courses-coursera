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

#ifndef GRAPH_SEARCH_HH
#define GRAPH_SEARCH_HH

#include "graph_python_interface.hh"
#include "graph_util.hh"
#include "hash_map_wrap.hh"

#ifdef USING_OPENMP
#include <omp.h>
#include <boost/type_traits.hpp>
#endif


namespace graph_tool
{
using namespace std;
using namespace boost;

// sort sequences lexicographically
template <class ValueType>
bool operator<=(const vector<ValueType>& v1, const vector<ValueType>& v2)
{
    for (size_t i = 0; i < min(v1.size(), v2.size()); ++i)
    {
        if (v1[i] != v2[i])
            return (v1[i] <= v2[i]);
    }
    return (v1.size() <= v2.size());
}

// sort strings in alphabetical (ASCII) order
bool operator<=(const string& s1, const string& s2)
{
    for (size_t i = 0; i < min(s1.size(), s2.size()); ++i)
    {
        if (s1[i] != s2[i])
            return (s1[i] <= s2[i]);
    }
    return (s1.size() <= s2.size());
}

// find vertices which match a certain (inclusive) property range
struct find_vertices
{
    template <class Graph, class DegreeSelector>
    void operator()(Graph& g, GraphInterface& gi, DegreeSelector deg,
                    python::tuple& prange, python::list& ret) const
    {
        typedef typename DegreeSelector::value_type value_type;
        pair<value_type,value_type> range;
        range.first = python::extract<value_type>(prange[0]);
        range.second = python::extract<value_type>(prange[1]);

        #ifdef USING_OPENMP
        size_t __attribute__ ((unused)) nt = omp_get_num_threads();
        if (std::is_convertible<value_type,python::object>::value)
            nt = 1; // python is not thread-safe
        #endif

        auto gp = retrieve_graph_view<Graph>(gi, g);
        bool is_eq = range.first == range.second;

        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) num_threads(nt)
        parallel_vertex_loop_no_spawn
            (g,
             [&](auto v)
             {
                 value_type val = deg(v, g);
                 if ((is_eq && (val == range.first)) ||
                     (!is_eq && (range.first <= val && val <= range.second)))
                 {
                     PythonVertex<Graph> pv(gp, v);
                     auto& ret_ = ret;  // work around clang
                     #pragma omp critical
                     {
                         ret_.append(pv);
                     }
                 }
             });
    }
};

// find edges which match a certain (inclusive) property range
struct find_edges
{
    template <class Graph, class EdgeIndex, class EdgeProperty>
    void operator()(Graph& g, GraphInterface& gi, EdgeIndex eindex,
                    EdgeProperty prop, python::tuple& prange, python::list& ret)
        const
    {
        typedef typename property_traits<EdgeProperty>::value_type value_type;
        pair<value_type,value_type> range;
        range.first = python::extract<value_type>(prange[0]);
        range.second = python::extract<value_type>(prange[1]);

        gt_hash_set<size_t> edge_set;

        #ifdef USING_OPENMP
        size_t __attribute__ ((unused)) nt = omp_get_num_threads();
        if (std::is_convertible<value_type,python::object>::value)
            nt = 1; // python is not thread-safe
        #endif

        auto gp = retrieve_graph_view<Graph>(gi, g);
        bool is_eq = range.first == range.second;

        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            num_threads(nt)
        parallel_edge_loop_no_spawn
            (g,
             [&](auto e)
             {
                 if (!is_directed::apply<Graph>::type::value)
                 {
                     if (edge_set.find(eindex[e]) == edge_set.end())
                         edge_set.insert(eindex[e]);
                    else
                        return;
                 }

                 value_type val = get(prop, e);
                 if ((is_eq && (val == range.first)) ||
                     (!is_eq && (range.first <= val && val <= range.second)))
                 {
                     PythonEdge<Graph> pe(gp, e);
                     auto& ret_ = ret;  // work around clang
                     #pragma omp critical
                     {
                         ret_.append(pe);
                     }
                 }
             });
    }
};


} // graph_tool namespace

#endif // GRAPH_SEARCH_HH

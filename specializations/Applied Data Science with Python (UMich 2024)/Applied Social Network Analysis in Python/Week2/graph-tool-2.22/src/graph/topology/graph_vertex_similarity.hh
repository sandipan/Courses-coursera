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

#ifndef GRAPH_VERTEX_SIMILARITY_HH
#define GRAPH_VERTEX_SIMILARITY_HH

#include "graph_util.hh"

namespace graph_tool
{
using namespace std;
using namespace boost;

template <class Graph, class Vertex, class Mark>
double dice(Vertex u, Vertex v, bool self_loop, Mark& mark, Graph& g)
{
    size_t count = 0;
    for (auto w : adjacent_vertices_range(u, g))
        mark[w] = true;
    if (self_loop)
        mark[u] = true;
    for (auto w : adjacent_vertices_range(v, g))
    {
        if (mark[w])
            count++;
    }
    for (auto w : adjacent_vertices_range(u, g))
        mark[w] = false;
    if (self_loop)
        mark[u] = false;
    return 2 * count / double(out_degree(u, g) + out_degree(v, g));
}

template <class Graph, class Vertex, class Mark>
double jaccard(Vertex u, Vertex v, bool self_loop, Mark& mark, Graph& g)
{
    size_t count = 0, total = 0;
    for (auto w : adjacent_vertices_range(u, g))
    {
        mark[w] = true;
        total++;
    }

    if (self_loop)
        mark[u] = true;

    for (auto w : adjacent_vertices_range(v, g))
    {
        if (mark[w])
            count++;
        else
            total++;
    }

    for (auto w : adjacent_vertices_range(u, g))
        mark[w] = false;
    if (self_loop)
        mark[u] = false;
    return count / double(total);
}

template <class Graph, class Vertex, class Mark>
double inv_log_weighted(Vertex u, Vertex v, Mark& mark, Graph& g)
{
    double count = 0;
    for (auto w : adjacent_vertices_range(u, g))
        mark[w] = true;
    for (auto w : adjacent_vertices_range(v, g))
    {
        if (mark[w])
        {
            if (is_directed::apply<Graph>::type::value)
                count += 1. / log(in_degreeS()(w, g));
            else
                count += 1. / log(out_degree(w, g));
        }
    }
    for (auto w : adjacent_vertices_range(u, g))
        mark[w] = false;
    return count;
}


template <class Graph, class VMap, class Sim>
void all_pairs_similarity(Graph& g, VMap s, Sim&& f)
{
    vector<bool> mask(num_vertices(g), false);
    #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
        firstprivate(mask)
    parallel_vertex_loop_no_spawn
        (g,
         [&](auto v)
         {
             s[v].resize(num_vertices(g));
             for (auto w : vertices_range(g))
                 s[v][w] = f(v, w, mask);
         });
}

template <class Graph, class Vlist, class Slist, class Sim>
void some_pairs_similarity(Graph& g, Vlist& vlist, Slist& slist, Sim&& f)
{
    vector<bool> mask(num_vertices(g), false);
    #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
        firstprivate(mask)
    parallel_loop_no_spawn
        (vlist,
         [&](size_t i, const auto& val)
         {
             size_t u = val[0];
             size_t v = val[1];
             slist[i] = f(u, v, mask);
         });
}

} // graph_tool namespace

#endif // GRAPH_VERTEX_SIMILARITY_HH

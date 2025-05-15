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
#include "graph_properties.hh"
#include "graph_selectors.hh"
#include "graph_util.hh"

#include "random.hh"

#include <boost/python.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct do_maximal_vertex_set
{
    template <class Graph, class VertexIndex, class VertexSet,
              class RNG>
    void operator()(const Graph& g, VertexIndex vertex_index, VertexSet mvs,
                    bool high_deg, RNG& rng) const
    {
        typedef typename graph_traits<Graph>::vertex_descriptor vertex_t;

        VertexSet marked(vertex_index, num_vertices(g));
        vector<vertex_t> vlist;
        double max_deg = 0, tmp_max_deg = 0;
        typename graph_traits<Graph>::vertex_iterator v, v_end;
        for (tie(v, v_end) = vertices(g); v != v_end; ++v)
        {
            vlist.push_back(*v);
            mvs[*v] = marked[*v] = false;
            max_deg = max(out_degree(*v, g), max_deg);
        }

        vector<vertex_t> selected, tmp;
        tmp.reserve(vlist.size());
        selected.reserve(vlist.size());
        while (!vlist.empty())
        {
            selected.clear();
            tmp.clear();
            tmp_max_deg = 0;

            parallel_loop
                (vlist,
                 [&](size_t, auto v)
                 {
                     marked[v] = false;
                     bool include = true;
                     for (auto u : adjacent_vertices_range(v, g))
                     {
                         if (mvs[u])
                         {
                             include = false;
                             break;
                         }
                     }
                     if (!include)
                         return;

                     include = false;
                     if (out_degree(v, g) > 0)
                     {
                         double p, r;
                         if (high_deg)
                             p = out_degree(v, g) / max_deg;
                         else
                             p = 1. / (2 * out_degree(v, g));


                         uniform_real_distribution<> sample(0, 1);
                         auto& rng_ = rng; // workaround clang
                         #pragma omp critical
                         {
                             r = sample(rng_);
                         }
                         if (r < p)
                             include = true;
                     }
                     else
                     {
                         include = true;
                     }

                     if (include)
                     {
                         marked[v] = true;
                         auto& selected_ = selected; // workaround clang
                         #pragma omp critical (selected)
                         {
                             selected_.push_back(v);
                         }
                     }
                     else
                     {
                         auto& tmp_ = tmp;                 // workaround clang
                         auto& tmp_max_deg_ = tmp_max_deg;
                         #pragma omp critical (tmp)
                         {
                             tmp_.push_back(v);
                             tmp_max_deg_ = max(tmp_max_deg_, out_degree(v, g));
                         }
                     }
                 });

            parallel_loop
                (selected,
                 [&](size_t, auto v)
                 {
                     bool include = true;
                     for (auto u : adjacent_vertices_range(v, g))
                     {
                         if (u == v)  //skip self-loops
                             continue;
                         if (mvs[u])
                         {
                             include = false;
                             break;
                         }

                         if (marked[u])
                         {
                             bool inc = ((high_deg && (out_degree(v, g) >
                                                       out_degree(u, g))) ||
                                         (!high_deg && (out_degree(v, g) <
                                                   out_degree(u, g))));
                             if (out_degree(v, g) == out_degree(u, g))
                                 inc = v < u;
                             include = include && inc;
                         }
                     }

                     if (include)
                     {
                         mvs[v] = true;
                     }
                     else
                     {
                         auto& tmp_ = tmp;                 // workaround clang
                         auto& tmp_max_deg_ = tmp_max_deg;
                         #pragma omp critical (tmp)
                         {
                             tmp_.push_back(v);
                             tmp_max_deg_ = max(tmp_max_deg_, out_degree(v, g));
                         }
                     }
                     marked[v] = false;
                 });

            vlist = tmp;
            max_deg = tmp_max_deg;
        }
    }
};

void maximal_vertex_set(GraphInterface& gi, boost::any mvs, bool high_deg,
                        rng_t& rng)
{
    run_action<>()
        (gi, std::bind(do_maximal_vertex_set(), std::placeholders::_1, gi.get_vertex_index(),
                       std::placeholders::_2, high_deg, std::ref(rng)),
         writable_vertex_scalar_properties())(mvs);
}

void export_maximal_vertex_set()
{
    python::def("maximal_vertex_set", &maximal_vertex_set);
}

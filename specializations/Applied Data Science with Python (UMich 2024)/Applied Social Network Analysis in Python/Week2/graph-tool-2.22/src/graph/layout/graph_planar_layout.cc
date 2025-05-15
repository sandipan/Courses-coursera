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
#include "graph_properties.hh"

#include <boost/graph/chrobak_payne_drawing.hpp>
#include <boost/graph/planar_canonical_ordering.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct point_t
{
    size_t x, y;
};

void planar_layout(GraphInterface& gi, boost::any aembed_map, boost::any apos)
{
    run_action<graph_tool::detail::never_directed>()
        (gi,
         [&](auto& g, auto& _embed, auto& _pos)
         {
             typedef typename std::remove_reference<decltype(g)>::type g_t;
             typedef typename graph_traits<g_t>::edge_descriptor edge_t;
             typedef typename graph_traits<g_t>::vertex_descriptor vertex_t;

             auto eindex = get(edge_index, g);
             vector<edge_t> edges;
             for (auto e : edges_range(g))
             {
                 auto ei = eindex[e];
                 if (ei >= edges.size())
                     edges.resize(ei + 1);
                 edges[ei] = e;
             }

             typename vprop_map_t<std::vector<edge_t>>::type::unchecked_t
                 embed(get(vertex_index, g), num_vertices(g));

             parallel_vertex_loop
                 (g,
                  [&](auto& v)
                  {
                      for (auto ei : _embed[v])
                          embed[v].push_back(edges[ei]);
                  });

             vector<vertex_t> ordering;
             planar_canonical_ordering(g, embed, std::back_inserter(ordering));

             assert(ordering.size() >= 3);

             typename vprop_map_t<point_t>::type::unchecked_t
                 pos(get(vertex_index_t(), g), num_vertices(g));

             chrobak_payne_straight_line_drawing(g, embed, ordering.begin(),
                                                 ordering.end(), pos,
                                                 get(vertex_index, g));
             parallel_vertex_loop
                 (g,
                  [&](auto& v)
                  {
                      auto& p = pos[v];
                      typedef typename std::remove_reference<decltype(_pos[v][0])>::type val_t;
                      _pos[v] = {val_t(p.x), val_t(p.y)};
                  });

         },
         vertex_scalar_vector_properties(), vertex_scalar_vector_properties())
        (aembed_map, apos);
}

#include <boost/python.hpp>

void export_planar()
{
    boost::python::def("planar_layout", &planar_layout);
}

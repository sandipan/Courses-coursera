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

#include <boost/python.hpp>

#include "graph_tool.hh"
#include "graph_vertex_similarity.hh"
#include "numpy_bind.hh"

using namespace std;
using namespace boost;
using namespace graph_tool;

void get_dice_similarity(GraphInterface& gi, boost::any as, bool self_loop)
{
    gt_dispatch<>()
        ([&](auto& g, auto& s)
         {
             all_pairs_similarity(g, s,
                                  [&](auto u, auto v, auto& mask)
                                  {
                                      return dice(u, v, self_loop, mask, g);
                                  });
         },
         all_graph_views(), vertex_floating_vector_properties())
        (gi.get_graph_view(), as);
}

void get_dice_similarity_pairs(GraphInterface& gi, python::object opairs,
                               python::object osim, bool self_loop)
{
    multi_array_ref<int64_t,2> pairs = get_array<int64_t,2>(opairs);
    multi_array_ref<double,1> sim = get_array<double,1>(osim);

    gt_dispatch<>()
        ([&](auto& g)
         {
             some_pairs_similarity(g, pairs, sim,
                                   [&](auto u, auto v, auto& mask)
                                   {
                                       return dice(u, v, self_loop, mask, g);
                                   });
         },
         all_graph_views())
        (gi.get_graph_view());
}

void get_jaccard_similarity(GraphInterface& gi, boost::any as, bool self_loop)
{
    gt_dispatch<>()
        ([&](auto& g, auto& s)
         {
             all_pairs_similarity(g, s,
                                  [&](auto u, auto v, auto& mask)
                                  {
                                      return jaccard(u, v, self_loop, mask, g);
                                  });
         },
         all_graph_views(), vertex_floating_vector_properties())
        (gi.get_graph_view(), as);
}

void get_jaccard_similarity_pairs(GraphInterface& gi, python::object opairs,
                                  python::object osim, bool self_loop)
{
    multi_array_ref<int64_t,2> pairs = get_array<int64_t,2>(opairs);
    multi_array_ref<double,1> sim = get_array<double,1>(osim);

    gt_dispatch<>()
        ([&](auto& g)
         {
             some_pairs_similarity(g, pairs, sim,
                                   [&](auto u, auto v, auto& mask)
                                   {
                                       return jaccard(u, v, self_loop, mask, g);
                                   });
         },
         all_graph_views())
        (gi.get_graph_view());
}

void get_inv_log_weight_similarity(GraphInterface& gi, boost::any as)
{
    gt_dispatch<>()
        ([&](auto& g, auto& s)
         {
             all_pairs_similarity(g, s,
                                  [&](auto u, auto v, auto& mask)
                                  {
                                      return inv_log_weighted(u, v, mask, g);
                                  });
         },
         all_graph_views(), vertex_floating_vector_properties())
        (gi.get_graph_view(), as);
}

void get_inv_log_weight_similarity_pairs(GraphInterface& gi,
                                         python::object opairs,
                                         python::object osim)
{
    multi_array_ref<int64_t,2> pairs = get_array<int64_t,2>(opairs);
    multi_array_ref<double,1> sim = get_array<double,1>(osim);

    gt_dispatch<>()
        ([&](auto& g)
         {
             some_pairs_similarity(g, pairs, sim,
                                   [&](auto u, auto v, auto& mask)
                                   {
                                       return inv_log_weighted(u, v,  mask, g);
                                   });
         },
         all_graph_views())
        (gi.get_graph_view());
}


void export_vertex_similarity()
{
    python::def("dice_similarity", &get_dice_similarity);
    python::def("dice_similarity_pairs", &get_dice_similarity_pairs);
    python::def("jaccard_similarity", &get_jaccard_similarity);
    python::def("jaccard_similarity_pairs", &get_jaccard_similarity_pairs);
    python::def("inv_log_weight_similarity", &get_inv_log_weight_similarity);
    python::def("inv_log_weight_similarity_pairs",
                &get_inv_log_weight_similarity_pairs);
};

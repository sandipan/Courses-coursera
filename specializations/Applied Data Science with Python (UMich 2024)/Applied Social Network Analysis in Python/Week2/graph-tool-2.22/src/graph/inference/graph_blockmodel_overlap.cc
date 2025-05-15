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

#include "graph_tool.hh"
#include "random.hh"

#include <boost/python.hpp>

#include "graph_blockmodel_overlap_util.hh"
#include "graph_blockmodel_overlap.hh"
#include "graph_state.hh"

using namespace boost;
using namespace graph_tool;

constexpr size_t overlap_stats_t::_null;

GEN_DISPATCH(overlap_block_state, OverlapBlockState, OVERLAP_BLOCK_STATE_params)

python::object make_overlap_block_state(boost::python::object ostate,
                                        rng_t& rng)
{
    python::object state;
    overlap_block_state::make_dispatch(ostate,
                                       [&](auto& s){state = python::object(s);},
                                       rng);
    return state;
}

void get_eg_overlap(GraphInterface& gi, GraphInterface& egi, boost::any obe,
                    boost::any ob, boost::any onode_index,
                    boost::any ohalf_edges, boost::any oeindex, boost::any orec,
                    boost::any oerec)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    typedef vprop_map_t<int64_t>::type vimap_t;
    typedef vprop_map_t<vector<int64_t>>::type vvmap_t;
    typedef eprop_map_t<vector<int32_t>>::type evmap_t;
    typedef eprop_map_t<int64_t>::type emap_t;
    typedef eprop_map_t<vector<double>>::type ermap_t;

    vmap_t b = any_cast<vmap_t>(ob);
    evmap_t be = any_cast<evmap_t>(obe);
    vimap_t node_index = any_cast<vimap_t>(onode_index);
    vvmap_t half_edges = any_cast<vvmap_t>(ohalf_edges);
    emap_t egindex = any_cast<emap_t>(oeindex);
    ermap_t rec = any_cast<ermap_t>(orec);
    ermap_t erec = any_cast<ermap_t>(oerec);

    run_action<>()(gi,
                   [&](auto& g)
                   {
                       auto& eg = egi.get_graph();
                       auto eindex = get(edge_index, g);
                       for (auto e : edges_range(g))
                       {
                           auto s = get_source(e, g);
                           auto t = get_target(e, g);
                           auto u = add_vertex(eg);
                           auto v = add_vertex(eg);
                           auto ne = add_edge(u, v, eg).first;
                           egindex[ne] = eindex[e];
                           if (be[e].size() != 2)
                               throw GraphException("Edge block property map must have exactly two values per edge");
                           b[u] = be[e][0];
                           b[v] = be[e][1];
                           node_index[u] = s;
                           node_index[v] = t;
                           half_edges[s].push_back(u);
                           half_edges[t].push_back(v);
                           erec[ne] = rec[e];
                       }
                   })();
}

void get_be_from_b_overlap(GraphInterface& gi, boost::any obe, boost::any ob)
{
    typedef vprop_map_t<int32_t>::type    vmap_t;
    typedef eprop_map_t<vector<int32_t>>::type evmap_t;

    vmap_t b = any_cast<vmap_t>(ob);
    evmap_t be = any_cast<evmap_t>(obe);

    run_action<>()(gi,
                   [&](auto& g)
                   {
                       for (auto e : edges_range(g))
                       {
                           auto s = get_source(e, g);
                           auto t = get_target(e, g);
                           be[e] = {b[s], b[t]};
                       }
                   })();
}

struct get_nodeset_overlap
{
    template <class Graph, class VProp, class VVProp>
    void operator()(Graph& g, VProp node_index, VVProp half_edges)
        const
    {
        typedef typename graph_traits<Graph>::vertex_descriptor vertex_t;
        for (auto e : edges_range(g))
        {
            vertex_t s = get_source(e, g);
            vertex_t t = get_target(e, g);
            half_edges[node_index[s]].push_back(s);
            half_edges[node_index[t]].push_back(t);
        }
    }
};

void get_nodeset_overlap(GraphInterface& gi, boost::any onode_index,
                         boost::any ohalf_edges)
{
    typedef vprop_map_t<int64_t>::type vmap_t;
    typedef vprop_map_t<vector<int64_t>>::type vvmap_t;

    vmap_t node_index = any_cast<vmap_t>(onode_index);
    vvmap_t half_edges = any_cast<vvmap_t>(ohalf_edges);

    run_action<>()(gi, [&](auto& g)
                   {
                       for (auto e : edges_range(g))
                       {
                           auto s = get_source(e, g);
                           auto t = get_target(e, g);
                           half_edges[node_index[s]].push_back(s);
                           half_edges[node_index[t]].push_back(t);
                       }
                   })();
}


void export_overlap_blockmodel_state()
{
    using namespace boost::python;

    overlap_block_state::dispatch
        ([&](auto* s)
         {
             typedef typename std::remove_reference<decltype(*s)>::type state_t;

             double (state_t::*virtual_move)(size_t, size_t, size_t,
                                             entropy_args_t) =
                 &state_t::virtual_move;
             size_t (state_t::*sample_block)(size_t, double, rng_t&)
                 = &state_t::sample_block;
             double (state_t::*get_move_prob)(size_t, size_t, size_t, double,
                                              bool)
                 = &state_t::get_move_prob;
             void (state_t::*set_partition)(boost::any&)
                 = &state_t::set_partition;
             void (state_t::*move_vertices)(python::object, python::object) =
                 &state_t::move_vertices;
             void (state_t::*remove_vertex)(size_t) = &state_t::remove_vertex;
             void (state_t::*add_vertex)(size_t, size_t) = &state_t::add_vertex;

             class_<state_t> c(name_demangle(typeid(state_t).name()).c_str(),
                               no_init);
             c.def("remove_vertex", remove_vertex)
                 .def("add_vertex", add_vertex)
                 .def("move_vertex", &state_t::move_vertex)
                 .def("move_vertices", move_vertices)
                 .def("set_partition", set_partition)
                 .def("virtual_move", virtual_move)
                 .def("sample_block", sample_block)
                 .def("entropy", &state_t::entropy)
                 .def("get_partition_dl", &state_t::get_partition_dl)
                 .def("get_deg_dl", &state_t::get_deg_dl)
                 .def("get_move_prob", get_move_prob)
                 .def("enable_partition_stats",
                      &state_t::enable_partition_stats)
                 .def("disable_partition_stats",
                      &state_t::disable_partition_stats)
                 .def("is_partition_stats_enabled",
                      &state_t::is_partition_stats_enabled)
                 .def("get_be_overlap",
                      +[](state_t& state, GraphInterface& gi,
                          boost::any obe)
                      {
                          typedef eprop_map_t<vector<int32_t>>::type evmap_t;
                          evmap_t be = any_cast<evmap_t>(obe);
                          run_action<>()(gi,
                                         [&](auto& g)
                                         {
                                             state.get_be_overlap(g, be);
                                         })();
                      })
                 .def("get_bv_overlap",
                      +[](state_t& state, GraphInterface& gi, boost::any obv,
                          boost::any obc_in, boost::any obc_out,
                          boost::any obc_total)
                      {
                          typedef vprop_map_t<vector<int32_t>>::type vvmap_t;
                          vvmap_t bv = any_cast<vvmap_t>(obv);
                          vvmap_t bc_in = any_cast<vvmap_t>(obc_in);
                          vvmap_t bc_out = any_cast<vvmap_t>(obc_out);
                          vvmap_t bc_total = any_cast<vvmap_t>(obc_total);
                          run_action<>()(gi,
                                         [&](auto& g)
                                         {
                                             state.get_bv_overlap(g, bv, bc_in,
                                                                  bc_out,
                                                                  bc_total);
                                         })();
                      })
                 .def("get_overlap_split",
                      +[](state_t& state, GraphInterface& gi, boost::any obv,
                          boost::any ob)
                      {
                          typedef vprop_map_t<int32_t>::type vmap_t;
                          typedef vprop_map_t<vector<int32_t>>::type vvmap_t;

                          vvmap_t bv = any_cast<vvmap_t>(obv);
                          vmap_t b = any_cast<vmap_t>(ob);
                          run_action<>()(gi,
                                         [&](auto& g)
                                         {
                                             state.get_overlap_split(g, bv, b);
                                         })();
                      })
                 .def("get_maj_overlap",
                      +[](state_t&, GraphInterface& gi, boost::any obv,
                          boost::any obc_total, boost::any ob)
                      {
                          typedef vprop_map_t<int32_t>::type vmap_t;
                          typedef vprop_map_t<vector<int32_t>>::type vvmap_t;

                          vmap_t b = any_cast<vmap_t>(ob);
                          vvmap_t bv = any_cast<vvmap_t>(obv);
                          vvmap_t bc_total = any_cast<vvmap_t>(obc_total);
                          run_action<>()(gi,
                                         [&](auto& g)
                                         {
                                             for (auto v : vertices_range(g))
                                             {
                                                 if (bv[v].empty())
                                                 {
                                                     b[v] = numeric_limits<int32_t>::max();
                                                     continue;
                                                 }
                                                 auto& c = bc_total[v];
                                                 auto pos = std::max_element(c.begin(), c.end());
                                                 auto r = *(bv[v].begin() + (pos - c.begin()));
                                                 b[v] = r;
                                             }
                                         })();
                      });
         });

    def("make_overlap_block_state", &make_overlap_block_state);
    def("get_be_from_b_overlap", &get_be_from_b_overlap);
    def("get_eg_overlap", &get_eg_overlap);
    def("get_nodeset_overlap", &get_nodeset_overlap);
}

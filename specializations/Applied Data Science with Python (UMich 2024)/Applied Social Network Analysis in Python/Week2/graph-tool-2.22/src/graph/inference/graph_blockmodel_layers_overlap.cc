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
#include "graph_blockmodel_layers_util.hh"
#define BASE_STATE_params OVERLAP_BLOCK_STATE_params ((eweight,,,0))
#include "graph_blockmodel_layers.hh"
#include "graph_state.hh"

using namespace boost;
using namespace graph_tool;

GEN_DISPATCH(overlap_block_state, OverlapBlockState, OVERLAP_BLOCK_STATE_params)

template <class BaseState>
GEN_DISPATCH(layered_block_state, Layers<BaseState>::template LayeredBlockState,
             LAYERED_BLOCK_STATE_params)

python::object
make_layered_overlap_block_state(boost::python::object oblock_state,
                                 boost::python::object olayered_state)
{
    python::object state;
    auto dispatch = [&](auto& block_state)
        {
            typedef typename std::remove_reference<decltype(block_state)>::type
            state_t;

            layered_block_state<state_t>::make_dispatch
                (olayered_state,
                 [&](auto& s)
                 {
                     state = python::object(s);
                 },
                 block_state);
        };
    overlap_block_state::dispatch(oblock_state, dispatch);
    return state;
}

void export_layered_overlap_blockmodel_state()
{
    using namespace boost::python;

    overlap_block_state::dispatch
        ([&](auto* bs)
         {
             typedef typename std::remove_reference<decltype(*bs)>::type block_state_t;

             layered_block_state<block_state_t>::dispatch
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
                      void (state_t::*move_vertices)(python::object, python::object) =
                          &state_t::move_vertices;

                      class_<state_t> c(name_demangle(typeid(state_t).name()).c_str(),
                                        no_init);
                      c.def("remove_vertex", &state_t::remove_vertex)
                          .def("add_vertex", &state_t::add_vertex)
                          .def("move_vertex", &state_t::move_vertex)
                          .def("move_vertices", move_vertices)
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
                               &state_t::is_partition_stats_enabled);
                  });
         });

    def("make_layered_overlap_block_state", &make_layered_overlap_block_state);
}

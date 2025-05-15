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

#include "graph_blockmodel_util.hh"
#include "graph_blockmodel.hh"
#include "graph_state.hh"

using namespace boost;
using namespace graph_tool;

GEN_DISPATCH(block_state, BlockState, BLOCK_STATE_params)

using namespace boost::python;

void export_sbm_state()
{
    block_state::dispatch
        ([&](auto* s)
         {
             typedef typename std::remove_reference<decltype(*s)>::type state_t;
             void (state_t::*remove_vertex)(size_t) =
                 &state_t::remove_vertex;
             void (state_t::*add_vertex)(size_t, size_t) =
                 &state_t::add_vertex;
             void (state_t::*move_vertex)(size_t, size_t) =
                 &state_t::move_vertex;
             void (state_t::*remove_vertices)(python::object) =
                 &state_t::remove_vertices;
             void (state_t::*add_vertices)(python::object, python::object) =
                 &state_t::add_vertices;
             void (state_t::*move_vertices)(python::object, python::object) =
                 &state_t::move_vertices;
             double (state_t::*virtual_move)(size_t, size_t, size_t,
                                             entropy_args_t) =
                 &state_t::virtual_move;
             size_t (state_t::*sample_block)(size_t, double, rng_t&) =
                 &state_t::sample_block;
             size_t (state_t::*random_neighbour)(size_t, rng_t&) =
                 &state_t::random_neighbour;
             double (state_t::*get_move_prob)(size_t, size_t, size_t, double,
                                              bool) =
                 &state_t::get_move_prob;
             void (state_t::*merge_vertices)(size_t, size_t) =
                 &state_t::merge_vertices;
             void (state_t::*set_partition)(boost::any&) =
                 &state_t::set_partition;

             class_<state_t> c(name_demangle(typeid(state_t).name()).c_str(),
                               no_init);
             c.def("remove_vertex", remove_vertex)
                 .def("add_vertex", add_vertex)
                 .def("remove_vertices", remove_vertices)
                 .def("add_vertices", add_vertices)
                 .def("move_vertex", move_vertex)
                 .def("move_vertices", move_vertices)
                 .def("set_partition", set_partition)
                 .def("virtual_move", virtual_move)
                 .def("merge_vertices", merge_vertices)
                 .def("sample_block", sample_block)
                 .def("sample_neighbour", random_neighbour)
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
                 .def("couple_state",
                      &state_t::couple_state)
                 .def("decouple_state",
                      &state_t::decouple_state)
                 .def("clear_egroups",
                      &state_t::clear_egroups)
                 .def("rebuild_neighbour_sampler",
                      &state_t::rebuild_neighbour_sampler)
                 .def("sync_emat",
                      &state_t::sync_emat);
         });
}

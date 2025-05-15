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

#include "graph_blockmodel_em.hh"
#include "graph_state.hh"

using namespace boost;
using namespace graph_tool;

GEN_DISPATCH(em_block_state, EMBlockState, EM_BLOCK_STATE_params)

python::object make_em_block_state(boost::python::object ostate, rng_t& rng)
{
    python::object state;
    em_block_state::make_dispatch(ostate,
                                  [&](auto& s){state = python::object(s);},
                                  rng);
    return state;
}

void export_em_blockmodel_state()
{
    using namespace boost::python;

    em_block_state::dispatch
        ([&](auto* s)
         {
             typedef typename std::remove_reference<decltype(*s)>::type state_t;
             class_<state_t> c(name_demangle(typeid(state_t).name()).c_str(),
                               no_init);
             c.def("learn_iter", &state_t::learn_iter)
                 .def("bp_iter", &state_t::bp_iter)
                 .def("bethe_fe", &state_t::bethe_fe)
                 .def("get_MAP", &state_t::get_MAP_any);
         });

    def("make_em_block_state",  make_em_block_state);
}

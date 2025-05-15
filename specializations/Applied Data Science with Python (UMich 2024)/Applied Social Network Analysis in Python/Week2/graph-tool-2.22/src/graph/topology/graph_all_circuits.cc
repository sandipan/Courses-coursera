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

#include <boost/graph/hawick_circuits.hpp>

#include "graph_tool.hh"
#include "numpy_bind.hh"
#include "coroutine.hh"
#include "graph_python_interface.hh"

using namespace std;
using namespace graph_tool;

template <class Yield>
struct CircuitVisitor
{
    CircuitVisitor(Yield& yield)
        : _yield(yield) {}
    Yield& _yield;

    template <class Vs, class Graph>
    void cycle(const Vs& vs, Graph&)
    {
        auto c = wrap_vector_owned(vs);
        _yield(c);
    }
};


boost::python::object get_all_circuits(GraphInterface& gi, bool unique)
{
#ifdef HAVE_BOOST_COROUTINE
    auto dispatch = [&](auto& yield)
        {
            run_action<>()
                (gi,
                 [&](auto& g)
                 {
                     CircuitVisitor<decltype(yield)> visitor(yield);
                     if (unique)
                         hawick_unique_circuits(g, visitor);
                     else
                         hawick_circuits(g, visitor);
                 })();
        };
    return boost::python::object(CoroGenerator(dispatch));
#else
    throw GraphException("This functionality is not available because boost::coroutine was not found at compile-time");
#endif // HAVE_BOOST_COROUTINE
}


void export_all_circuits()
{
    boost::python::def("get_all_circuits", &get_all_circuits);
};

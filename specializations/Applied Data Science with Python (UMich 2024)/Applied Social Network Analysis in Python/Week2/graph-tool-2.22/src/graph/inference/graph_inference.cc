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

#include <boost/python.hpp>
#include "numpy_bind.hh"
#include "hash_map_wrap.hh"

using namespace std;
using namespace boost;
using namespace graph_tool;

template <class Value>
void vector_map(boost::python::object ovals, boost::python::object omap)
{
    multi_array_ref<Value,1> vals = get_array<Value,1>(ovals);
    multi_array_ref<Value,1> map = get_array<Value,1>(omap);

    size_t pos = 0;
    for (size_t i = 0; i < vals.size(); ++i)
    {
        Value v = vals[i];
        if (map[v] == -1)
            map[v] = pos++;
        vals[i] = map[v];
    }
}

template <class Value>
void vector_continuous_map(boost::python::object ovals)
{
    multi_array_ref<Value,1> vals = get_array<Value,1>(ovals);
    gt_hash_map<Value, size_t> map;

    for (size_t i = 0; i < vals.size(); ++i)
    {
        Value v = vals[i];
        auto iter = map.find(v);
        if (iter == map.end())
            iter = map.insert(make_pair(v, map.size())).first;
        vals[i] = iter->second;
    }
}

template <class Value>
void vector_rmap(boost::python::object ovals, boost::python::object omap)
{
    multi_array_ref<Value,1> vals = get_array<Value,1>(ovals);
    multi_array_ref<Value,1> map = get_array<Value,1>(omap);

    for (size_t i = 0; i < vals.size(); ++i)
    {
        map[vals[i]] = i;
    }
}

extern void export_blockmodel_state();
extern void export_blockmodel_mcmc();
extern void export_blockmodel_multicanonical();
extern void export_blockmodel_multiflip_mcmc();
extern void export_blockmodel_merge();
extern void export_blockmodel_gibbs();
extern void export_overlap_blockmodel_state();
extern void export_overlap_blockmodel_mcmc();
extern void export_overlap_blockmodel_mcmc_bundled();
extern void export_overlap_blockmodel_multicanonical();
extern void export_overlap_blockmodel_multiflip_mcmc();
extern void export_overlap_blockmodel_gibbs();
extern void export_overlap_blockmodel_vacate();
extern void export_layered_blockmodel_state();
extern void export_layered_blockmodel_mcmc();
extern void export_layered_blockmodel_merge();
extern void export_layered_blockmodel_gibbs();
extern void export_layered_blockmodel_multicanonical();
extern void export_layered_blockmodel_multiflip_mcmc();
extern void export_layered_overlap_blockmodel_state();
extern void export_layered_overlap_blockmodel_mcmc();
extern void export_layered_overlap_blockmodel_bundled_mcmc();
extern void export_layered_overlap_blockmodel_gibbs();
extern void export_layered_overlap_blockmodel_multicanonical();
extern void export_layered_overlap_blockmodel_multiflip_mcmc();
extern void export_layered_overlap_blockmodel_vacate();
extern void export_em_blockmodel_state();
extern void export_blockmodel_exhaustive();
extern void export_overlap_blockmodel_exhaustive();
extern void export_layered_blockmodel_exhaustive();
extern void export_layered_overlap_blockmodel_exhaustive();
extern void export_marginals();
extern void export_modularity();

BOOST_PYTHON_MODULE(libgraph_tool_inference)
{
    using namespace boost::python;
    export_blockmodel_state();
    export_blockmodel_mcmc();
    export_blockmodel_multicanonical();
    export_blockmodel_multiflip_mcmc();
    export_blockmodel_merge();
    export_blockmodel_gibbs();
    export_overlap_blockmodel_state();
    export_overlap_blockmodel_mcmc();
    export_overlap_blockmodel_mcmc_bundled();
    export_overlap_blockmodel_multicanonical();
    export_overlap_blockmodel_multiflip_mcmc();
    export_overlap_blockmodel_gibbs();
    export_overlap_blockmodel_vacate();
    export_layered_blockmodel_state();
    export_layered_blockmodel_mcmc();
    export_layered_blockmodel_multiflip_mcmc();
    export_layered_blockmodel_merge();
    export_layered_blockmodel_gibbs();
    export_layered_blockmodel_multicanonical();
    export_layered_overlap_blockmodel_state();
    export_layered_overlap_blockmodel_mcmc();
    export_layered_overlap_blockmodel_bundled_mcmc();
    export_layered_overlap_blockmodel_gibbs();
    export_layered_overlap_blockmodel_multicanonical();
    export_layered_overlap_blockmodel_multiflip_mcmc();
    export_layered_overlap_blockmodel_vacate();
    export_em_blockmodel_state();
    export_blockmodel_exhaustive();
    export_overlap_blockmodel_exhaustive();
    export_layered_blockmodel_exhaustive();
    export_layered_overlap_blockmodel_exhaustive();
    export_marginals();
    export_modularity();

    def("vector_map", vector_map<int32_t>);
    def("vector_map64", vector_map<int64_t>);
    def("vector_rmap", vector_rmap<int32_t>);
    def("vector_rmap64", vector_rmap<int64_t>);
    def("vector_continuous_map", vector_continuous_map<int32_t>);
    def("vector_continuous_map64", vector_continuous_map<int64_t>);
}

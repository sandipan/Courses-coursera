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

#ifndef GRAPH_SBM_HH
#define GRAPH_SBM_HH

#include <tuple>
#include <iostream>
#include <boost/functional/hash.hpp>

#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_util.hh"
#include "sampler.hh"

#include "random.hh"

#include "hash_map_wrap.hh"

namespace graph_tool
{
using namespace std;
using namespace boost;

template <class Graph, class VProp, class IVec, class FVec, class VDProp,
          class RNG>
void gen_sbm(Graph& g, VProp b, IVec& rs, IVec& ss, FVec probs, VDProp in_deg,
             VDProp out_deg, RNG& rng)
{
    vector<vector<size_t>> rvs;
    vector<vector<double>> v_in_probs, v_out_probs;
    for (auto v : vertices_range(g))
    {
        size_t r = b[v];
        if (r >= v_in_probs.size())
        {
            v_in_probs.resize(r+1);
            v_out_probs.resize(r+1);
            rvs.resize(r+1);
        }
        rvs[r].push_back(v);
        v_in_probs[r].push_back(in_deg[v]);
        v_out_probs[r].push_back(out_deg[v]);
    }

    vector<Sampler<size_t>> v_in_sampler, v_out_sampler;
    for (size_t r = 0; r < rvs.size(); ++r)
    {
        v_in_sampler.emplace_back(rvs[r], v_in_probs[r]);
        v_out_sampler.emplace_back(rvs[r], v_out_probs[r]);
    }

    for (size_t i = 0; i < rs.shape()[0]; ++i)
    {
        size_t r = rs[i];
        size_t s = ss[i];
        double p = probs[i];

        if (!is_directed::apply<Graph>::type::value && r == s)
            p /= 2;

        if (r >= v_out_sampler.size() || v_out_sampler[r].prob_sum() == 0 ||
            s >= v_in_sampler.size() || v_in_sampler[s].prob_sum() == 0)
            throw GraphException("Inconsistent SBM parameters: edge probabilities given for empty groups");

        std::poisson_distribution<> poi(p);
        size_t ers = poi(rng);

        for (size_t j = 0; j < ers; ++j)
        {
            size_t u = v_out_sampler[r].sample(rng);
            size_t v = v_in_sampler[s].sample(rng);
            add_edge(u, v, g);
        }
    }
}


} // graph_tool namespace

#endif // GRAPH_SBM_HH

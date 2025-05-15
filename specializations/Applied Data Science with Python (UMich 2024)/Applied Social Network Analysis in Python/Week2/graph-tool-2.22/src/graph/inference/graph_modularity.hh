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

#ifndef GRAPH_MODULARITY_HH
#define GRAPH_MODULARITY_HH

#include <tuple>
#include <iostream>
#include <fstream>
#include <iomanip>

#include "graph_tool.hh"
#include "hash_map_wrap.hh"

namespace graph_tool
{

using namespace std;
using namespace boost;

// get Newman's modularity of a given community partition
template <class Graph, class WeightMap, class CommunityMap>
double get_modularity(const Graph& g, WeightMap weights, CommunityMap b)
{
    size_t B = 0;
    for (auto v : vertices_range(g))
    {
        auto r = get(b, v);
        if (r < 0)
            throw ValueException("invalid community label: negative value!");
        B = std::max(size_t(r) + 1, B);
    }

    vector<double> er(B), err(B);
    double W = 0;

    for (auto e : edges_range(g))
    {
        size_t r = get(b, source(e, g));
        size_t s = get(b, target(e, g));

        auto w = get(weights, e);
        W += 2 * w;
        er[r] += w;
        er[s] += w;

        if (r == s)
            err[r] += 2 * w;
    }

    double Q = 0;
    for (size_t r = 0; r < B; ++r)
        Q += err[r] - (er[r] * er[r]) / W;
    Q /= W;
    return Q;
};

} // graph_tool namespace

#endif //GRAPH_MODULARITY_HH

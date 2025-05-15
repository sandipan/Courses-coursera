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

#ifndef GRAPH_BLOCKMODEL_LAYERS_UTIL_HH
#define GRAPH_BLOCKMODEL_LAYERS_UTIL_HH

#include "config.h"

#include <vector>

namespace graph_tool
{
using namespace boost;
using namespace std;


template <class State, class MEntries>
double virtual_move_covariate(size_t v, size_t r, size_t s, State& state,
                              MEntries& m_entries, bool reset)
{
    if (reset)
    {
        m_entries.clear();
        state.get_move_entries(v, r, s, m_entries);
    }

    auto& entries = m_entries.get_entries();
    auto& delta = m_entries.get_delta();

    double dS = 0;
    for (size_t i = 0; i < entries.size(); ++i)
    {
        auto& entry = entries[i];
        auto er = entry.first;
        auto es = entry.second;
        int d = get<0>(delta[i]);

        int ers = get_beprop(er, es, state._mrs, state._emat);
        assert(ers + d >= 0);
        dS -= -lgamma_fast(ers + 1);
        dS += -lgamma_fast(ers + d + 1);
    }
    return dS;
}

template <class Graph, class EMap>
double covariate_entropy(Graph& bg, EMap& mrs)
{
    double S = 0;
    for (auto e : edges_range(bg))
        S -= lgamma_fast(mrs[e] + 1);
    return S;
}

} // graph_tool namespace

#endif //GRAPH_BLOCKMODEL_LAYERS_UTIL_HH

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

#ifndef GRAPH_AUGMENT_HH
#define GRAPH_AUGMENT_HH

namespace graph_tool
{
using namespace std;
using namespace boost;

template <class Graph, class AugmentedMap, class CapacityMap,
          class ReversedMap,  class ResidualMap>
void augment_graph(Graph& g, AugmentedMap augmented, CapacityMap capacity,
                   ReversedMap rmap, ResidualMap res,
                   bool detect_reversed=false)
{
    vector<typename graph_traits<Graph>::edge_descriptor> e_list;
    for (auto e : edges_range(g))
        augmented[e] = false;
    for (auto e : edges_range(g))
    {
        if (!detect_reversed)
        {
            e_list.push_back(e);
        }
        else
        {
            for (auto ae : out_edges_range(target(e, g), g))
            {
                if (target(ae, g) == source(e, g) && augmented[e] == false)
                {
                    augmented[e] = augmented[ae] = 2;
                    rmap[e] = ae;
                    rmap[ae] = e;
                    break;
                }
            }
            if (augmented[e] == false)
                e_list.push_back(e);
        }
    }

    for (auto& e : e_list)
    {
        auto ae = add_edge(target(e, g), source(e, g), g).first;
        augmented[ae] = true;
        capacity[ae] = 0;
        rmap[e] = ae;
        rmap[ae] = e;
        res[ae] = 0;
    }
}

template <class Graph, class AugmentedMap>
void deaugment_graph(Graph& g, AugmentedMap augmented)
{
    vector<typename graph_traits<Graph>::edge_descriptor> e_list;
    for (auto v : vertices_range(g))
    {
        e_list.clear();
        for (auto e : out_edges_range(v, g))
        {
            if (augmented[e] == true)
                e_list.push_back(e);
        }

        for (auto& e : e_list)
            remove_edge(e, g);
    }
}


template <class Graph, class CapacityMap, class ResidualMap,
          class AugmentedMap>
void residual_graph(Graph& g, CapacityMap capacity, ResidualMap res,
                    AugmentedMap augmented)
{
    vector<typename graph_traits<Graph>::edge_descriptor> e_list;
    for (auto e : edges_range(g))
    {
        if (capacity[e] - res[e] > 0)
            e_list.push_back(e);
    }

    for (auto& e : e_list)
    {
        auto ne = add_edge(target(e, g), source(e, g), g);
        augmented[ne.first] = true;
    }
}

} // graph_tool namespace

#endif // GRAPH_AUGMENT_HH

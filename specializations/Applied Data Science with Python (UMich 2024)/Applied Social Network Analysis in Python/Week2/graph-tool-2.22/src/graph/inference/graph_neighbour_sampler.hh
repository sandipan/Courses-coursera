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

#ifndef GRAPH_NEIGHBOUR_SAMPLER_HH
#define GRAPH_NEIGHBOUR_SAMPLER_HH

#include "config.h"

#include "graph_tool.hh"

// Sample neighbours efficiently
// =============================

namespace graph_tool
{

template <class Graph, class Weighted, class Dynamic>
class NeighbourSampler
{
public:
    typedef typename boost::graph_traits<Graph>::vertex_descriptor vertex_t;

    template <class Eprop>
    NeighbourSampler(Graph& g, Eprop& eweight, bool self_loops=false)
        : _sampler(get(vertex_index_t(), g), num_vertices(g)),
          _sampler_pos(get(vertex_index_t(), g), num_vertices(g)),
          _eindex(get(edge_index_t(), g))
    {
        init(g, eweight, self_loops,
             typename boost::mpl::and_<Weighted,
                                       typename boost::mpl::not_<Dynamic>::type>::type());
    }

    template <class Eprop>
    void init(Graph& g, Eprop& eweight, bool self_loops, boost::mpl::false_)
    {
        for (auto e : edges_range(g))
        {
            auto u = source(e, g);
            auto v = target(e, g);

            if (!self_loops && u == v)
                continue;

            auto w = eweight[e];

            if (w == 0)
                continue;

            if (u == v)
            {
                insert(v, u, w, e);
            }
            else
            {
                insert(v, u, w, e);
                insert(u, v, w, e);
            }
        }
    }

    template <class Eprop>
    void init(Graph& g, Eprop& eweight, bool self_loops, boost::mpl::true_)
    {
        for (auto v : vertices_range(g))
        {
            std::vector<item_t> us;
            std::vector<double> probs;
            for (auto e : out_edges_range(v, g))
            {
                auto u = target(e, g);
                double w = eweight[e];
                if (w == 0)
                    continue;

                if (u == v)
                {
                    if (!self_loops)
                        continue;
                    if (!is_directed::apply<Graph>::type::value)
                        w /= 2;
                }
                us.emplace_back(u, 0);
                probs.push_back(w);
            }

            for (auto e : in_edges_range(v, g))
            {
                auto u = source(e, g);
                double w = eweight[e];
                if (w == 0 || u == v)
                    continue;
                us.emplace_back(u, 0);
                probs.push_back(w);
            }
            _sampler[v] = sampler_t(us, probs);
        }
    }

    template <class RNG>
    vertex_t sample(vertex_t v, RNG& rng)
    {
        auto& sampler = _sampler[v];
        auto& item = sample_item(sampler, rng);
        return item.first;
    }

    bool empty(vertex_t v)
    {
        return _sampler[v].empty();
    }

    template <class Edge>
    void remove(vertex_t v, vertex_t u, Edge&& e)
    {
        auto& sampler = _sampler[v];
        auto& sampler_pos = _sampler_pos[v];

        auto k = std::make_pair(u, _eindex[e]);
        remove_item(k, sampler, sampler_pos);
    }

    template <class Weight, class Edge>
    void insert(vertex_t v, vertex_t u, Weight w, Edge&& e)
    {
        auto& sampler = _sampler[v];
        auto& sampler_pos = _sampler_pos[v];
        auto k = std::make_pair(u, _eindex[e]);
        insert_item(k, w, sampler, sampler_pos);
    }

private:
    typedef std::pair<vertex_t, size_t> item_t;
    typedef gt_hash_map<item_t, size_t> pos_map_t;

    template <class RNG>
    const item_t& sample_item(std::vector<item_t>& sampler, RNG& rng)
    {
        return uniform_sample(sampler, rng);
    }

    template <class Sampler, class RNG>
    const item_t& sample_item(Sampler& sampler, RNG& rng)
    {
        return sampler.sample(rng);
    }

    void remove_item(item_t& u, std::vector<item_t>& sampler,
                     pos_map_t& sampler_pos)
    {
        auto& back = sampler.back();
        size_t pos = sampler_pos[u];
        sampler_pos[back] = pos;
        sampler[pos] = back;
        sampler.pop_back();
        sampler_pos.erase(u);
    }

    template <class Sampler>
    void remove_item(item_t& u, Sampler& sampler,
                     pos_map_t& sampler_pos)
    {
        size_t pos = sampler_pos[u];
        sampler.remove(pos);
        sampler_pos.erase(u);
    }


    template <class Weight>
    void insert_item(item_t& u, Weight, std::vector<item_t>& sampler,
                     pos_map_t& sampler_pos)
    {
        sampler_pos[u] = sampler.size();
        sampler.push_back(u);
    }

    template <class Weight>
    void insert_item(item_t& u, Weight w, DynamicSampler<item_t>& sampler,
                     pos_map_t& sampler_pos)
    {
        assert(sampler_pos.find(u) == sampler_pos.end());
        sampler_pos[u] = sampler.insert(u, w);
    }

    typedef typename std::conditional<Weighted::value,
                                      typename std::conditional<Dynamic::value,
                                                                DynamicSampler<item_t>,
                                                                Sampler<item_t,
                                                                        boost::mpl::false_>>::type,
                                      vector<item_t>>::type
        sampler_t;

    typedef typename vprop_map_t<sampler_t>::type vsampler_t;
    typename vsampler_t::unchecked_t _sampler;

    typedef typename vprop_map_t<pos_map_t>::type sampler_pos_t;
    typename sampler_pos_t::unchecked_t _sampler_pos;

    typename property_map<Graph, edge_index_t>::type _eindex;
};

}

#endif // GRAPH_NEIGHBOUR_SAMPLER_HH

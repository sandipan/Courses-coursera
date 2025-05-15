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

#include "graph.hh"
#include "graph_filtering.hh"
#include "graph_properties.hh"
#include "graph_util.hh"
#include "graph_selectors.hh"

#include "graph_motifs.hh"

#include "graph_python_interface.hh"
#include <boost/python.hpp>

using namespace graph_tool;

struct append_to_list
{
    template <class Graph>
    void operator()(Graph& g, std::vector<d_graph_t>& glist) const
    {
        glist.emplace_back();
        graph_copy(g, glist.back());
    }
};

struct retrieve_from_list
{
    template <class Graph>
    void operator()(Graph& g, std::vector<d_graph_t>& glist, bool& done) const
    {
        if (glist.empty())
        {
            done = true;
            return;
        }
        typename wrap_directed::apply<Graph,d_graph_t>::type
            uback(glist.back());
        graph_copy(uback, g);
        glist.pop_back();
    }
};

void get_motifs(GraphInterface& g, size_t k, boost::python::list subgraph_list,
                boost::python::list hist, boost::python::list pvmaps,
                bool collect_vmaps, boost::python::list p, bool comp_iso,
                bool fill_list, rng_t& rng)
{
    std::vector<d_graph_t> list;
    for (int i = 0; i <  boost::python::len(subgraph_list); ++i)
    {
        GraphInterface& sub =
            boost::python::extract<GraphInterface&>(subgraph_list[i]);
        run_action<>()(sub, std::bind(append_to_list(),
                                      std::placeholders::_1,
                                      std::ref(list)))();
    }

    std::vector<size_t> phist;
    std::vector<double> plist;
    double total = 1;
    for (int i = 0; i < boost::python::len(p); ++i)
    {
        plist.push_back(boost::python::extract<double>(p[i]));
        total *= plist[i];
    }

    boost::any sampler;
    if (total == 1.0)
        sampler = sample_all();
    else
        sampler = sample_some(plist, rng);

    typedef property_map_type
            ::apply<int32_t, GraphInterface::vertex_index_map_t>::type
            vmap_t;
    std::vector<std::vector<vmap_t> > vmaps;

    run_action<>()
        (g, std::bind(get_all_motifs(collect_vmaps, plist[0], comp_iso,
                                     fill_list, rng),
                      std::placeholders::_1, k, std::ref(list), std::ref(phist),
                      std::ref(vmaps), std::placeholders::_2),
         boost::mpl::vector<sample_all,sample_some>())(sampler);

    for (size_t i = 0; i < phist.size(); ++i)
        hist.append(phist[i]);

    for (size_t i = 0; i < vmaps.size(); ++i)
    {
        boost::python::list vlist;
        for (size_t j = 0; j < vmaps[i].size(); ++j)
            vlist.append(PythonPropertyMap<vmap_t>(vmaps[i][j]));
        pvmaps.append(vlist);
    }

    if (fill_list)
    {
        for (int i = 0; i < boost::python::len(subgraph_list); ++i)
            subgraph_list.pop();

        bool done = false;
        while (!done)
        {

            GraphInterface sub;
            sub.set_directed(g.get_directed());
            typedef graph_tool::detail::get_all_graph_views::apply
                <graph_tool::detail::filt_scalar_type,
                 boost::mpl::bool_<false>, boost::mpl::bool_<false>,
                 boost::mpl::bool_<false>, boost::mpl::bool_<true>,
                 boost::mpl::bool_<true> >::type gviews;
            run_action<gviews>()
                (sub, std::bind(retrieve_from_list(), std::placeholders::_1,
                                std::ref(list), std::ref(done)))();
            if (!done)
                subgraph_list.append(sub);
        }
        subgraph_list.reverse();
    }
}

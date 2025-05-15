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

#include "graph_python_interface.hh"
#include "graph.hh"
#include "graph_properties.hh"
#include "graph_filtering.hh"
#include "graph_selectors.hh"
#include "graph_util.hh"
#include "hash_map_wrap.hh"

#include <boost/mpl/for_each.hpp>

#include <boost/python/extract.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct do_perfect_ehash
{
    template <class Graph, class EdgePropertyMap, class HashProp>
    void operator()(Graph& g, EdgePropertyMap prop, HashProp hprop,
                    boost::any& adict) const
    {
        typedef typename property_traits<EdgePropertyMap>::value_type val_t;
        typedef typename property_traits<HashProp>::value_type hash_t;
        typedef unordered_map<val_t, hash_t> dict_t;

        if (adict.empty())
            adict = dict_t();

        dict_t& dict = any_cast<dict_t&>(adict);

        for (auto e : edges_range(g))
        {
            auto val = prop[e];
            auto iter = dict.find(val);
            hash_t h;
            if (iter == dict.end())
            {
                h = dict.size();
                dict[val] = h;
            }
            else
            {
                h = iter->second;
            }
            hprop[e] = h;
        }
    }
};

void perfect_ehash(GraphInterface& gi, boost::any prop, boost::any hprop,
                   boost::any& dict)
{
    run_action<graph_tool::detail::always_directed>()
        (gi, std::bind<void>(do_perfect_ehash(), std::placeholders::_1,
         std::placeholders::_2, std::placeholders::_3, std::ref(dict)),
         edge_properties(), writable_edge_scalar_properties())
        (prop, hprop);
}

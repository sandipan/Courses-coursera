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

#define BOOST_PYTHON_MAX_ARITY 40
#include <boost/python.hpp>

#include "graph_tool.hh"
#include "random.hh"

#include "graph_blockmodel_util.hh"
#include "graph_blockmodel.hh"
#include "graph_blockmodel_layers_util.hh"
#define BASE_STATE_params BLOCK_STATE_params
#include "graph_blockmodel_layers.hh"
#include "graph_state.hh"

using namespace boost;
using namespace graph_tool;

GEN_DISPATCH(block_state, BlockState, BLOCK_STATE_params)

template <class BaseState>
GEN_DISPATCH(layered_block_state, Layers<BaseState>::template LayeredBlockState,
             LAYERED_BLOCK_STATE_params)

python::object make_layered_block_state(boost::python::object oblock_state,
                                        boost::python::object olayered_state)
{
    python::object state;
    auto dispatch = [&](auto& block_state)
        {
            typedef typename std::remove_reference<decltype(block_state)>::type
            state_t;

            layered_block_state<state_t>::make_dispatch
                (olayered_state,
                 [&](auto& s)
                 {
                     state = python::object(s);
                 },
                 block_state);
        };
    block_state::dispatch(oblock_state, dispatch);
    return state;
}

template <class Type>
vector<Type> from_list(boost::python::object list)
{
    vector<Type> v;
    for (int i = 0; i < boost::python::len(list); ++i)
        v.push_back(boost::python::extract<Type>(list[i])());
    return v;
};

template <class Type>
vector<std::reference_wrapper<Type>> from_rlist(boost::python::object list)
{
    vector<std::reference_wrapper<Type>> v;
    for (int i = 0; i < boost::python::len(list); ++i)
        v.emplace_back(boost::python::extract<Type&>(list[i])());
    return v;
};

template <class Type>
vector<std::reference_wrapper<Type>> from_any_list(boost::python::object list)
{
    vector<std::reference_wrapper<Type>> v;
    for (int i = 0; i < boost::python::len(list); ++i)
        v.emplace_back(any_cast<Type&>(boost::python::extract<boost::any&>(list[i])()));
    return v;
};

void split_layers(GraphInterface& gi, boost::any& aec, boost::any& ab,
                  boost::any& arec, boost::any& adrec, boost::any& aeweight,
                  boost::any& avweight, boost::any& avc, boost::any& avmap,
                  boost::any& alweight, boost::python::object& ous,
                  boost::python::object& oub, boost::python::object& ourec,
                  boost::python::object& oudrec,
                  boost::python::object& oueweight,
                  boost::python::object& ouvweight, vbmap_t& block_map,
                  boost::python::object& obrmap, boost::python::object& ouvmap)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    typedef vprop_map_t<vector<int32_t>>::type vvmap_t;
    typedef eprop_map_t<int32_t>::type emap_t;
    typedef eprop_map_t<std::vector<double>>::type remap_t;

    emap_t& ec = any_cast<emap_t&>(aec);
    vmap_t& b = any_cast<vmap_t&>(ab);
    remap_t& rec = any_cast<remap_t&>(arec);
    remap_t& drec = any_cast<remap_t&>(adrec);
    vmap_t& vweight = any_cast<vmap_t&>(avweight);
    emap_t& eweight = any_cast<emap_t&>(aeweight);
    vvmap_t& vc = any_cast<vvmap_t&>(avc);
    vvmap_t& vmap = any_cast<vvmap_t&>(avmap);
    vvmap_t& lweight = any_cast<vvmap_t&>(alweight);

    auto us = from_rlist<GraphInterface>(ous);
    auto ub = from_any_list<vmap_t>(oub);
    auto urec = from_any_list<remap_t>(ourec);
    auto udrec = from_any_list<remap_t>(oudrec);
    auto uvweight = from_any_list<vmap_t>(ouvweight);
    auto ueweight = from_any_list<emap_t>(oueweight);

    auto block_rmap = from_any_list<vmap_t>(obrmap);
    auto uvmap = from_any_list<vmap_t>(ouvmap);

    run_action<>()(gi,
                   [&](auto& g)
                   {
                       std::vector<gt_hash_map<size_t, size_t>>
                           vhmap(num_vertices(g));

                       typename vprop_map_t<gt_hash_map<size_t, size_t>>::type
                           lw(get(vertex_index, g));
                       for (auto v : vertices_range(g))
                       {
                           for (size_t i = 0; i < lweight[v].size(); i += 2)
                           {
                               auto l = lweight[v][i];
                               auto w = lweight[v][i + 1];
                               lw[v][l] = w;
                           }
                       }

                       auto get_v = [&] (size_t v, size_t l) -> size_t
                           {
                               auto iter = vhmap[v].find(l);
                               if (iter == vhmap[v].end())
                               {
                                   size_t u = add_vertex(us[l].get().get_graph());
                                   vhmap[v][l] = u;
                                   size_t pos = lower_bound(vc[v].begin(), vc[v].end(), l) - vc[v].begin();
                                   vc[v].insert(vc[v].begin() + pos, l);
                                   vmap[v].insert(vmap[v].begin() + pos, u);
                                   uvmap[l].get()[u] = v;
                                   if (lw[v].empty())
                                       uvweight[l].get()[u] = vweight[v];
                                   else
                                       uvweight[l].get()[u] = lw[v][l];
                                   size_t r =  b[v];
                                   size_t u_r;

                                   if (block_map.size() <= l)
                                       block_map.resize(l + 1);

                                   auto& bmap = block_map[l];
                                   auto riter = bmap.find(r);
                                   if (riter == bmap.end())
                                   {
                                       u_r = bmap.size();
                                       bmap[r] = u_r;
                                       block_rmap[l].get()[u_r] = r;
                                   }
                                   else
                                   {
                                       u_r = riter->second;
                                   }
                                   ub[l].get()[u] = u_r;
                                   return u;
                               }
                               else
                               {
                                   return iter->second;
                               }
                           };

                       for (auto e : edges_range(g))
                       {
                           auto s = source(e, g);
                           auto t = target(e, g);
                           size_t l = ec[e];

                           auto u_s = get_v(s, l);
                           auto u_t = get_v(t, l);
                           auto ne = add_edge(u_s, u_t, us[l].get().get_graph()).first;
                           ueweight[l].get()[ne] = eweight[e];
                           urec[l].get()[ne] = rec[e];
                           udrec[l].get()[ne] = drec[e];
                       }
                   })();
}


void get_lweights(GraphInterface& gi, boost::any& avc, boost::any& avmap,
                  boost::any& alweight, boost::python::object& ouvweight)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    typedef vprop_map_t<vector<int32_t>>::type vvmap_t;

    vvmap_t& vc = any_cast<vvmap_t&>(avc);
    vvmap_t& vmap = any_cast<vvmap_t&>(avmap);
    vvmap_t& lweight = any_cast<vvmap_t&>(alweight);

    auto uvweight = from_any_list<vmap_t>(ouvweight);

    run_action<>()(gi, [&](auto& g)
                   {
                       for (auto v : vertices_range(g))
                       {
                           for (size_t i = 0; i < vc[v].size(); ++i)
                           {
                               auto l = vc[v][i];
                               auto u = vmap[v][i];
                               auto w = uvweight[l].get()[u];
                               lweight[v].push_back(l);
                               lweight[v].push_back(w);
                           }
                       }
                   })();
}

void get_blweights(GraphInterface& gi, boost::any& ab, boost::any& avc,
                   boost::any& avmap, boost::any& alweight,
                   boost::python::object& ouvweight)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    typedef vprop_map_t<vector<int32_t>>::type vvmap_t;

    vmap_t& b = any_cast<vmap_t&>(ab);
    vvmap_t& vc = any_cast<vvmap_t&>(avc);
    vvmap_t& vmap = any_cast<vvmap_t&>(avmap);
    vvmap_t& lweight = any_cast<vvmap_t&>(alweight);

    auto uvweight = from_any_list<vmap_t>(ouvweight);

    run_action<>()(gi, [&](auto& g)
                   {
                       gt_hash_map<size_t, gt_hash_map<size_t, size_t>> blw;
                       for (auto v : vertices_range(g))
                       {
                           auto r = b[v];
                           for (size_t i = 0; i < vc[v].size(); ++i)
                           {
                               auto l = vc[v][i];
                               auto u = vmap[v][i];
                               auto w = uvweight[l].get()[u];
                               blw[r][l] += w;
                           }
                       }
                       for (auto& rlw : blw)
                       {
                           auto r = rlw.first;
                           for (auto& lw : rlw.second)
                           {
                               auto l = lw.first;
                               auto w = lw.second;
                               lweight[r].push_back(l);
                               lweight[r].push_back(w);
                           }
                       }
                   })();
}


bool bmap_has(const vbmap_t& bmap, size_t c, size_t r)
{
    if (c > bmap.size())
        throw GraphException("invalid covariate value:" + lexical_cast<string>(c));
    auto iter = bmap[c].find(r);
    if (iter == bmap[c].end())
        return false;
    return true;
}

size_t bmap_get(const vbmap_t& bmap, size_t c, size_t r)
{
    if (c > bmap.size())
        throw GraphException("invalid covariate value:" + lexical_cast<string>(c));
    auto iter = bmap[c].find(r);
    if (iter == bmap[c].end())
        throw GraphException("no mapping for block " + lexical_cast<string>(r)
                             + " in layer " + lexical_cast<string>(c));
    return iter->second;
}

void bmap_set(vbmap_t& bmap, size_t c, size_t r, size_t r_u)
{
    if (c > bmap.size())
        throw GraphException("invalid covariate value:" + lexical_cast<string>(c));
    bmap[c][r] = r_u;
}

void bmap_del_c(vbmap_t& bmap, size_t c)
{
    if (c > bmap.size())
        throw GraphException("invalid covariate value:" + lexical_cast<string>(c));
    bmap.erase(bmap.begin() + c);
}

vbmap_t bmap_copy(const vbmap_t& bmap)
{
    return bmap;
}

size_t bmap_size(const vbmap_t& bmap)
{
    return bmap.size();
}

typedef gt_hash_map<std::tuple<int, int>,
                    gt_hash_map<std::tuple<size_t, size_t>, size_t>>
    ldegs_map_t;

ldegs_map_t get_layered_block_degs(GraphInterface& gi, boost::any aeweight,
                                   boost::any avweight, boost::any aec,
                                   boost::any ab)
{
    ldegs_map_t degs;
    vmap_t b = boost::any_cast<vmap_t>(ab);
    emap_t eweight = boost::any_cast<emap_t>(aeweight);
    vmap_t vweight = boost::any_cast<vmap_t>(avweight);
    emap_t ec = boost::any_cast<emap_t>(aec);
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       for (auto v : vertices_range(g))
                       {
                           gt_hash_map<size_t, size_t> kin, kout;
                           gt_hash_set<size_t> ls;

                           for (auto e : out_edges_range(v, g))
                           {
                               auto w = eweight[e];
                               auto l = ec[e];
                               kout[l] += w;
                               ls.insert(l);
                           }

                           for (auto e : in_edges_range(v, g))
                           {
                               auto w = eweight[e];
                               auto l = ec[e];
                               kin[l] += w;
                               ls.insert(l);
                           }

                           for (auto l : ls)
                           {
                               size_t skin = 0, skout = 0;
                               auto iter = kin.find(l);
                               if (iter != kin.end())
                                   skin = iter->second;
                               iter = kout.find(l);
                               if (iter != kout.end())
                                   skout = iter->second;
                               auto& h = degs[std::make_tuple(l + 1, b[v])];
                               h[std::make_tuple(skin, skout)] += vweight[v];
                           }

                           size_t skin = in_degreeS()(v, g, eweight);
                           size_t skout = out_degreeS()(v, g, eweight);
                           auto& h = degs[std::make_tuple(0, b[v])];
                           h[std::make_tuple(skin, skout)] += vweight[v];
                       }
                   })();
    return degs;
}

degs_map_t get_mapped_block_degs(GraphInterface& gi, ldegs_map_t& ldegs,
                                 int l, boost::any avmap)
{
    degs_map_t ndegs;
    vmap_t vmap = boost::any_cast<vmap_t>(avmap);
    run_action<>()(gi,
                   [&](auto& g)
                   {
                       for (auto u : vertices_range(g))
                       {
                           int v = vmap[u];
                           auto& d = ndegs[u];
                           for (auto& ks : ldegs[std::make_tuple(l, v)])
                               d.emplace_back(get<0>(ks.first), get<1>(ks.first),
                                              ks.second);
                       }
                   })();
    return ndegs;
}

ldegs_map_t get_ldegs(GraphInterface& gi, boost::any& avc, boost::any& avmap,
                      boost::python::object& oudegs)
{
    typedef vprop_map_t<vector<int32_t>>::type vvmap_t;

    vvmap_t& vc = any_cast<vvmap_t&>(avc);
    vvmap_t& vmap = any_cast<vvmap_t&>(avmap);

    auto udegs = from_rlist<degs_map_t>(oudegs);

    ldegs_map_t ndegs;
    run_action<>()(gi, [&](auto& g)
                   {
                       gt_hash_map<size_t, gt_hash_map<size_t, size_t>> blw;
                       for (int v : vertices_range(g))
                       {
                           auto& d = udegs[0].get()[v];
                           auto& h = ndegs[std::make_tuple(0, v)];
                           for (auto& kn : d)
                               h[std::make_tuple(get<0>(kn), get<1>(kn))] =
                                   get<2>(kn);

                           for (size_t i = 0; i < vc[v].size(); ++i)
                           {
                               int l = vc[v][i];
                               auto u = vmap[v][i];
                               auto& d = udegs[l + 1].get()[u];
                               auto& h = ndegs[std::make_tuple(l + 1, v)];
                               for (auto& kn : d)
                                   h[std::make_tuple(get<0>(kn), get<1>(kn))] =
                                       get<2>(kn);
                           }
                       }
                   })();
    return ndegs;
}


ldegs_map_t ldegs_map_copy(ldegs_map_t& ldegs)
{
    return ldegs;
}

void export_lsbm();

void export_layered_blockmodel_state()
{
    using namespace boost::python;

    export_lsbm();

    def("make_layered_block_state", &make_layered_block_state);
    def("split_layers", &split_layers);
    def("get_layered_block_degs", &get_layered_block_degs);
    def("get_mapped_block_degs", &get_mapped_block_degs);
    def("get_ldegs", &get_ldegs);
    def("get_lweights", &get_lweights);
    def("get_blweights", &get_blweights);

    class_<ldegs_map_t>("ldegs_map_t")
        .def("copy", &ldegs_map_copy);

    class_<vbmap_t>("bmap_t")
        .def("has", bmap_has)
        .def("get", bmap_get)
        .def("set", bmap_set)
        .def("del_c", bmap_del_c)
        .def("copy", bmap_copy)
        .def("size", bmap_size);
}

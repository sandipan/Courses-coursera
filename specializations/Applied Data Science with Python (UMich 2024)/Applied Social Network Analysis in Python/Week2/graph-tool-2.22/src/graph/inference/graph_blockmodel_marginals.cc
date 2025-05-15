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

#include <boost/math/special_functions/gamma.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

void collect_vertex_marginals(GraphInterface& gi, boost::any ob,
                              boost::any op, size_t update)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    auto b = any_cast<vmap_t>(ob).get_unchecked();

    run_action<>()
        (gi, [&](auto& g, auto p)
         {
             typename property_traits<decltype(p)>::value_type::value_type
                 up = update;
             parallel_vertex_loop
                 (g,
                  [&](auto v)
                  {
                      auto r = b[v];
                      auto& pv = p[v];
                      if (pv.size() <= size_t(r))
                          pv.resize(r + 1);
                      pv[r] += up;
                  });
         },
         vertex_scalar_vector_properties())(op);
}

class BlockPairHist
    : public gt_hash_map<std::pair<int32_t,int32_t>,size_t>
{
public:

    boost::python::dict get_state()
    {
        boost::python::dict state;
        for (auto& kv : *this)
        {
            auto k = python::make_tuple(kv.first.first,
                                        kv.first.second);
            state[k] = kv.second;
        }
        return state;
    }

    void set_state(boost::python::dict state)
    {
        auto keys = state.keys();
        for (int i = 0; i < python::len(keys); ++i)
        {
            auto k = keys[i];
            int32_t r = python::extract<int32_t>(k[0]);
            int32_t s = python::extract<int32_t>(k[1]);
            size_t v = python::extract<size_t>(state[k]);
            (*this)[make_pair(r, s)] = v;
        }
    }

    size_t get_item(boost::python::object k)
    {
        int32_t r = python::extract<int32_t>(k[0]);
        int32_t s = python::extract<int32_t>(k[1]);
        auto iter = this->find(make_pair(r, s));
        if (iter == this->end())
            return 0;
        return iter->second;
    }

    void set_item(boost::python::object k, double v)
    {
        int32_t r = python::extract<int32_t>(k[0]);
        int32_t s = python::extract<int32_t>(k[1]);
        (*this)[make_pair(r, s)] = v;
    }

};

void collect_edge_marginals(GraphInterface& gi, boost::any ob,
                            boost::any op, size_t update)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    auto b = any_cast<vmap_t>(ob).get_unchecked();

    typedef eprop_map_t<python::object>::type
        emap_t;
    auto pe = any_cast<emap_t>(op).get_unchecked(gi.get_edge_index_range());

    run_action<>()
        (gi,
         [&](auto& g)
         {
            parallel_edge_loop
                 (g,
                  [&](const auto& e)
                  {
                      auto u = min(source(e, g), target(e, g));
                      auto v = max(source(e, g), target(e, g));

                      auto r = b[u];
                      auto s = b[v];

                      BlockPairHist& h =
                          boost::python::extract<BlockPairHist&>(pe[e]);

                      h[make_pair(r, s)] += update;
                  });
         })();
}

double mf_entropy(GraphInterface& gi, boost::any opv)
{
    double H=0;
    run_action<>()
        (gi,
         [&](auto& g, auto pv)
         {
             for (auto v : vertices_range(g))
             {
                 double sum = 0;
                 for (auto p : pv[v])
                     sum += p;
                 for (double p : pv[v])
                 {
                     if (p == 0)
                         continue;
                     p /= sum;
                     H -= p * log(p);
                 }
             }
         },
         vertex_scalar_vector_properties())(opv);

    return H;
}

boost::python::tuple bethe_entropy(GraphInterface& gi, boost::any op,
                                   boost::any opv)
{
    typedef vprop_map_t<vector<double>>::type vmap_t;
    vmap_t pv = any_cast<vmap_t>(opv);

    typedef eprop_map_t<boost::python::object>::type emap_t;
    auto pe = any_cast<emap_t>(op).get_unchecked();

    double H=0, Hmf=0;
    run_action<>()
        (gi,
         [&](auto& g)
         {
             for (auto e : edges_range(g))
             {
                 auto u = min(source(e, g), target(e, g));
                 auto v = max(source(e, g), target(e, g));

                 double sum = 0;

                 BlockPairHist& h =
                     boost::python::extract<BlockPairHist&>(pe[e]);

                 for (auto& prs : h)
                 {
                     sum += prs.second;
                     size_t r = prs.first.first;
                     size_t s = prs.first.second;
                     if (r >= pv[u].size())
                         pv[u].resize(r + 1);
                     pv[u][r] += prs.second;
                     if (s >= pv[v].size())
                         pv[v].resize(s + 1);
                     pv[v][s] += prs.second;
                 }

                 for (auto& prs : h)
                 {
                     if (prs.second == 0)
                         continue;
                     double pi = prs.second / sum;
                     H -= pi * log(pi);
                 }
             }

             for (auto v : vertices_range(g))
             {
                 double sum = std::accumulate(pv[v].begin(), pv[v].end(), 0.);
                 for (double pi : pv[v])
                 {
                     if (pi == 0)
                         continue;
                     pi /= sum;
                     int kt = 1 - total_degreeS()(v, g);
                     if (kt != 0)
                         H -= kt * (pi * log(pi));
                     Hmf -= pi * log(pi);
                 }
             }
         })();

    return boost::python::make_tuple(H, Hmf);
}

class PartitionHist
    : public gt_hash_map<std::vector<int32_t>, double>
{
public:

    boost::python::dict get_state()
    {
        boost::python::dict state;
        for (auto& kv : *this)
            state[kv.first] = kv.second;
        return state;
    }

    void set_state(boost::python::dict state)
    {
        auto keys = state.keys();
        for (int i = 0; i < python::len(keys); ++i)
        {
            auto& k = python::extract<std::vector<int32_t>&>(keys[i])();
            double v = python::extract<double>(state[k]);
            (*this)[k] = v;
        }
    }

    size_t get_item(std::vector<int32_t>& k)
    {
        auto iter = this->find(k);
        if (iter == this->end())
            return 0;
        return iter->second;
    }

    void set_item(std::vector<int32_t>& k, double v)
    {
        (*this)[k] = v;
    }

};

double log_n_permutations(const vector<int32_t>& b)
{
    std::vector<int32_t> count(b.size());
    for (auto bi : b)
        count[bi]++;
    double n = boost::math::lgamma(b.size() + 1);
    for (auto nr : count)
        n -= boost::math::lgamma(nr + 1);
    return n;
}

vector<int32_t> unlabel_partition(vector<int32_t> b)
{
    std::vector<int32_t> map(b.size(), -1);
    size_t pos = 0;
    for (auto& bi : b)
    {
        auto& x = map[bi];
        if (x == -1)
        {
            x = pos;
            ++pos;
        }
        bi = x;
    }
    return b;
}

void collect_partitions(boost::any& ob, PartitionHist& h, double update,
                        bool unlabel)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    auto& b = any_cast<vmap_t&>(ob);
    auto& v = b.get_storage();
    if (unlabel)
    {
        auto vc = unlabel_partition(v);
        h[vc] += update;
    }
    else
    {
        h[v] += update;
    }
}

void collect_hierarchical_partitions(python::object ovb, PartitionHist& h,
                                     size_t update, bool unlabel)
{
    typedef vprop_map_t<int32_t>::type vmap_t;
    vector<int32_t> v;
    for (int i = 0; i < len(ovb); ++i)
    {
        boost::any& ob = python::extract<boost::any&>(ovb[i])();
        auto& b = any_cast<vmap_t&>(ob);
        auto& vi = b.get_storage();
        v.reserve(v.size() + vi.size());
        if (unlabel)
        {
            auto vc = unlabel_partition(v);
            v.insert(v.end(), vc.begin(), vc.end());
        }
        else
        {
            v.insert(v.end(), vi.begin(), vi.end());
        }
        v.push_back(-1);
    }
    h[v] += update;
}

double partitions_entropy(PartitionHist& h, bool unlabeled)
{
    double S = 0;
    size_t N = 0;
    for (auto kv : h)
    {
        if (kv.second == 0)
            continue;
        N += kv.second;
        S -= kv.second * log(kv.second);
        if (unlabeled)
            S += kv.second * log_n_permutations(kv.first);
    }
    if (N > 0)
    {
        S /= N;
        S += log(N);
    }
    return S;
}

void export_marginals()
{
    using namespace boost::python;

    class_<BlockPairHist>("BlockPairHist",
                          "Histogram of block pairs, implemented in C++.\n"
                          "Interface supports querying and setting using pairs "
                          "of ints as keys, and ints as values.")
        .def("__setitem__", &BlockPairHist::set_item)
        .def("__getitem__", &BlockPairHist::get_item)
        .def("__setstate__", &BlockPairHist::set_state)
        .def("__getstate__", &BlockPairHist::get_state)
        .def("asdict", &BlockPairHist::get_state,
             "Return the histogram's contents as a dict.").enable_pickling();

    class_<PartitionHist>("PartitionHist",
                          "Histogram of partitions, implemented in C++.\n"
                          "Interface supports querying and setting using Vector_int32_t "
                          "as keys, and ints as values.")
        .def("__setitem__", &PartitionHist::set_item)
        .def("__getitem__", &PartitionHist::get_item)
        .def("__setstate__", &PartitionHist::set_state)
        .def("__getstate__", &PartitionHist::get_state)
        .def("asdict", &PartitionHist::get_state,
             "Return the histogram's contents as a dict.").enable_pickling();

    def("vertex_marginals", &collect_vertex_marginals);
    def("edge_marginals", &collect_edge_marginals);
    def("mf_entropy", &mf_entropy);
    def("bethe_entropy", &bethe_entropy);
    def("collect_partitions", &collect_partitions);
    def("collect_hierarchical_partitions", &collect_hierarchical_partitions);
    def("partitions_entropy", &partitions_entropy);
}

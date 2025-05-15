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

#ifndef GRAPH_MOTIFS_HH
#define GRAPH_MOTIFS_HH

#include <boost/graph/isomorphism.hpp>
#include <boost/functional/hash.hpp>
#include <algorithm>
#include <vector>

#include "random.hh"
#include "hash_map_wrap.hh"

namespace graph_tool
{
namespace mpl = boost::mpl;

template <class Value>
void insert_sorted(std::vector<Value>& v, const Value& val)
{
    auto iter = lower_bound(v.begin(), v.end(), val);
    if (iter != v.end() && *iter == val)
        return; // no repetitions
    v.insert(iter, val);
}

template <class Value>
bool has_val(std::vector<Value>& v, const Value& val)
{
    auto iter = lower_bound(v.begin(), v.end(), val);
    if (iter == v.end())
        return false;
    return *iter == val;
}

// gets all the subgraphs starting from vertex v and store it in subgraphs.
template <class Graph, class Sampler>
void get_subgraphs(Graph& g, typename boost::graph_traits<Graph>::vertex_descriptor v,
                   size_t n,
                   std::vector<std::vector<typename boost::graph_traits<Graph>::vertex_descriptor> >& subgraphs,
                   Sampler sampler)
{
    typedef typename boost::graph_traits<Graph>::vertex_descriptor vertex_t;

    // extension and subgraph stack
    std::vector<std::vector<vertex_t>> ext_stack(1);
    std::vector<std::vector<vertex_t>> sub_stack(1);
    std::vector<std::vector<vertex_t>> sub_neighbours_stack(1);

    sub_stack[0].push_back(v);
    for (auto e : out_edges_range(v, g))
    {
        typename boost::graph_traits<Graph>::vertex_descriptor u = target(e, g);
        if (u > v && !has_val(ext_stack[0], u))
        {
            insert_sorted(ext_stack[0], u);
            insert_sorted(sub_neighbours_stack[0],u);
        }
    }

    while (!sub_stack.empty())
    {
        std::vector<vertex_t>& ext = ext_stack.back();
        std::vector<vertex_t>& sub = sub_stack.back();
        std::vector<vertex_t>& sub_neighbours = sub_neighbours_stack.back();

        if (sub.size() == n)
        {
            // found a subgraph of the desired size; put it in the list and go
            // back a level
            subgraphs.push_back(sub);
            sub_stack.pop_back();
            ext_stack.pop_back();
            sub_neighbours_stack.pop_back();
            continue;
        }

        if (ext.empty())
        {
            // no where else to go
            ext_stack.pop_back();
            sub_stack.pop_back();
            sub_neighbours_stack.pop_back();
            continue;
        }
        else
        {
            // extend subgraph
            std::vector<vertex_t> new_ext, new_sub = sub,
                new_sub_neighbours = sub_neighbours;

            // remove w from ext
            vertex_t w = ext.back();
            ext.pop_back();

            // insert w in subgraph
            insert_sorted(new_sub, w);

            // update new_ext
            new_ext = ext;
            for (auto e : out_edges_range(w, g))
            {
                vertex_t u = target(e, g);
                if (u > v)
                {
                    if (!has_val(sub_neighbours, u))
                        insert_sorted(new_ext, u);
                    insert_sorted(new_sub_neighbours, u);
                }
            }

            sampler(new_ext, ext_stack.size());

            ext_stack.push_back(new_ext);
            sub_stack.push_back(new_sub);
            sub_neighbours_stack.push_back(new_sub_neighbours);
        }
    }
}

// sampling selectors

struct sample_all
{
    template <class val_type>
    void operator()(std::vector<val_type>&, size_t) {}
};

struct sample_some
{
    sample_some(std::vector<double>& p, rng_t& rng): _p(&p), _rng(&rng) {}
    sample_some() {}

    template <class val_type>
    void operator()(std::vector<val_type>& extend, size_t d)
    {
        typedef std::uniform_real_distribution<double> rdist_t;
        auto random = std::bind(rdist_t(), std::ref(*_rng));

        double pd = (*_p)[d+1];
        size_t nc = extend.size();
        double u = nc*pd - floor(nc*pd);
        size_t n;
        double r;
        #pragma omp critical (random)
        {
            r = random();
        }
        if (r < u)
            n = size_t(ceil(nc*pd));
        else
            n = size_t(floor(nc*pd));

        if (n == extend.size())
            return;
        if (n == 0)
        {
            extend.clear();
            return;
        }

        typedef std::uniform_int_distribution<size_t> idist_t;
        for (size_t i = 0; i < n; ++i)
        {
            auto random_v = std::bind(idist_t(0, extend.size()-i-1),
                                      std::ref(*_rng));
            size_t j;
            #pragma omp critical (random)
            {
                j = i + random_v();
            }
            std::swap(extend[i], extend[j]);
        }
        extend.resize(n);
    }

    std::vector<double>* _p;
    rng_t* _rng;
};


// build the actual induced subgraph from the vertex list
template <class Graph, class GraphSG>
void make_subgraph
    (std::vector<typename boost::graph_traits<Graph>::vertex_descriptor>& vlist,
     Graph& g, GraphSG& sub)
{
    for (size_t i = 0; i < vlist.size(); ++i)
        add_vertex(sub);
    for (size_t i = 0; i < vlist.size(); ++i)
    {
        typename boost::graph_traits<Graph>::vertex_descriptor ov = vlist[i], ot;
        typename boost::graph_traits<GraphSG>::vertex_descriptor nv = vertex(i,sub);
        for (auto e : out_edges_range(ov, g))
        {
            ot = target(e, g);
            auto viter = lower_bound(vlist.begin(), vlist.end(), ot);
            size_t ot_index = viter - vlist.begin();
            if (viter != vlist.end() && vlist[ot_index] == ot &&
                (is_directed::apply<Graph>::type::value || ot < ov))
                add_edge(nv, vertex(ot_index, sub), sub);
        }
    }
}

// compare two graphs for labeled exactness (not isomorphism)
template <class Graph>
bool graph_cmp(Graph& g1, Graph& g2)
{
    if (num_vertices(g1) != num_vertices(g2) || num_edges(g1) != num_edges(g2))
        return false;

    typename boost::graph_traits<Graph>::vertex_iterator v1, v1_end;
    typename boost::graph_traits<Graph>::vertex_iterator v2, v2_end;
    std::tie(v2, v2_end) = vertices(g2);
    for (std::tie(v1, v1_end) = vertices(g1); v1 != v1_end; ++v1)
    {
        if (out_degree(*v1, g1) != out_degree(*v2, g2))
            return false;
        if (in_degreeS()(*v1, g1) != in_degreeS()(*v2, g2))
            return false;

        std::vector<typename boost::graph_traits<Graph>::vertex_descriptor> out1, out2;
        typename boost::graph_traits<Graph>::out_edge_iterator e, e_end;
        for (std::tie(e, e_end) = out_edges(*v1, g1); e != e_end; ++e)
            out1.push_back(target(*e, g1));
        for (std::tie(e, e_end) = out_edges(*v2, g2); e != e_end; ++e)
            out2.push_back(target(*e, g2));
        std::sort(out1.begin(), out1.end());
        std::sort(out2.begin(), out2.end());
        if (out1 != out2)
            return false;
    }
    return true;
}

// short hand for subgraph types
typedef boost::adj_list<size_t> d_graph_t;

// we need this wrap to use the undirected_adaptor only on directed graphs
struct wrap_undirected
{
    template <class Graph>
    struct apply
    {
        typedef typename mpl::if_<typename is_directed::apply<Graph>::type,
                                  boost::undirected_adaptor<Graph>,
                                  Graph&>::type type;
    };
};

struct wrap_directed
{
    template <class Graph, class Sub>
    struct apply
    {
        typedef typename mpl::if_<typename is_directed::apply<Graph>::type,
                                  Sub&,
                                  boost::undirected_adaptor<Sub>>::type type;
    };
};


// get the signature of the graph: sorted degree sequence
template <class Graph>
void get_sig(Graph& g, std::vector<size_t>& sig)
{
    sig.clear();
    size_t N = num_vertices(g);
    if (N > 0)
        sig.resize(is_directed::apply<Graph>::type::value ? 2 * N : N);
    for (size_t i = 0; i < N; ++i)
    {
        auto v = vertex(i, g);
        sig[i] = out_degree(v, g);
        if(is_directed::apply<Graph>::type::value)
            sig[i + N] = in_degreeS()(v, g);
    }
    sort(sig.begin(), sig.end());
}

// gets (or samples) all the subgraphs in graph g
struct get_all_motifs
{
    get_all_motifs(bool collect_vmaps, double p, bool comp_iso, bool fill_list,
                   rng_t& rng)
        : collect_vmaps(collect_vmaps), p(p),
          comp_iso(comp_iso), fill_list(fill_list), rng(rng) {}
    bool collect_vmaps;
    double p;
    bool comp_iso;
    bool fill_list;
    rng_t& rng;

    template <class Graph, class Sampler, class VMap>
    void operator()(Graph& g, size_t k, std::vector<d_graph_t>& subgraph_list,
                    std::vector<size_t>& hist, std::vector<std::vector<VMap> >& vmaps,
                    Sampler sampler) const
    {
        // this hashes subgraphs according to their signature
        gt_hash_map<std::vector<size_t>,
                    std::vector<std::pair<size_t, d_graph_t> >,
                    std::hash<std::vector<size_t>>> sub_list;
        std::vector<size_t> sig; // current signature

        for (size_t i = 0; i < subgraph_list.size(); ++i)
        {
            auto& sub = subgraph_list[i];
            typename wrap_directed::apply<Graph,d_graph_t>::type
                usub(sub);
            get_sig(usub, sig);
            sub_list[sig].emplace_back(i, sub);
        }

        // the subgraph count
        hist.resize(subgraph_list.size());

        typedef std::uniform_real_distribution<double> rdist_t;
        auto random = std::bind(rdist_t(), std::ref(rng));

        // the set of vertices V to be sampled (filled only if p < 1)
        std::vector<size_t> V;
        if (p < 1)
        {
            for (auto v : vertices_range(g))
                V.push_back(v);

            size_t n;
            if (random() < p)
                n = size_t(ceil(V.size()*p));
            else
                n = size_t(floor(V.size()*p));

            typedef std::uniform_int_distribution<size_t> idist_t;
            for (size_t i = 0; i < n; ++i)
            {
                auto random_v = std::bind(idist_t(0, V.size()-i-1),
                                          std::ref(rng));
                size_t j = i + random_v();
                std::swap(V[i], V[j]);
            }
            V.resize(n);
        }

        size_t N = (p < 1) ? V.size() : num_vertices(g);
        #pragma omp parallel for if (num_vertices(g) > OPENMP_MIN_THRESH) \
            private(sig)
        for (size_t i = 0; i < N; ++i)
        {
            std::vector<std::vector<typename boost::graph_traits<Graph>::vertex_descriptor> >
                subgraphs;
            typename boost::graph_traits<Graph>::vertex_descriptor v =
                (p < 1) ? V[i] : vertex(i, g);
            if (!is_valid_vertex(v, g))
                continue;

            typename wrap_undirected::apply<Graph>::type ug(g);
            get_subgraphs(ug, v, k, subgraphs, sampler);

            for (size_t j = 0; j < subgraphs.size(); ++j)
            {
                d_graph_t sub;
                typename wrap_directed::apply<Graph,d_graph_t>::type
                    usub(sub);
                make_subgraph(subgraphs[j], g, usub);
                get_sig(usub, sig);

                #pragma omp critical (gather)
                {
                    bool skip = false;
                    auto iter = sub_list.find(sig);
                    if(iter == sub_list.end())
                    {
                        if (!fill_list)
                            skip = true; // avoid inserting an element in sub_list
                        sub_list[sig].clear();
                    }

                    if (!skip)
                    {
                        bool found = false;
                        size_t pos;
                        auto sl = sub_list.find(sig);
                        if (sl != sub_list.end())
                        {
                            for (auto& mpos : sl->second)
                            {
                                d_graph_t& motif = mpos.second;
                                typename wrap_directed::apply<Graph,d_graph_t>::type
                                    umotif(motif);
                                if (comp_iso)
                                {
                                    if (isomorphism(umotif, usub,
                                                    vertex_index1_map(get(boost::vertex_index, umotif)).
                                                    vertex_index2_map(get(boost::vertex_index, usub))))
                                        found = true;
                                }
                                else
                                {
                                    if (graph_cmp(umotif, usub))
                                        found = true;
                                }
                                if (found)
                                {
                                    pos = mpos.first;
                                    hist[pos]++;
                                    break;
                                }
                            }
                        }

                        if (found == false && fill_list)
                        {
                            subgraph_list.push_back(sub);
                            sub_list[sig].emplace_back(subgraph_list.size() - 1,
                                                       sub);
                            hist.push_back(1);
                            pos = hist.size() - 1;
                            found = true;
                        }

                        if (found && collect_vmaps)
                        {
                            if (pos >= vmaps.size())
                                vmaps.resize(pos + 1);
                            vmaps[pos].push_back(VMap(get(boost::vertex_index,sub)));
                            for (size_t vi = 0; vi < num_vertices(sub); ++vi)
                                vmaps[pos].back()[vertex(vi, sub)] = subgraphs[j][vi];
                        }
                    }
                }
            }
        }
    }
};

} //graph-tool namespace

#endif // GRAPH_MOTIFS_HH

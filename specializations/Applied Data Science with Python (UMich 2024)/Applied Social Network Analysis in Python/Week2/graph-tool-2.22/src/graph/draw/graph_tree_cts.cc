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

#include "graph_selectors.hh"
#include "graph_properties.hh"

#include <boost/mpl/quote.hpp>
#include <boost/graph/breadth_first_search.hpp>

#include <cmath>

using namespace std;
using namespace boost;
using namespace graph_tool;

typedef pair<double, double> point_t;

point_t interpolate(const point_t& p1, const point_t& p2, double r = 0.5)
{
    point_t ret;
    ret.first = (1 - r) * p1.first + p2.first * r;
    ret.second = (1 - r) * p1.second + p2.second * r;
    return ret;
}

double dist(point_t& p1, point_t& p2)
{
    return sqrt(pow(p1.first - p2.first, 2) + pow(p1.second - p2.second, 2));
}

void to_bezier(const vector<point_t> &x, vector<point_t>& ncp)
{
    vector<point_t> cp(x.size() + 6);
    for (size_t i = 0; i < 3; ++i)
        cp[i] = x[0];
    for (size_t i = 0; i < x.size(); ++i)
        cp[i + 3] = x[i];
    for (size_t i = cp.size() - 3; i < cp.size(); ++i)
        cp[i] = x.back();

    vector<point_t> one_thirds(cp.size() - 1);
    vector<point_t> two_thirds(cp.size() - 1);

    for (size_t i = 0; i < cp.size() - 1; ++i)
    {
        const point_t& p1 = cp[i];
        const point_t& p2 = cp[i + 1];
        one_thirds[i] = interpolate(p1, p2, 1./3);
        two_thirds[i] = interpolate(p2, p1, 1./3);
    }

    ncp.resize((cp.size() - 3) * 3);
    for (size_t i = 0; i < cp.size() - 3; ++i)
    {
        size_t pos = i * 3;
        ncp[pos] = one_thirds[i + 1];
        ncp[pos + 1] = two_thirds[i + 1];
        ncp[pos + 2] = interpolate(two_thirds[i + 1], one_thirds[i + 2]);
    }
}

void transform(vector<point_t>& cp)
{
    point_t origin = cp[0];
    for (auto& xy : cp)
    {
        xy.first -= origin.first;
        xy.second -= origin.second;
    }

    double t = atan2(cp.back().second - cp.front().second,
                     cp.back().first - cp.front().first);

    for (auto& xy : cp)
    {
        double x = xy.first;
        double y = xy.second;

        xy.first = cos(t) * x + sin(t) * y;
        xy.second = -sin(t) * x + cos(t) * y;
    }

    point_t d;
    d.first = cp.back().first - cp.front().first;
    d.second = cp.back().second - cp.front().second;
    double r = sqrt(d.first * d.first + d.second * d.second);

    for (auto& xy : cp)
        xy.first /= r;

    d.first = d.second = 0;
    cp.insert(cp.begin(), d);
}

template <class PosProp>
void get_control_points(vector<size_t>& path, PosProp& pos, double beta,
                        vector<point_t>& ncp)
{
    size_t L = path.size();
    vector<point_t> cp(L);
    for (size_t i = 0; i < L; ++i)
    {
        auto& p = pos[path[i]];
        if (p.size() < 2)
            p.resize(2);
        cp[i].first = p[0];
        cp[i].second = p[1];
    }

    ncp.resize(L);
    for (size_t i = 0; i < L; ++i)
    {
        ncp[i].first = beta * cp[i].first + (1 - beta) * (cp[0].first + (cp.back().first - cp[0].first) * i / (L - 1.));
        ncp[i].second = beta * cp[i].second + (1 - beta) * (cp[0].second + (cp.back().second - cp[0].second) * i / (L - 1.));
    }
}

template <class Graph>
void tree_path(Graph& g, size_t s, size_t t, vector<size_t>& path,
               size_t max_depth)
{
    vector<size_t> s_root;
    vector<size_t> t_root;
    s_root.push_back(s);
    t_root.push_back(t);

    size_t v = s;
    size_t u = t;

    while (v != u && s_root.size() < max_depth)
    {
        typename graph_traits<Graph>::in_edge_iterator e, e_end;
        tie(e, e_end) = in_edges(v, g);
        if (e == e_end)
            throw GraphException("Invalid hierarchical tree: No path from source to target.");
        v = source(*e, g);
        s_root.push_back(v);

        tie(e, e_end) = in_edges(u, g);
        if (e == e_end)
            throw GraphException("Invalid hierarchical tree: No path from source to target.");
        u = source(*e, g);
        if (u != v)
            t_root.push_back(u);
    }
    path = s_root;
    std::copy(t_root.rbegin(), t_root.rend(), std::back_inserter(path));
}


template <class Graph>
void graph_path(Graph& g, size_t s, size_t t, vector<size_t>& path)
{
    typename property_map_type::apply<size_t,
                                      typename property_map<Graph, vertex_index_t>::type>::type
        cpred;
    auto pred = cpred.get_unchecked(num_vertices(g));

    undirected_adaptor<Graph> ug(g);

    boost::breadth_first_search(ug, s,
                                boost::visitor(
                                    boost::make_bfs_visitor(
                                        boost::record_predecessors(
                                            pred,
                                            boost::on_tree_edge()))));
    size_t pos = t;
    path.push_back(pos);
    while (pos != s)
    {
        pos = pred[pos];
        path.push_back(pos);
    }
    std::reverse(path.begin(), path.end());
}

template<class T>
void pack(vector<point_t>& cp, vector<T>& ncp)
{
    ncp.resize(cp.size() * 2);
    for (size_t i = 0; i < cp.size(); ++i)
    {
        ncp[2 * i] = cp[i].first;
        ncp[2 * i + 1] = cp[i].second;
    }
}

struct do_get_cts
{
    template <class Graph, class Tree, class PosProp, class BProp, class CMap>
    void operator()(Graph& g, Tree& t, PosProp tpos, BProp beta, CMap cts,
                    bool is_tree, size_t max_depth) const
    {
        vector<size_t> path;
        vector<point_t> cp;
        vector<point_t> ncp;

        for (auto e : edges_range(g))
        {
            auto u = source(e, g);
            auto v = target(e, g);
            if (u == v)
                continue;

            path.clear();
            if (is_tree)
                tree_path(t, u, v, path, max_depth);
            else
                graph_path(t, u, v, path);
            cp.clear();
            get_control_points(path, tpos, beta[e], cp);
            ncp.clear();
            to_bezier(cp, ncp);
            transform(ncp);
            pack(ncp, cts[e]);
        }
    }
};

void get_cts(GraphInterface& gi, GraphInterface& tgi, boost::any otpos,
             boost::any obeta, boost::any octs, bool is_tree, size_t max_depth)
{
    typedef eprop_map_t<vector<double>>::type eprop_t;
    typedef eprop_map_t<double>::type beprop_t;

    eprop_t cts = boost::any_cast<eprop_t>(octs);
    beprop_t beta = boost::any_cast<beprop_t>(obeta);

    gt_dispatch<>()
        (std::bind(do_get_cts(), std::placeholders::_1, std::placeholders::_2,
                   std::placeholders::_3, beta, cts, is_tree, max_depth),
         graph_tool::all_graph_views(),
         graph_tool::always_directed(),
         vertex_scalar_vector_properties())
        (gi.get_graph_view(), tgi.get_graph_view(), otpos);
}

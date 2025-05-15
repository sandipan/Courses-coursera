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

// As a special exception, you have permission to link this program
// with the CGAL library and distribute executables, as long as you
// follow the requirements of the GNU GPL in regard to all of the
// software in the executable aside from CGAL.

#ifndef GRAPH_TRIANGULATION_HH
#define GRAPH_TRIANGULATION_HH

#include <tuple>
#include <functional>

#include "graph_util.hh"
#include "hash_map_wrap.hh"

namespace graph_tool
{
using namespace std;
using namespace boost;

struct hash_point
{
    template <class Vertex>
    std::size_t operator()(const Vertex& v) const
    {
        size_t seed = 42;
        _hash_combine(seed, v.point().x());
        _hash_combine(seed, v.point().y());
        _hash_combine(seed, v.point().z());
        return seed;
    }
};

template <class Triang, class IsPeriodic>
struct get_triangulation
{
    // this will insert edges in the graph
    template <class Graph, class VertexMap>
    class edge_inserter
    {
    public:
        typedef output_iterator_tag iterator_category;
        typedef typename graph_traits<Graph>::vertex_descriptor value_type;
        typedef size_t difference_type;
        typedef typename graph_traits<Graph>::vertex_descriptor* pointer;
        typedef typename graph_traits<Graph>::vertex_descriptor& reference;

        edge_inserter(Graph& g, const typename VertexMap::key_type& v,
                      VertexMap& vertex_map)
            : _g(g), _vertex_map(vertex_map), _source(vertex_map[v]) {}

        edge_inserter& operator++() { return *this; }
        edge_inserter& operator++(int) { return *this; }
        edge_inserter& operator*() { return *this; }

        template <class Vertex>
        edge_inserter& operator=(const Vertex& v)
        {
            auto iter = _vertex_map.find(*v);
            if (iter != _vertex_map.end())
            {
                auto target = iter->second;
                if (!is_adjacent(_source, target, _g) && _source != target)
                    add_edge(_source, target, _g);
            }
            return *this;
        }

    private:
        Graph& _g;
        VertexMap& _vertex_map;
        typename graph_traits<Graph>::vertex_descriptor _source;
    };


    template <class T, class VIter, class Vis>
    void incident_vertices(T& t, VIter& v_iter, Vis& vis, std::true_type) const
    {
        t.incident_vertices(v_iter, vis);
    }

    template <class T, class VIter, class Vis>
    void incident_vertices(T& t, VIter& v_iter, Vis& vis, std::false_type) const
    {
        t.finite_incident_vertices(v_iter, vis);
    }

    template <class Graph, class Points, class PosMap>
    void operator()(Graph& g, Points& points, PosMap pos) const
    {
        typedef std::unordered_map <typename Triang::Vertex,
                                    typename graph_traits<Graph>::vertex_descriptor,
                                    hash_point> vertex_map_t;
        vertex_map_t vertex_map;

        Triang T;
        for (size_t i = 0; i < points.shape()[0]; ++i)
        {
            typename Triang::Point p(points[i][0], points[i][1], points[i][2]);
            auto v = add_vertex(g);
            vertex_map[*T.insert(p)] = v;
            pos[v].resize(3);
            for (size_t j = 0; j < 3; ++j)
                pos[v][j] = points[i][j];
        }

        auto v_iter = T.finite_vertices_begin();
        auto v_end = T.finite_vertices_end();
        while (v_iter != v_end)
        {
            auto v = *v_iter;
            if (vertex_map.find(v) != vertex_map.end())
            {
                edge_inserter<Graph, vertex_map_t> insert(g, v, vertex_map);
                incident_vertices(T, v_iter, insert, IsPeriodic());
            }
            ++v_iter;
        }
    }

};

} // namespace graph_tool

#endif // GRAPH_TRIANGULATION_HH

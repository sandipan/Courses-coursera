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
#include "graph_selectors.hh"

#include <boost/python.hpp>

#include <boost/graph/johnson_all_pairs_shortest.hpp>
#include <boost/graph/floyd_warshall_shortest.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct do_all_pairs_search
{
    template <class Graph, class VertexIndexMap, class DistMap, class WeightMap>
    void operator()(const Graph& g, VertexIndexMap vertex_index,
                    DistMap dist_map, WeightMap weight, bool dense) const
    {
        typedef typename property_traits<DistMap>::value_type::value_type
            dist_t;

        parallel_vertex_loop
            (g,
             [&](auto& v)
             {
                 dist_map[v].clear();
                 dist_map[v].resize(num_vertices(g), 0);
             });

        if (dense)
        {
            floyd_warshall_all_pairs_shortest_paths
                (g, dist_map,
                 weight_map(ConvertedPropertyMap<WeightMap,dist_t>(weight)).
                 vertex_index_map(vertex_index));
        }
        else
        {
            johnson_all_pairs_shortest_paths
                (g, dist_map,
                 weight_map(ConvertedPropertyMap<WeightMap,dist_t>(weight)).
                 vertex_index_map(vertex_index));
        }
    }
};

struct do_all_pairs_search_unweighted
{
    template <class DistMap, class PredMap>
    class bfs_visitor: public boost::bfs_visitor<null_visitor>
    {
    public:
        bfs_visitor(DistMap& dist_map, PredMap& pred, size_t source)
        : _dist_map(dist_map), _pred(pred), _source(source) {}

        template <class Graph>
        void initialize_vertex(typename graph_traits<Graph>::vertex_descriptor v,
                               Graph&)
        {
            typedef typename DistMap::value_type dist_t;
            dist_t inf = std::is_floating_point<dist_t>::value ?
                numeric_limits<dist_t>::infinity() :
                numeric_limits<dist_t>::max();
            _dist_map[v] = (v == _source) ? 0 : inf;
            _pred[v] = v;
        }

        template <class Graph>
        void tree_edge(const typename graph_traits<Graph>::edge_descriptor& e,
                       Graph& g)
        {
            _pred[target(e,g)] = source(e,g);
        }

        template <class Graph>
        void discover_vertex(typename graph_traits<Graph>::vertex_descriptor v,
                             Graph&)
        {
            if (size_t(_pred[v]) == v)
                return;
            _dist_map[v] = _dist_map[_pred[v]] + 1;
        }

    private:
        DistMap& _dist_map;
        PredMap& _pred;
        size_t _source;
    };

    template <class Graph, class DistMap>
    void operator()(const Graph& g, DistMap dist_map) const
    {
        typedef typename graph_traits<Graph>::vertex_descriptor vertex_t;

        vector<vertex_t> pred_map(num_vertices(g));
        #pragma omp parallel if (num_vertices(g) > OPENMP_MIN_THRESH) \
            firstprivate(pred_map)
        parallel_vertex_loop_no_spawn
                (g,
                 [&](auto v)
                 {
                     dist_map[v].resize(num_vertices(g), 0);
                     bfs_visitor<typename std::remove_reference<decltype(dist_map[v])>::type,
                                 vector<size_t>>
                         vis(dist_map[v], pred_map, v);
                     breadth_first_search(g, v, visitor(vis));
                 });
    }
};


void get_all_dists(GraphInterface& gi, boost::any dist_map, boost::any weight,
                   bool dense)
{
    if (weight.empty())
    {
        run_action<>()
            (gi, std::bind(do_all_pairs_search_unweighted(),
                           std::placeholders::_1, std::placeholders::_2),
             vertex_scalar_vector_properties())
            (dist_map);
    }
    else
    {
        run_action<>()
            (gi, std::bind(do_all_pairs_search(), std::placeholders::_1,
                           gi.get_vertex_index(), std::placeholders::_2,
                           std::placeholders::_3, dense),
             vertex_scalar_vector_properties(),
             edge_scalar_properties())
            (dist_map, weight);
    }
}

void export_all_dists()
{
    python::def("get_all_dists", &get_all_dists);
};

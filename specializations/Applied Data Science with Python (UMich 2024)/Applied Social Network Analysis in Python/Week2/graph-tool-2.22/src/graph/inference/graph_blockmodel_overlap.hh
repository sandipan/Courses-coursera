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

#ifndef GRAPH_BLOCKMODEL_OVERLAP_HH
#define GRAPH_BLOCKMODEL_OVERLAP_HH

#include "config.h"
#include <tuple>

#include "graph_state.hh"
#include "graph_blockmodel_util.hh"
#include "graph_blockmodel_overlap_util.hh"

namespace graph_tool
{

using namespace boost;
using namespace std;

typedef vprop_map_t<int32_t>::type vmap_t;
typedef eprop_map_t<int32_t>::type emap_t;

typedef vprop_map_t<int64_t>::type vimap_t;
typedef vprop_map_t<vector<int64_t>>::type vvmap_t;

typedef mpl::vector2<std::true_type, std::false_type> use_hash_tr;

#define OVERLAP_BLOCK_STATE_params                                             \
    ((g, &, never_filtered_never_reversed, 1))                                 \
    ((use_hash,, use_hash_tr, 1))                                              \
    ((_abg, &, boost::any&, 0))                                                \
    ((node_index,, vimap_t, 0))                                                \
    ((half_edges,, vvmap_t, 0))                                                \
    ((mrs,, emap_t, 0))                                                        \
    ((mrp,, vmap_t, 0))                                                        \
    ((mrm,, vmap_t, 0))                                                        \
    ((wr,, vmap_t, 0))                                                         \
    ((b,, vmap_t, 0))                                                          \
    ((candidate_blocks, &, std::vector<size_t>&, 0))                           \
    ((bclabel,, vmap_t, 0))                                                    \
    ((pclabel,, vmap_t, 0))                                                    \
    ((deg_corr,, bool, 0))                                                     \
    ((rec_types,, std::vector<int>, 0))                                        \
    ((rec,, eprop_map_t<std::vector<double>>::type, 0))                        \
    ((drec,, eprop_map_t<std::vector<double>>::type, 0))                       \
    ((brec,, eprop_map_t<std::vector<double>>::type, 0))                       \
    ((bdrec,, eprop_map_t<std::vector<double>>::type, 0))                      \
    ((brecsum,, vprop_map_t<double>::type, 0))                                 \
    ((wparams,, std::vector<std::vector<double>>, 0))                          \
    ((allow_empty,, bool, 0))

GEN_STATE_BASE(OverlapBlockStateBase, OVERLAP_BLOCK_STATE_params)

template <class... Ts>
class OverlapBlockState
    : public OverlapBlockStateBase<Ts...>
{
public:
    GET_PARAMS_USING(OverlapBlockStateBase<Ts...>, OVERLAP_BLOCK_STATE_params)
    GET_PARAMS_TYPEDEF(Ts, OVERLAP_BLOCK_STATE_params)

    template <class RNG, class... ATs,
              typename std::enable_if_t<sizeof...(ATs) == sizeof...(Ts)>* = nullptr>
    OverlapBlockState(RNG& rng, ATs&&... args)
        : OverlapBlockStateBase<Ts...>(std::forward<ATs>(args)...),
          _bg(boost::any_cast<std::reference_wrapper<bg_t>>(__abg)),
          _c_mrs(_mrs.get_checked()),
          _c_brec(_brec.get_checked()),
          _c_bdrec(_bdrec.get_checked()),
          _emat(_bg, rng),
          _egroups_enabled(true),
          _overlap_stats(_g, _b, _half_edges, _node_index, num_vertices(_bg))
    {
        for (auto r : vertices_range(_bg))
            _wr[r] = _overlap_stats.get_block_size(r);
    }

    OverlapBlockState(const OverlapBlockState& other)
        : OverlapBlockStateBase<Ts...>
             (static_cast<const OverlapBlockStateBase<Ts...>&>(other)),
          _bg(other._bg),
          _c_mrs(other._c_mrs),
          _c_brec(_brec.get_checked()),
          _c_bdrec(_bdrec.get_checked()),
          _emat(other._emat),
          _egroups_enabled(other._egroups_enabled),
          _overlap_stats(other._overlap_stats)
    {
        if (other.is_partition_stats_enabled())
            enable_partition_stats();
    }

    template <class EOP>
    void remove_vertex(size_t v, EOP&& eop)
    {
        size_t r = _b[v];

        auto u = _overlap_stats.get_out_neighbour(v);
        if (u != _overlap_stats._null)
        {
            size_t s = _b[u];

            auto& me = _emat.get_me(r, s);

            _mrs[me] -= 1;
            _mrp[r] -= 1;
            _mrm[s] -= 1;

            auto e = *out_edges(v, _g).first;
            eop(e, me);

            assert(_mrs[me] >= 0);
            if (_mrs[me] == 0)
                _emat.remove_me(me, _bg);
        }

        u = _overlap_stats.get_in_neighbour(v);
        if (u != _overlap_stats._null)
        {
            size_t s = _b[u];

            auto& me = _emat.get_me(s, r);

            _mrs[me] -= 1;
            _mrp[s] -= 1;
            _mrm[r] -= 1;

            auto e = *in_edge_iteratorS<g_t>().get_edges(v, _g).first;
            eop(e, me);

            if (_mrs[me] == 0)
                _emat.remove_me(me, _bg);
        }

        _overlap_stats.remove_half_edge(v, r, _b, _g);
        _wr[r] = _overlap_stats.get_block_size(r);

        if (!_egroups.empty() && _egroups_enabled)
            _egroups.remove_vertex(v, _b, _g);
    }

    void remove_vertex(size_t v)
    {
        remove_vertex(v,
                      [&](auto& e, auto& me)
                      {
                          for (size_t i = 0; i < this->_rec_types.size(); ++i)
                          {
                              switch (this->_rec_types[i])
                              {
                              case weight_type::REAL_NORMAL: // signed weights
                                  this->_bdrec[me][i] -= this->_drec[e][i];
                              case weight_type::REAL_EXPONENTIAL:
                              case weight_type::DISCRETE_GEOMETRIC:
                              case weight_type::DISCRETE_POISSON:
                              case weight_type::DISCRETE_BINOMIAL:
                              case weight_type::DELTA_T:
                                  this->_brec[me][i] -= this->_rec[e][i];
                              }
                          }
                      });
    }

    template <class EOP>
    void add_vertex(size_t v, size_t r, EOP&& eop)
    {
        auto u = _overlap_stats.get_out_neighbour(v);
        if (u != _overlap_stats._null)
        {
            size_t s = r;
            if (u != v)
                s = _b[u];

            auto me = _emat.get_me(r, s);

            if (me == _emat.get_null_edge())
            {
                me = add_edge(r, s, _bg).first;
                _emat.put_me(r, s, me);
                _c_mrs[me] = 0;
                _c_brec[me].clear();
                _c_bdrec[me].clear();
            }

            assert(me == _emat.get_me(r, s));

            _mrs[me] += 1;
            _mrp[r] += 1;
            _mrm[s] += 1;

            auto e = *out_edges(v, _g).first;
            eop(e, me);
        }

        u = _overlap_stats.get_in_neighbour(v);
        if (u != _overlap_stats._null)
        {
            size_t s = _b[u];

            auto me = _emat.get_me(s, r);

            if (me == _emat.get_null_edge())
            {
                me = add_edge(s, r, _bg).first;
                _emat.put_me(s, r, me);
                _c_mrs[me] = 0;
                _c_brec[me].clear();
                _c_bdrec[me].clear();
            }

            assert(me == _emat.get_me(s, r));

            _mrs[me] += 1;
            _mrp[s] += 1;
            _mrm[r] += 1;
            auto e = *in_edge_iteratorS<g_t>().get_edges(v, _g).first;
            eop(e, me);
        }

        _overlap_stats.add_half_edge(v, r, _b, _g);
        _wr[r] = _overlap_stats.get_block_size(r);

        _b[v] = r;

        if (!_egroups.empty() && _egroups_enabled)
            _egroups.add_vertex(v, _b, _eweight, _g);
    }

    void add_vertex(size_t v, size_t r)
    {
        add_vertex(v, r,
                   [&](auto& e, auto& me)
                   {
                       this->_brec[me].resize(this->_rec_types.size());
                       this->_bdrec[me].resize(this->_rec_types.size());
                       for (size_t i = 0; i < this->_rec_types.size(); ++i)
                       {
                           switch (this->_rec_types[i])
                           {
                           case weight_type::REAL_NORMAL: // signed weights
                               this->_bdrec[me][i] += this->_drec[e][i];
                           case weight_type::REAL_EXPONENTIAL:
                           case weight_type::DISCRETE_GEOMETRIC:
                           case weight_type::DISCRETE_POISSON:
                           case weight_type::DISCRETE_BINOMIAL:
                           case weight_type::DELTA_T:
                               this->_brec[me][i] += this->_rec[e][i];
                           }
                       }
                   });
    }

    bool allow_move(size_t r, size_t nr)
    {
        return (_bclabel[r] == _bclabel[nr]);
    }

    // move a vertex from its current block to block nr
    void move_vertex(size_t v, size_t nr)
    {
        size_t r = _b[v];
        if (r == nr)
            return;

        if (!allow_move(r, nr))
            throw ValueException("cannot move vertex across clabel barriers");

        if (is_partition_stats_enabled())
            get_partition_stats(v).move_vertex(v, _b[v], nr, _deg_corr, _g);

        remove_vertex(v);
        add_vertex(v, nr);
    }

    template <class Vec>
    void move_vertices(Vec& v, Vec& nr)
    {
        for (size_t i = 0; i < std::min(v.size(), nr.size()); ++i)
            move_vertex(v[i], nr[i]);
    }

    void move_vertices(python::object ovs, python::object ors)
    {
        multi_array_ref<uint64_t, 1> vs = get_array<uint64_t, 1>(ovs);
        multi_array_ref<uint64_t, 1> rs = get_array<uint64_t, 1>(ors);
        if (vs.size() != rs.size())
            throw ValueException("vertex and group lists do not have the same size");
        move_vertices(vs, rs);
    }

    template <class VMap>
    void set_partition(VMap&& b)
    {
        for (auto v : vertices_range(_g))
            move_vertex(v, b[v]);
    }

    void set_partition(boost::any& ab)
    {
        vmap_t& b = boost::any_cast<vmap_t&>(ab);
        set_partition<typename vmap_t::unchecked_t>(b.get_unchecked());
    }

    size_t virtual_remove_size(size_t v)
    {
        return _overlap_stats.virtual_remove_size(v, _b[v]);
    }

    template <class MEntries>
    void get_move_entries(size_t v, size_t r, size_t nr, MEntries& m_entries) const
    {
        auto mv_entries = [&](auto&&... args)
            {
                move_entries(v, r, nr, _b, _g, _eweight, m_entries,
                             [](auto) { return false; },
                             is_loop_overlap(_overlap_stats), args...);
            };

        int rec_type = weight_type::NONE;
        for (auto rt : _rec_types)
        {
            rec_type = rt;
            if (rt == weight_type::REAL_NORMAL)
                break;
        }

        switch (rec_type)
        {
        case weight_type::REAL_EXPONENTIAL:
            mv_entries(_rec);
            break;
        case weight_type::REAL_NORMAL:
            mv_entries(_rec, _drec);
            break;
        default: // no weights
            mv_entries();
        }
    }

    // compute the entropy difference of a virtual move of vertex from block r to nr
    template <bool exact, class MEntries>
    double virtual_move_sparse(size_t v, size_t nr, bool multigraph,
                               MEntries& m_entries) const
    {
        size_t r = _b[v];

        if (r == nr)
            return 0.;

        size_t kout = out_degreeS()(v, _g);
        size_t kin = 0;
        if (is_directed::apply<g_t>::type::value)
            kin = in_degreeS()(v, _g);

        double dS = entries_dS<exact>(m_entries, _mrs, _emat, _bg);

        int dwr = _wr[r] - _overlap_stats.virtual_remove_size(v, r, kin, kout);
        int dwnr = _overlap_stats.virtual_add_size(v, nr) - _wr[nr];

        if (_deg_corr)
            dS += _overlap_stats.virtual_move_dS(v, r, nr, _g, kin, kout);

        if (multigraph)
            dS += _overlap_stats.virtual_move_parallel_dS(v, r, nr, _b, _g);

        if (!is_directed::apply<g_t>::type::value)
            kin = kout;

        auto vt = [&](auto mrp, auto mrm, auto nr)
            {
                if (exact)
                    return vterm_exact(mrp, mrm, nr, _deg_corr, _bg);
                else
                    return vterm(mrp, mrm, nr, _deg_corr, _bg);
            };

        dS += vt(_mrp[r]  - kout, _mrm[r]  - kin, _wr[r]  - dwr );
        dS += vt(_mrp[nr] + kout, _mrm[nr] + kin, _wr[nr] + dwnr);
        dS -= vt(_mrp[r]        , _mrm[r]       , _wr[r]        );
        dS -= vt(_mrp[nr]       , _mrm[nr]      , _wr[nr]       );

        return dS;
    }

    template <bool exact>
    double virtual_move_sparse(size_t v, size_t nr, bool multigraph)
    {
        return virtual_move_sparse<exact>(v, nr, multigraph, _m_entries);
    }

    template <class MEntries>
    double virtual_move_dense(size_t, size_t, bool, MEntries&) const
    {
        throw GraphException("Dense entropy for overlapping model not implemented!");
    }

    double virtual_move_dense(size_t v, size_t nr, bool multigraph)
    {
        return virtual_move_dense(v, nr, multigraph, _m_entries);
    }

    template <class MEntries>
    double virtual_move(size_t v, size_t r, size_t nr, entropy_args_t ea,
                        MEntries& m_entries)
    {
        if (r == nr)
            return 0;

        if (!allow_move(r, nr))
            return std::numeric_limits<double>::infinity();

        get_move_entries(v, r, nr, m_entries);

        double dS = 0;
        if (ea.adjacency)
        {
            if (ea.exact)
                dS = virtual_move_sparse<true>(v, nr, ea.multigraph, m_entries);
            else
                dS = virtual_move_sparse<false>(v, nr, ea.multigraph, m_entries);
        }

        if (ea.partition_dl || ea.degree_dl || ea.edges_dl)
        {
            enable_partition_stats();
            auto& ps = get_partition_stats(v);
            if (ea.partition_dl)
                dS += ps.get_delta_partition_dl(v, r, nr, _g);
            if (_deg_corr && ea.degree_dl)
                dS += ps.get_delta_deg_dl(v, r, nr, _eweight, _g);
            if (ea.edges_dl)
            {
                size_t actual_B = 0;
                for (auto& ps : _partition_stats)
                    actual_B += ps.get_actual_B();
                dS += ps.get_delta_edges_dl(v, r, nr, actual_B, _g);
            }
        }


        auto positive_entries_op = [&](size_t i, auto&& w_log_P)
            {
                entries_op(m_entries, this->_emat,
                           [&](auto, auto, auto& me, auto& delta)
                           {
                               size_t ers = 0;
                               double xrs = 0;
                               if (me != _emat.get_null_edge())
                               {
                                   ers = this->_mrs[me];
                                   xrs = this->_brec[me][i];
                               }
                               auto d = get<0>(delta);
                               auto dx = get<1>(delta)[i];
                               dS -= -w_log_P(ers, xrs);
                               dS += -w_log_P(ers + d, xrs + dx);
                           });
            };

        for (size_t i = 0; i < _rec_types.size(); ++i)
        {
            auto& wparams = _wparams[i];
            switch (_rec_types[i])
            {
            case weight_type::REAL_EXPONENTIAL:
                positive_entries_op(i,
                                    [&](auto N, auto x)
                                    { return positive_w_log_P(N, x,
                                                              wparams[0],
                                                              wparams[1]);
                                    });
                break;
            case weight_type::DISCRETE_GEOMETRIC:
                positive_entries_op(i,
                                    [&](auto N, auto x)
                                    { return geometric_w_log_P(N, x,
                                                               wparams[0],
                                                               wparams[1]);
                                    });
                break;
            case weight_type::DISCRETE_POISSON:
                positive_entries_op(i,
                                    [&](auto N, auto x)
                                    { return poisson_w_log_P(N, x,
                                                             wparams[0],
                                                             wparams[1]);
                                    });
                break;
            case weight_type::DISCRETE_BINOMIAL:
                positive_entries_op(i,
                                    [&](auto N, auto x)
                                    { return binomial_w_log_P(N, x,
                                                              wparams[0],
                                                              wparams[1],
                                                              wparams[2]);
                                    });
                break;
            case weight_type::REAL_NORMAL:
                entries_op(m_entries, _emat,
                           [&](auto, auto, auto& me, auto& delta)
                           {
                               size_t ers = 0;
                               double xrs = 0, x2rs = 0;
                               if (me != _emat.get_null_edge())
                               {
                                   ers = this->_mrs[me];
                                   xrs = this->_brec[me][i];
                                   x2rs = this->_bdrec[me][i];
                               }
                               auto d = get<0>(delta);
                               auto dx = get<1>(delta)[i];
                               auto dx2 = get<2>(delta)[i];
                               auto sigma1 = x2rs - xrs * (xrs / ers);
                               auto sigma2 = x2rs + dx2 - (xrs + dx) * ((xrs + dx) / (ers + d));
                               dS -= -signed_w_log_P(ers, xrs, sigma1,
                                                     wparams[0],
                                                     wparams[1],
                                                     wparams[2],
                                                     wparams[3]);
                               dS += -signed_w_log_P(ers + d, xrs + dx,
                                                     sigma2,
                                                     wparams[0],
                                                     wparams[1],
                                                     wparams[2],
                                                     wparams[3]);
                           });
            break;
            }
        }
        return dS;
    }

    double virtual_move(size_t v, size_t r, size_t nr, entropy_args_t ea)
    {
        return virtual_move(v, r, nr, ea, _m_entries);
    }

    double get_delta_partition_dl(size_t v, size_t r, size_t nr)
    {
        enable_partition_stats();
        return get_partition_stats(v).get_delta_partition_dl(v, r, nr, _g);
    }

    // Sample node placement
    template <class RNG>
    size_t sample_block(size_t v, double c, RNG& rng)
    {
        // attempt random block
        size_t s = uniform_sample(_candidate_blocks, rng);

        if (!std::isinf(c))
        {
            size_t w = get_lateral_half_edge(v, rng);

            size_t u = _overlap_stats.get_out_neighbour(w);
            if (u >= num_vertices(_g))
                u = _overlap_stats.get_in_neighbour(w);

            size_t t = _b[u];
            double p_rand = 0;
            if (c > 0)
            {
                size_t B = num_vertices(_bg);
                if (is_directed::apply<g_t>::type::value)
                    p_rand = c * B / double(_mrp[t] + _mrm[t] + c * B);
                else
                    p_rand = c * B / double(_mrp[t] + c * B);
            }

            typedef std::uniform_real_distribution<> rdist_t;
            if (c == 0 || rdist_t()(rng) >= p_rand)
            {
                if (_egroups.empty())
                    _egroups.init(_b, _eweight, _g, _bg);
                const auto& e = _egroups.sample_edge(t, rng);
                s = _b[target(e, _g)];
                if (s == t)
                    s = _b[source(e, _g)];
            }
        }

        return s;
    }

    size_t sample_block(size_t v, double c, rng_t& rng)
    {
        return sample_block<rng_t>(v, c, rng);
    }

    template <class RNG>
    size_t get_lateral_half_edge(size_t v, RNG& rng)
    {
        size_t vv = _overlap_stats.get_node(v);
        size_t w = _overlap_stats.sample_half_edge(vv, rng);
        return w;
    }

    template <class RNG>
    size_t random_neighbour(size_t v,  RNG& rng)
    {
        size_t w = get_lateral_half_edge(v, _overlap_stats, rng);

        size_t u = _overlap_stats.get_out_neighbour(w);
        if (u >= num_vertices(_g))
            u = _overlap_stats.get_in_neighbour(w);
        return u;
    }

    // Computes the move proposal probability
    template <class MEntries>
    double get_move_prob(size_t v, size_t r, size_t s, double c, bool reverse,
                         MEntries& m_entries)
    {
        typedef typename graph_traits<g_t>::vertex_descriptor vertex_t;
        size_t B = num_vertices(_bg);
        double p = 0;
        size_t w = 0;

        size_t kout = out_degreeS()(v, _g, _eweight);
        size_t kin = kout;
        if (is_directed::apply<g_t>::type::value)
            kin = in_degreeS()(v, _g, _eweight);

        size_t vi = _overlap_stats.get_node(v);
        auto& ns = _overlap_stats.get_half_edges(vi);

        for (size_t v: ns)
        {
            for (auto e : all_edges_range(v, _g))
            {
                vertex_t u = target(e, _g);
                if (is_directed::apply<g_t>::type::value && u == v)
                    u = source(e, _g);
                vertex_t t = _b[u];
                if (u == v)
                    t = r;
                size_t ew = _eweight[e];
                w += ew;

                int mts = 0;
                const auto& me = m_entries.get_me(t, s, _emat);
                if (me != _emat.get_null_edge())
                    mts = _mrs[me];
                int mtp = _mrp[t];
                int mst = mts;
                int mtm = mtp;

                if (is_directed::apply<g_t>::type::value)
                {
                    mst = 0;
                    const auto& me = m_entries.get_me(s, t, _emat);
                    if (me != _emat.get_null_edge())
                        mst = _mrs[me];
                    mtm = _mrm[t];
                }

                if (reverse)
                {
                    int dts = get<0>(m_entries.get_delta(t, s));
                    int dst = dts;
                    if (is_directed::apply<g_t>::type::value)
                        dst = get<0>(m_entries.get_delta(s, t));

                    mts += dts;
                    mst += dst;

                    if (t == s)
                    {
                        mtp -= kout;
                        mtm -= kin;
                    }

                    if (t == r)
                    {
                        mtp += kout;
                        mtm += kin;
                    }
                }

                if (is_directed::apply<g_t>::type::value)
                {
                    p += ew * ((mts + mst + c) / (mtp + mtm + c * B));
                }
                else
                {
                    if (t == s)
                        mts *= 2;
                    p += ew * (mts + c) / (mtp + c * B);
                }
            }
        }
        if (w > 0)
            return p / w;
        else
            return 1. / B;
    }

    double get_move_prob(size_t v, size_t r, size_t s, double c, bool reverse)
    {
        return get_move_prob(v, r, s, c, reverse, _m_entries);
    }

    bool is_last(size_t v)
    {
        auto r = _b[v];
        return _overlap_stats.virtual_remove_size(v, r) == 0;
    }

    size_t node_weight(size_t)
    {
        return 1;
    }

    double sparse_entropy(bool multigraph, bool deg_entropy, bool exact) const
    {
        double S = 0;
        if (exact)
        {
            for (auto e : edges_range(_bg))
                S += eterm_exact(source(e, _bg), target(e, _bg), _mrs[e], _bg);
            for (auto v : vertices_range(_bg))
                S += vterm_exact(_mrp[v], _mrm[v], _wr[v], _deg_corr, _bg);
        }
        else
        {
            for (auto e : edges_range(_bg))
                S += eterm(source(e, _bg), target(e, _bg), _mrs[e], _bg);
            for (auto v : vertices_range(_bg))
                S += vterm(_mrp[v], _mrm[v], _wr[v], _deg_corr, _bg);
        }

        if (_deg_corr && deg_entropy)
        {
            typedef gt_hash_map<int, int> map_t;

            map_t in_hist, out_hist;
            size_t N = _overlap_stats.get_N();

            for (size_t v = 0; v < N; ++v)
            {
                in_hist.clear();
                out_hist.clear();

                const auto& half_edges = _overlap_stats.get_half_edges(v);
                for (size_t u : half_edges)
                {
                    in_hist[_b[u]] += in_degreeS()(u, _g);
                    out_hist[_b[u]] += out_degree(u, _g);
                }

                for (auto& k_c : in_hist)
                    S -= lgamma_fast(k_c.second + 1);
                for (auto& k_c : out_hist)
                    S -= lgamma_fast(k_c.second + 1);
            }
        }

        if (multigraph)
        {
            for (const auto& h : _overlap_stats.get_parallel_bundles())
            {
                for (const auto& kc : h)
                {
                    if (kc.first.first == kc.first.second)
                    {
                        S += lgamma_fast(kc.second + 1) + kc.second * log(2);
                    }
                    else
                    {
                        S += lgamma_fast(kc.second + 1);
                    }
                }
            }
        }
        return S;
    }

    double dense_entropy(bool)
    {
        throw GraphException("Dense entropy for overlapping model not implemented!");
    }

    double entropy(bool dense, bool multigraph, bool deg_entropy, bool exact,
                   bool recs)
    {
        double S = 0;
        if (dense)
            S = dense_entropy(multigraph);
        else
            S = sparse_entropy(multigraph, deg_entropy, exact);

        if (recs)
        {
            for (size_t i = 0; i < _rec_types.size(); ++i)
            {
                switch (_rec_types[i])
                {
                case weight_type::REAL_EXPONENTIAL:
                    for (auto me : edges_range(_bg))
                    {
                        auto ers = _mrs[me];
                        auto xrs = _brec[me][i];
                        S += -positive_w_log_P(ers, xrs,
                                               _wparams[i][0],
                                               _wparams[i][1]);
                    }
                    break;
                case weight_type::DISCRETE_GEOMETRIC:
                    for (auto me : edges_range(_bg))
                    {
                        auto ers = _mrs[me];
                        auto xrs = _brec[me][i];
                        S += -geometric_w_log_P(ers, xrs,
                                                _wparams[i][0],
                                                _wparams[i][1]);
                    }
                    break;
                case weight_type::DISCRETE_POISSON:
                    for (auto me : edges_range(_bg))
                    {
                        auto ers = _mrs[me];
                        auto xrs = _brec[me][i];
                        S += -poisson_w_log_P(ers, xrs,
                                              _wparams[i][0],
                                              _wparams[i][1]);
                    }
                    for (auto e : edges_range(_g))
                        S += boost::math::lgamma(_rec[e][i] + 1);
                    break;
                case weight_type::DISCRETE_BINOMIAL:
                    for (auto me : edges_range(_bg))
                    {
                        auto ers = _mrs[me];
                        auto xrs = _brec[me][i];
                        S += -binomial_w_log_P(ers, xrs,
                                               _wparams[i][0],
                                               _wparams[i][1],
                                               _wparams[i][2]);
                    }
                    for (auto e : edges_range(_g))
                        S -= lbinom(_wparams[i][0], _rec[e][i]);
                    break;
                case weight_type::REAL_NORMAL:
                    for (auto me : edges_range(_bg))
                    {
                        auto ers = _mrs[me];
                        auto xrs = _brec[me][i];
                        auto x2rs = _bdrec[me][i];
                        auto sigma = x2rs - xrs * (xrs / ers);
                        S += -signed_w_log_P(ers, xrs, sigma,
                                             _wparams[i][0],
                                             _wparams[i][1],
                                             _wparams[i][2],
                                             _wparams[i][3]);
                    }
                    break;
                }
            }
        }
        return S;
    }

    double get_partition_dl()
    {
        if (!is_partition_stats_enabled())
            enable_partition_stats();
        double S = 0;
        for (auto& ps : _partition_stats)
            S += ps.get_partition_dl();
        return S;
    }

    double get_deg_dl(int kind)
    {
        if (!is_partition_stats_enabled())
            enable_partition_stats();
        double S = 0;
        for (auto& ps : _partition_stats)
            S += ps.get_deg_dl(kind);
        return S;
    }

    double get_parallel_entropy()
    {
        double S = 0;
        for (auto& h : _overlap_stats.get_parallel_bundles())
        {
            for (auto& kc : h)
                S += lgamma_fast(kc.second + 1);
        }
        return S;
    }

    void enable_partition_stats()
    {
        if (_partition_stats.empty())
        {

            size_t E = num_vertices(_g) / 2;
            size_t B = num_vertices(_bg);

            auto vi = std::max_element(vertices(_g).first, vertices(_g).second,
                                       [&](auto u, auto v)
                                       { return this->_pclabel[u] < this->_pclabel[v];});
            size_t C = _bclabel[*vi] + 1;

            vector<gt_hash_set<size_t>> vcs(C);
            vector<size_t> rc(num_vertices(_bg));
            for (auto v : vertices_range(_g))
            {
                vcs[_pclabel[v]].insert(_overlap_stats.get_node(v));
                rc[_b[v]] = _pclabel[v];
            }

            for (size_t c = 0; c < C; ++c)
                _partition_stats.emplace_back(_g, _b, vcs[c], E, B,
                                              _eweight, _overlap_stats,
                                              _bmap, _vmap, _allow_empty);

            for (size_t r = 0; r < num_vertices(_bg); ++r)
                _partition_stats[rc[r]].get_r(r);
        }
    }

    void disable_partition_stats()
    {
        _partition_stats.clear();
    }

    bool is_partition_stats_enabled() const
    {
        return !_partition_stats.empty();
    }

    overlap_partition_stats_t& get_partition_stats(size_t v)
    {
        return _partition_stats[_pclabel[v]];
    }

    template <class Graph, class EMap>
    void get_be_overlap(Graph& g, EMap be)
    {
        for (auto ei : edges_range(_g))
        {
            auto u = source(ei, _g);
            auto v = target(ei, _g);

            auto s = vertex(_node_index[u], g);
            auto t = vertex(_node_index[v], g);

            for (auto e : out_edges_range(s, g))
            {
                if (!be[e].empty() || target(e, g) != t)
                    continue;
                if (is_directed::apply<Graph>::type::value || s < target(e, g))
                    be[e] = {_b[u], _b[v]};
                else
                    be[e] = {_b[v], _b[u]};
                break;
            }

            for (auto e : in_edges_range(t, g))
            {
                if (!be[e].empty() || source(e, g) != s)
                    continue;
                be[e] = {_b[u], _b[v]};
                break;
            }
        }
    }

    template <class Graph, class VMap>
    void get_bv_overlap(Graph& g, VMap bv, VMap bc_in, VMap bc_out,
                        VMap bc_total)
    {
        typedef gt_hash_map<int, int> map_t;
        vector<map_t> hist_in;
        vector<map_t> hist_out;

        for (auto v : vertices_range(_g))
        {
            if (out_degree(v, _g) > 0)
            {
                size_t s = _node_index[v];
                if (s >= hist_out.size())
                    hist_out.resize(s + 1);
                hist_out[s][_b[v]]++;
            }

            if (in_degreeS()(v, _g) > 0)
            {
                size_t t = _node_index[v];
                if (t >= hist_in.size())
                    hist_in.resize(t + 1);
                hist_in[t][_b[v]]++;
            }
        }

        hist_in.resize(num_vertices(g));
        hist_out.resize(num_vertices(g));

        set<size_t> rs;
        for (auto i : vertices_range(g))
        {
            rs.clear();
            for (auto iter = hist_out[i].begin(); iter != hist_out[i].end(); ++iter)
                rs.insert(iter->first);
            for (auto iter = hist_in[i].begin(); iter != hist_in[i].end(); ++iter)
                rs.insert(iter->first);
            // if (rs.empty())
            //     throw GraphException("Cannot have empty overlapping block membership!");
            for (size_t r : rs)
            {
                bv[i].push_back(r);

                auto iter_in = hist_in[i].find(r);
                if (iter_in != hist_in[i].end())
                    bc_in[i].push_back(iter_in->second);
                else
                    bc_in[i].push_back(0);

                auto iter_out = hist_out[i].find(r);
                if (iter_out != hist_out[i].end())
                    bc_out[i].push_back(iter_out->second);
                else
                    bc_out[i].push_back(0);

                bc_total[i].push_back(bc_in[i].back() +
                                      bc_out[i].back());
            }
        }
    }

    template <class Graph, class VVProp, class VProp>
    void get_overlap_split(Graph& g, VVProp bv, VProp b) const
    {
        gt_hash_map<vector<int>, size_t> bvset;

        for (auto v : vertices_range(g))
        {
            auto r = bv[v];
            auto iter = bvset.find(r);
            if (iter == bvset.end())
                iter = bvset.insert(make_pair(r, bvset.size())).first;
            b[v] = iter->second;
        }
    }


    void init_mcmc(double c, double dl)
    {
        if (!std::isinf(c))
        {
            if (_egroups.empty())
                _egroups.init(_b, _eweight, _g, _bg);
        }
        else
        {
            _egroups.clear();
        }

        if (dl)
            enable_partition_stats();
        else
            disable_partition_stats();
    }

    bool check_edge_counts()
    {
        gt_hash_map<std::pair<size_t, size_t>, size_t> mrs;
        for (auto e : edges_range(_g))
        {
            size_t r = _b[source(e, _g)];
            size_t s = _b[target(e, _g)];
            if (!is_directed::apply<g_t>::type::value && s < r)
                std::swap(r, s);
            mrs[std::make_pair(r, s)] += _eweight[e];
        }

        for (auto& rs_m : mrs)
        {
            auto r = rs_m.first.first;
            auto s = rs_m.first.second;
            auto me = _emat.get_me(r, s);
            if (me == _emat.get_null_edge())
            {
                assert(false);
                return false;
            }
            if (size_t(_mrs[me]) != rs_m.second)
            {
                assert(false);
                return false;
            }
        }
        return true;
    }

//private:
    typedef typename
        std::conditional<is_directed::apply<g_t>::type::value,
                         GraphInterface::multigraph_t,
                         undirected_adaptor<GraphInterface::multigraph_t>>::type
        bg_t;
    bg_t& _bg;

    typename mrs_t::checked_t _c_mrs;
    typename brec_t::checked_t _c_brec;
    typename bdrec_t::checked_t _c_bdrec;

    typedef typename std::conditional<use_hash_t::value,
                                      EHash<bg_t>,
                                      EMat<bg_t>>::type
        emat_t;
    emat_t _emat;

    EGroups<g_t, mpl::false_> _egroups;
    bool _egroups_enabled;

    overlap_stats_t _overlap_stats;
    std::vector<overlap_partition_stats_t> _partition_stats;
    std::vector<size_t> _bmap;
    std::vector<size_t> _vmap;

    typedef SingleEntrySet<g_t, bg_t, int, std::vector<double>,
                           std::vector<double>> m_entries_t;
    m_entries_t _m_entries;

    UnityPropertyMap<int,GraphInterface::edge_t> _eweight;
    UnityPropertyMap<int,GraphInterface::vertex_t> _vweight;

    std::array<size_t, 0> _empty_blocks;

};

} // namespace graph_tool

#endif // GRAPH_BLOCKMODEL_OVERLAP_HH

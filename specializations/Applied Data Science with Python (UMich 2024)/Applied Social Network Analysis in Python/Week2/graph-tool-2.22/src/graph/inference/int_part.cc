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

#include <boost/math/special_functions/zeta.hpp>
#include <boost/math/special_functions/gamma.hpp>

#include "graph_tool.hh"
#include "hash_map_wrap.hh"
#include "int_part.hh"
#include "util.hh"

double spence(double);

namespace graph_tool
{

using namespace std;

boost::multi_array<double, 2> __q_cache;

void init_q_cache(size_t n_max)
{
    size_t old_n = __q_cache.shape()[0];
    if (old_n >= n_max)
        return;

    __q_cache.resize(boost::extents[0][0]);
    __q_cache.resize(boost::extents[n_max + 1][n_max + 1]);

    for (size_t n = 1; n <= n_max; ++n)
    {
        __q_cache[n][1] = 1;
        for (size_t k = 2; k <= n; ++k)
        {
            __q_cache[n][k] += __q_cache[n][k - 1];
            if (n > k)
                __q_cache[n][k] += __q_cache[n - k][k];
        }
    }

    for (size_t n = 0; n < __q_cache.shape()[0]; ++n)
    {
        for (size_t k = 0; k < __q_cache.shape()[1]; ++k)
        {
            auto& x = __q_cache[n][k];
            x = log(x);
        }
    }
}

double q_rec(int n, int k)
{
    if (n <= 0 || k < 1)
        return 0;
    if (k > n)
        k = n;
    if (k == 1)
        return 1;
    return q_rec(n, k - 1) + q_rec(n - k, k);
}

gt_hash_map<pair<int, int>, double> __q_memo;

double q_rec_memo(int n, int k)
{
    if (k > n || n <= 0 || k < 1)
        return 0;
    if (k > n)
        k = n;
    if (k == 1)
        return 1;
    auto key = make_pair(n, k);
    auto iter = __q_memo.find(key);
    if (iter != __q_memo.end())
        return iter->second;
    auto res = q_rec_memo(n, k - 1) + q_rec_memo(n - k, k);
    __q_memo[key] = res;
    return res;
}

double log_q_approx_big(int n, int k)
{
    double C = M_PI * sqrt(2/3.);
    double S = C * sqrt(n) - log(4 * sqrt(3) * n);
    if (k < n)
    {
        double x = k / sqrt(n) - log(n) / C;
        S -= (2 / C) * exp(-C * x / 2);
    }
    return S;
}

double log_q_approx_small(int n, int k)
{
    return lbinom_fast(n - 1, k - 1) - lgamma_fast(k + 1);
}

double get_v(double u, double epsilon=1e-8)
{
    double v = u;
    double delta = 1;
    while (delta > epsilon)
    {
        double n_v = u * sqrt(-v*v/2 - spence(exp(v)));
        delta = abs(n_v - v);
        v = n_v;
    }
    return v;
}

double log_q_approx(int n, int k)
{
    if (k < pow(n, 1/4.))
        return log_q_approx_small(n, k);
    double u = k / sqrt(n);
    double v = get_v(u);
    double lf = log(v) - log(1 - exp(-v) * (1 + u * u/2)) / 2 - log(2) * 3 / 2
        - log(u) - log(M_PI);
    double g = 2 * v / u - u * log(1-exp(-v));
    return lf - log(n) + sqrt(n) * g;
}


} // namespace graph_tool

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

#ifndef UTIL_HH
#define UTIL_HH

#include "config.h"

#include <cmath>
#include <iostream>

#include "cache.hh"

namespace graph_tool
{
using namespace boost;

inline double lbinom(double N, double k)
{
    if (N == 0 || k == 0 || k > N)
        return 0;
    assert(N > 0);
    assert(k > 0);
    return ((lgamma(N + 1) - lgamma(k + 1)) - lgamma(N - k + 1));
}

inline double lbinom_fast(int N, int k)
{
    if (N == 0 || k == 0 || k > N)
        return 0;
    return ((lgamma_fast(N + 1) - lgamma_fast(k + 1)) - lgamma_fast(N - k + 1));
}

inline double lbinom_careful(double N, double k)
{
    if (N == 0 || k == 0 || k >= N)
        return 0;
    double lgN = lgamma(N + 1);
    double lgk = lgamma(k + 1);
    if (lgN - lgk > 1e8)
    {
        // We have N >> k. Use Stirling's approximation: ln N! ~ N ln N - N
        // and reorder
        return - N * log1p(-k / N) - k * log1p(-k / N) - k - lgk + k * log(N);
    }
    else
    {
        return lgN - lgamma(N - k + 1) - lgk;
    }
}

inline double lbeta(double x, double y)
{
    return lgamma(x) + lgamma(y) - lgamma(x + y);
}

template <class Vec, class PosMap, class Val>
void remove_element(Vec& vec, PosMap& pos, Val val)
{
    auto& back = vec.back();
    auto& j = pos[back];
    auto i = pos[val];
    vec[i] = back;
    j = i;
    vec.pop_back();
}

template <class Vec, class PosMap, class Val>
void add_element(Vec& vec, PosMap& pos, Val val)
{
    pos[val] = vec.size();
    vec.push_back(val);
}

template <class Vec, class PosMap, class Val>
bool has_element(Vec& vec, PosMap& pos, Val val)
{
    size_t i = pos[val];
    return (i < vec.size() && vec[i] == val);
}


} // namespace graph_tool




#endif // UTIL_HH

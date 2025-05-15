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

#ifndef CACHE_HH
#define CACHE_HH

#include "config.h"

#include <vector>
#include <cmath>

#include <boost/math/special_functions/gamma.hpp>

namespace graph_tool
{
using namespace std;

// Repeated computation of x*log(x) and log(x) actually adds up to a lot of
// time. A significant speedup can be made by caching pre-computed values.

extern vector<double> __safelog_cache;
extern vector<double> __xlogx_cache;
extern vector<double> __lgamma_cache;

void init_safelog(size_t x);

template <class Type>
inline double safelog(Type x)
{
    if (x == 0)
        return 0;
    return log(x);
}

inline double safelog(size_t x)
{
    if (x >= __safelog_cache.size())
        init_safelog(x);
    return __safelog_cache[x];
}

void init_xlogx(size_t x);

inline double xlogx(size_t x)
{
    //return x * safelog(x);
    if (x >= __xlogx_cache.size())
        init_xlogx(x);
    return __xlogx_cache[x];
}

void init_lgamma(size_t x);

inline double lgamma_fast(size_t x)
{
    //return lgamma(x);
    if (x >= __lgamma_cache.size())
        init_lgamma(x);
    return __lgamma_cache[x];
}

void init_cache(size_t E);

} // graph_tool namespace

#endif //CACHE_HH

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

#include "cache.hh"

namespace graph_tool
{

using namespace std;

vector<double> __safelog_cache;
vector<double> __xlogx_cache;
vector<double> __lgamma_cache;

void init_safelog(size_t x)
{
    #pragma omp critical (_safelog_)
    {
        size_t old_size = __safelog_cache.size();
        if (x >= old_size)
        {
            __safelog_cache.resize(x + 1);
            for (size_t i = old_size; i < __safelog_cache.size(); ++i)
                __safelog_cache[i] = safelog(double(i));
        }
    }
}

void clear_safelog()
{
    vector<double>().swap(__safelog_cache);
}


void init_xlogx(size_t x)
{
    #pragma omp critical (_xlogx_)
    {
        size_t old_size = __xlogx_cache.size();
        if (x >= old_size)
        {
            __xlogx_cache.resize(x + 1);
            for (size_t i = old_size; i < __xlogx_cache.size(); ++i)
                __xlogx_cache[i] = i * safelog(i);
        }
    }
}

void clear_xlogx()
{
    vector<double>().swap(__xlogx_cache);
}

void init_lgamma(size_t x)
{
    #pragma omp critical (_lgamma_)
    {
        size_t old_size = __lgamma_cache.size();
        if (x >= old_size)
        {
            __lgamma_cache.resize(x + 1);
            if (old_size == 0)
                __lgamma_cache[0] = numeric_limits<double>::infinity();
            for (size_t i = std::max(old_size, size_t(1));
                 i < __lgamma_cache.size(); ++i)
                __lgamma_cache[i] = lgamma(i);
        }
    }
}

void clear_lgamma()
{
    vector<double>().swap(__lgamma_cache);
}

void init_cache(size_t E)
{
    init_lgamma(2 * E);
    init_xlogx(2 * E);
    init_safelog(2 * E);
}


} // namespace graph_tool

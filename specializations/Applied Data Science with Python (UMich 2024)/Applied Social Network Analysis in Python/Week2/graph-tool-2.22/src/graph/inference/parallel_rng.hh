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

#ifndef PARALLEL_RNG_HH
#define PARALLEL_RNG_HH

#include <vector>

template <class RNG>
void init_rngs(std::vector<std::shared_ptr<RNG>>& rngs, RNG& rng)
{
    size_t num_threads = 1;
#ifdef USING_OPENMP
    num_threads = omp_get_max_threads();
#endif
    for (size_t i = 0; i < num_threads; ++i)
    {
        std::array<int, RNG::state_size> seed_data;
        std::generate_n(seed_data.data(), seed_data.size(), std::ref(rng));
        std::seed_seq seq(std::begin(seed_data), std::end(seed_data));
        rngs.push_back(std::make_shared<rng_t>(seq));
    }
}

template <class RNG>
RNG& get_rng(std::vector<std::shared_ptr<RNG>>& rngs, RNG& rng)
{
    if (rngs.empty())
        return rng;
    size_t tid = 0;
#ifdef USING_OPENMP
    tid = omp_get_thread_num();
#endif
    return *rngs[tid];
};

#endif // PARALLEL_RNG_HH

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

#ifndef SAMPLER_HH
#define SAMPLER_HH

#include "random.hh"
#include <functional>
#include <boost/mpl/if.hpp>

namespace graph_tool
{
using namespace std;
using namespace boost;

// Discrete sampling via vose's alias method.

// See http://www.keithschwarz.com/darts-dice-coins/ for a very clear
// explanation.

template <class Value, class KeepReference = mpl::true_>
class Sampler
{
public:
    Sampler(const vector<Value>& items,
            const vector<double>& probs)
        : _items(items), _probs(probs), _alias(items.size()),
          _S(0)
    {
        for (size_t i = 0; i < _probs.size(); ++i)
            _S += _probs[i];

        vector<size_t> small;
        vector<size_t> large;

        for (size_t i = 0; i < _probs.size(); ++i)
        {
            _probs[i] *= _probs.size() / _S;
            if (_probs[i] < 1)
                small.push_back(i);
            else
                large.push_back(i);
        }

        while (!(small.empty() || large.empty()))
        {
            size_t l = small.back();
            size_t g = large.back();
            small.pop_back();
            large.pop_back();

            _alias[l] = g;
            _probs[g] = (_probs[l] + _probs[g]) - 1;
            if (_probs[g] < 1)
                small.push_back(g);
            else
                large.push_back(g);
        }

        // fix numerical instability
        for (size_t i = 0; i < large.size(); ++i)
            _probs[large[i]] = 1;
        for (size_t i = 0; i < small.size(); ++i)
            _probs[small[i]] = 1;

        _sample = uniform_int_distribution<size_t>(0, _probs.size() - 1);
    }

    Sampler() {}

    template <class RNG>
    const Value& sample(RNG& rng)
    {
        size_t i = _sample(rng);
        bernoulli_distribution coin(_probs[i]);
        if (coin(rng))
            return _items[i];
        else
            return _items[_alias[i]];
    }

    size_t size() const { return _items.size(); }
    bool empty() const { return _items.empty(); }
    double prob_sum() const { return _S; }

    const Value& operator[](size_t i) const
    {
        return _items[i];
    }

    const auto& items() const
    {
        return _items;
    }

    auto begin() const
    {
        return _items.begin();
    }

    auto end() const
    {
        return _items.end();
    }

private:

    typedef typename mpl::if_<KeepReference,
                              const vector<Value>&,
                              vector<Value> >::type items_t;
    items_t _items;
    vector<double> _probs;
    vector<size_t> _alias;
    uniform_int_distribution<size_t> _sample;
    double _S;
};

// uniform sampling from containers

template <class Iter, class RNG>
auto& uniform_sample(Iter begin, const Iter& end, RNG& rng)
{
    auto N = end - begin;
    std::uniform_int_distribution<size_t> i_rand(0, N - 1);
    std::advance(begin, i_rand(rng));
    return *begin;
}

template <class Container, class RNG>
auto& uniform_sample(Container& v, RNG& rng)
{
    return uniform_sample(v.begin(), v.end(), rng);
}

} // namespace graph_tool

#endif // SAMPLER_HH

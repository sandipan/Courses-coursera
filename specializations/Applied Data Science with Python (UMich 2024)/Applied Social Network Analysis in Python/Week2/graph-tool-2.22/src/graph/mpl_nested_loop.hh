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

#ifndef NESTED_FOR_LOOP_HH
#define NESTED_FOR_LOOP_HH

#include <boost/mpl/for_each.hpp>
#include <boost/mpl/vector.hpp>
#include <boost/mpl/empty.hpp>
#include <boost/any.hpp>

namespace boost
{
namespace mpl
{
// The following is a implementation of a nested for_each loop, which runs a
// given Action functor for each combination of its arguments, given by the type
// ranges, as such:
//
//     struct foo
//     {
//         template<class T1, class T2, class T3>
//         void operator()(T1, T2, T3) const
//         {
//             ...
//         }
//     };
//
//     ...
//
//     typedef mpl::vector<int,float,long> r1;
//     typedef mpl::vector<string,double> r2;
//     typedef mpl::vector<size_t,char> r3;
//
//     any x = float(2);
//     any y = string("foo");
//     any z = size_t(42);
//
//     bool found = nested_for_each<r1,r2,r3>(foo(), x, y, z);
//
// The code above will run iterate through all combinations of foo::operator(T1,
// T2, T3) and call the one that corresponds to the actual types stored in x, y,
// and z. If the types are not found during iteration, we have found == true,
// otherwise found == false. This provides a more general compile-time to
// run-time bridge than the simpler mpl::for_each().


struct stop_iteration: public std::exception {};

// this is a functor wrapper that will perform an any_cast<> in each in an array
// of arguments according to the called types. If the cast is successful, the
// function will be called with those types, and stop_iteration will be thrown.
template <class Action, std::size_t N>
struct all_any_cast
{
    all_any_cast(Action a, std::array<any*, N>& args)
        : _a(a), _args(args) {}

    template <class... Ts>
    __attribute__((always_inline))
    void operator()(Ts*... vs) const
    {
        dispatch(std::make_index_sequence<sizeof...(Ts)>(), vs...);
    }

    struct fail_cast {};

    template <class T>
    T& try_any_cast(boost::any& a) const
    {
        try
        {
            return any_cast<T&>(a);
        }
        catch (bad_any_cast&)
        {
            try
            {
                return any_cast<std::reference_wrapper<T>>(a);
            }
            catch (bad_any_cast&)
            {
                throw fail_cast();
            }
        }
    }

    template <std::size_t... Idx, class... Ts>
    __attribute__((always_inline))
    void dispatch(std::index_sequence<Idx...>, Ts*...) const
    {
        try
        {
            static_assert(sizeof...(Idx) == N,
                          "all_any_cast: wrong number of arguments");
            _a(try_any_cast<Ts>(*_args[Idx])...);
            throw stop_iteration();
        }
        catch (fail_cast) {}
    }

    Action _a;
    std::array<any*, N>& _args;
};

// recursion-free variadic version of for_each
template <class...>
struct for_each_variadic;

template <class F, class... Ts>
struct for_each_variadic<F,std::tuple<Ts...>>
{
    void operator()(F f)
    {
        auto call = [&](auto&& arg){f(std::forward<decltype(arg)>(arg)); return 0;};
        (void) std::initializer_list<int> {call(typename std::add_pointer<Ts>::type())...};
    }
};

// convert mpl sequence to std::tuple
template <class T, class R>
struct to_tuple_imp;

template <class... Ts, class X>
struct to_tuple_imp<std::tuple<Ts...>, X>
{
    typedef std::tuple<Ts..., X> type;
};

template <class Seq>
struct to_tuple
{
    typedef typename mpl::fold<Seq, std::tuple<>,
                               to_tuple_imp<mpl::_1, mpl::_2>>::type type;
};

// nested type loops via variadic templates

template <class...>
struct inner_loop {};

template <class Action, class... Ts>
struct inner_loop<Action, std::tuple<Ts...>>
{
    inner_loop(Action a): _a(a) {}

    template <class T>
    __attribute__((always_inline))
    void operator()(T*) const
    { _a(typename std::add_pointer<Ts>::type()...,
         typename std::add_pointer<T>::type()); }  // innermost loop
    Action _a;
};

template <class Action, class... Ts, class TR1, class... TRS>
struct inner_loop<Action, std::tuple<Ts...>, TR1, TRS...>
{
    inner_loop(Action a): _a(a) {}

    template <class T>
    __attribute__((always_inline))
    void operator()(T*) const
    {
        typedef inner_loop<Action, std::tuple<Ts..., T>, TRS...> inner_loop_t;
        typedef typename to_tuple<TR1>::type tr_tuple;
        for_each_variadic<inner_loop_t, tr_tuple>()(inner_loop_t(_a));
    }
    Action _a;
};

// final function

template <class TR1, class... TRS, class Action, class... Args>
bool nested_for_each(Action a, Args&&... args)
{
    std::array<any*, sizeof...(args)> as{{&args...}};
    auto b = all_any_cast<Action, sizeof...(args)>(a, as);
    try
    {
        typedef decltype(b) action_t;
        typedef typename to_tuple<TR1>::type tr_tuple;
        typedef inner_loop<action_t, std::tuple<>, TRS...> inner_loop_t;
        for_each_variadic<inner_loop_t, tr_tuple>()(inner_loop_t(b));
        return false;
    }
    catch (stop_iteration&)
    {
        return true;
    }
}

template <class TR1, class... TRS, class Action>
void nested_for_each(Action a)
{
    try
    {
        typedef typename to_tuple<TR1>::type tr_tuple;
        typedef inner_loop<Action, std::tuple<>, TRS...> inner_loop_t;
        for_each_variadic<inner_loop_t, tr_tuple>()(inner_loop_t(a));
    }
    catch (stop_iteration&) {}
}


} // mpl namespace
} // boost namespace

#endif //NESTED_FOR_LOOP_HH

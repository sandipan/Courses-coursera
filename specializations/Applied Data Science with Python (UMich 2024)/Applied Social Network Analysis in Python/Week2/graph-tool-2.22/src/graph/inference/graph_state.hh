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

#ifndef GRAPH_STATE_HH
#define GRAPH_STATE_HH

#include <boost/python.hpp>
#include <boost/preprocessor/comparison/equal.hpp>
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/seq/size.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <boost/preprocessor/seq/for_each_i.hpp>
#include <boost/preprocessor/stringize.hpp>
#include <boost/preprocessor/tuple/elem.hpp>
#include <boost/preprocessor/control/if.hpp>
#include <boost/preprocessor/arithmetic/dec.hpp>
#include <boost/preprocessor/seq/transform.hpp>
#include <boost/preprocessor/seq/filter.hpp>
#include <boost/preprocessor/comparison/equal.hpp>
#include <boost/preprocessor/comparison/not_equal.hpp>
#include <boost/preprocessor/punctuation/comma.hpp>
#include <boost/preprocessor/facilities/empty.hpp>
#include <boost/preprocessor/seq/first_n.hpp>

#include "graph.hh"
#include "graph_selectors.hh"
#include "graph_properties.hh"
#include "graph_filtering.hh"
#include "graph_util.hh"

#include "numpy_bind.hh"

#include "config.h"

namespace graph_tool
{
using namespace boost;

template <size_t N>
struct nth
{
    template <class T, class... Ts>
    auto&& operator()(T&&, Ts&&... as) const
    {
        static_assert(N < sizeof...(as) + 1, "wrong number of arguments");
        return nth<N-1>()(std::forward<Ts>(as)...);
    }
};

template <>
struct nth<0>
{
    template <class T, class... Ts>
    auto&& operator()(T&& a, Ts&&...) const
    {
        return a;
    }
};

template <size_t N, class T, class... Ts>
struct nth_t
{
    typedef typename std::conditional<N == 0,
                                      T,
                                      typename nth_t<N-1, Ts...>::type>::type
        type;
};

template <size_t N, class T>
struct nth_t<N, T>
{
    typedef T type;
};

template <template <class...> class State>
struct StateFactory
{
    template <class... Ts>
    struct apply
    {
        typedef State<Ts...> type;
    };
};


template <class Type, class Index>
auto uncheck(boost::checked_vector_property_map<Type,Index>*)
{
    boost::unchecked_vector_property_map<Type,Index>* na(nullptr);
    return na;
}

template <class Type, class Index>
auto uncheck(boost::checked_vector_property_map<Type,Index> p)
{
    return p.get_unchecked();
}

template <class T>
auto&& uncheck(T&& a)
{
    return a;
}


template <class Factory, class... TRS>
struct StateWrap
{
    template <class... Ts>
    struct FactoryWrap
    {
        typedef typename Factory::template apply
            <typename std::remove_reference<Ts>::type...>::type
            type;

        template <class... ATs>
        auto operator()(ATs&&... args) const
        {
            return type(std::forward<ATs>(args)...);
        };
    };

    template <class... TS, class F>
    static void dispatch(F&& f)
    {
        auto full_dispatch = [&](auto*... full_args)
            {
                typedef typename FactoryWrap
                    <typename std::remove_reference
                       <decltype(*full_args)>::type...>::type
                    state_t;
                state_t* ptr(nullptr);
                f(ptr);
            };
        auto partial_dispatch = [&](auto*... args)
            {
                full_dispatch(args...,
                              uncheck((typename std::add_pointer<TS>::type)(nullptr))...);
            };
        mpl::nested_for_each<TRS...>
            ([&](auto*... args){partial_dispatch(uncheck(args)...);});
    }

    template <class... TS, class F>
    static void dispatch(python::object& ostate, F&& f,
                         bool throw_not_found = true)
    {
        bool found = false;
        dispatch<TS...>
            ([&](auto* s)
             {
                 typedef typename std::remove_reference<decltype(*s)>::type
                     state_t;
                 python::extract<state_t&> get_state(ostate);
                 if (get_state.check())
                 {
                     state_t& state = get_state();
                     f(state);
                     found = true;
                 }
             });

        if (!found && throw_not_found)
            throw GraphException("dispatch not found for: " +
                                 name_demangle(typeid(StateWrap).name()));
    }


    template <class... Ts>
    struct make_dispatch
    {
        template <size_t N, size_t... Idx, size_t... FIdx, class... Extra,
                  class F>
        void operator()(python::object& ostate,
                        std::array<const char*, N>& names,
                        std::index_sequence<Idx...>,
                        std::index_sequence<FIdx...>,
                        F&& f, Extra&&... extra) const
        {
            static_assert(sizeof...(TRS)  == sizeof...(Idx),
                          "wrong number of argument names");
            static_assert(sizeof...(TRS) + sizeof...(FIdx) == N,
                          "wrong total number of argument names");

            auto full_f = [&](auto&&... full_args)
                {
                    auto state = FactoryWrap<decltype(full_args)...>()
                       (std::forward<Extra>(extra)...,
                        std::forward<decltype(full_args)>(full_args)...);
                    f(state);
                };
            auto partial_f = [&](auto&&... args)
                {
                    full_f(std::forward<decltype(args)>(args)...,
                           uncheck(Extract<Ts>()
                                   (ostate,
                                    names[FIdx + sizeof...(Idx)]))...);
                };
            gt_dispatch<>()(partial_f, TRS()...)
                (get_any(ostate, names[Idx], TRS())...);
        }

        template <class T>
        struct Extract
        {
            T operator()(python::object mobj, std::string name) const
            {
                python::object obj = mobj.attr(name.c_str());
                python::extract<T> extract(obj);
                if (extract.check())
                {
                    T val = extract();
                    return val;
                }
                else
                {
                    python::object aobj;
                    if (PyObject_HasAttrString(obj.ptr(), "_get_any"))
                        aobj = obj.attr("_get_any")();
                    else
                        aobj = obj;
                    python::extract<boost::any&> extract(aobj);
                    try
                    {
                        if (!extract.check())
                            throw boost::bad_any_cast();
                        boost::any& aval = extract();
                        T val = any_cast<T>(aval);
                        return val;
                    }
                    catch (boost::bad_any_cast)
                    {
                        try
                        {
                            typedef std::reference_wrapper
                                <typename std::remove_reference<T>::type>
                                ref_wrap_t;
                            boost::any& aval = extract();
                            auto val = any_cast<ref_wrap_t>(aval);
                            return val.get();
                        }
                        catch (boost::bad_any_cast)
                        {
                            throw ValueException("Cannot extract parameter '" + name +
                                                 "' of desired type: " +
                                                 name_demangle(typeid(T).name()));
                        }
                    }
                }
            }
        };

        template <class Type, size_t Dim>
        struct Extract<multi_array_ref<Type, Dim>>
        {
            multi_array_ref<Type, Dim> operator()(python::object mobj,
                                                  std::string name) const
            {
                python::object obj = mobj.attr(name.c_str());
                try
                {
                    return get_array<Type, Dim>(obj);
                }
                catch (InvalidNumpyConversion& e)
                {
                    throw ValueException("Cannot extract parameter '" + name +
                                         "' of desired type: " +
                                         name_demangle(typeid(multi_array_ref<Type, Dim>).name())
                                         + ", reason: " +
                                         std::string(e.what()));
                }
            }
        };
    };


    template <class TR>
    static boost::any get_any(python::object mobj, std::string name, TR)
    {
        python::object obj = mobj.attr(name.c_str());
        if (PyObject_HasAttrString(obj.ptr(), "_get_any"))
        {
            return python::extract<boost::any&>(obj.attr("_get_any")())();
        }
        else
        {
            boost::any ret;
            bool found = false;
            mpl::nested_for_each<TR>
                ([&](auto* t)
                 {
                     typedef typename std::remove_reference<decltype(*t)>::type
                         val_t;
                     if (std::is_same<val_t, python::object>::value)
                     {
                         ret = obj;
                         found = true;
                     }
                     else if (std::is_same<val_t, std::true_type>::value ||
                              std::is_same<val_t, std::false_type>::value)
                     {
                         python::extract<bool> extract(obj);
                         if (extract.check())
                         {
                             bool val = extract();
                             if (val == std::is_same<val_t, std::true_type>::value)
                             {
                                 ret = typename std::is_same<val_t,
                                                             std::true_type>::type();
                                 found = true;
                             }
                         }
                     }
                     else
                     {
                         python::extract<val_t> extract(obj);
                         if (extract.check())
                         {
                             val_t val = extract();
                             ret = val;
                             found = true;
                         }
                     }
                 });
            if (!found)
                throw ValueException("Cannot extract parameter '" + name +
                                     "' of desired types: " +
                                     name_demangle(typeid(TR).name()));
            return ret;
        }
    }
};

#define _COMMA_CAT(r, data, pos, name) name,
#define GET_COMMA_LIST(seq)                                                    \
    BOOST_PP_SEQ_FOR_EACH_I                                                    \
        (_COMMA_CAT,,BOOST_PP_SEQ_FIRST_N(BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(seq)),\
                                          seq))                                \
        BOOST_PP_SEQ_ELEM(BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(seq)), seq)

#define _PARAM_TYPEDEF(r, pack, pos, name)                                     \
    typedef typename nth_t<pos, pack...>::type                                 \
    BOOST_PP_CAT(BOOST_PP_TUPLE_ELEM(4, 0, name), _t);
#define GET_PARAMS_TYPEDEF(pack, names)                                        \
    BOOST_PP_SEQ_FOR_EACH_I(_PARAM_TYPEDEF, pack, names)

#define _PARAM_USING(r, base, pos, name)                                       \
    using base :: BOOST_PP_CAT(_,BOOST_PP_TUPLE_ELEM(4, 0, name));
#define GET_PARAMS_USING(base, names)                                          \
    BOOST_PP_SEQ_FOR_EACH_I(_PARAM_USING, base, names)

#define _PARAM_DEFINE(r, pack, pos, name)                                      \
    BOOST_PP_CAT(BOOST_PP_TUPLE_ELEM(4, 0, name), _t)                          \
    BOOST_PP_TUPLE_ELEM(2, 1, name)                                            \
    BOOST_PP_CAT(_, BOOST_PP_TUPLE_ELEM(4, 0, name));
#define GET_PARAMS_DEFINE(names)                                               \
    BOOST_PP_SEQ_FOR_EACH_I(_PARAM_DEFINE, r, names)

#define _PARAM_INIT(r, pack, pos, name)                                        \
    BOOST_PP_CAT(_, BOOST_PP_TUPLE_ELEM(4, 0, name))(nth<pos>()(pack...)),
#define GET_PARAMS_INIT(pack, names)                                           \
    BOOST_PP_SEQ_FOR_EACH_I                                                    \
       (_PARAM_INIT, pack,                                                     \
        BOOST_PP_SEQ_FIRST_N(BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(names)),           \
                             names))                                           \
   BOOST_PP_CAT(_, BOOST_PP_TUPLE_ELEM                                         \
                (4, 0,                                                         \
                 BOOST_PP_SEQ_ELEM(BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(names)),     \
                                   names)))                                    \
        (nth<BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(names))>()(pack...))

#define _PARAM_STRING(r, data, pos, name)                                      \
    BOOST_PP_STRINGIZE(BOOST_PP_TUPLE_ELEM(4, 0, name)),
#define GET_PARAMS_NAMES(names)                                                \
    BOOST_PP_SEQ_FOR_EACH_I                                                    \
       (_PARAM_STRING,,                                                        \
        BOOST_PP_SEQ_FIRST_N(BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(names)),           \
                             names))                                           \
    BOOST_PP_STRINGIZE                                                         \
       (BOOST_PP_TUPLE_ELEM                                                    \
        (4, 0, BOOST_PP_SEQ_ELEM(BOOST_PP_DEC(BOOST_PP_SEQ_SIZE(names)),       \
                                 names)))


#define GEN_STATE_BASE(base_name, state_params)                                \
    template <class... Ts>                                                     \
    class base_name                                                            \
    {                                                                          \
    public:                                                                    \
        GET_PARAMS_TYPEDEF(Ts, state_params)                                   \
        template <class... ATs,                                                \
                  typename std::enable_if_t                                    \
                      <!std::is_same<typename nth_t<0, ATs...>::type,          \
                                     base_name<Ts...>>::value>* = nullptr>     \
        base_name(ATs&&... args) : GET_PARAMS_INIT(args, state_params) {}      \
        base_name(const base_name<Ts...>&) = default;                          \
    protected:                                                                 \
        GET_PARAMS_DEFINE(state_params)                                        \
    };



#define _GET_T(r, data, elem) BOOST_PP_TUPLE_ELEM(4, 2, elem)
#define _IS_TR(s, data, elem) BOOST_PP_EQUAL(BOOST_PP_TUPLE_ELEM(4, 3, elem),1)
#define GET_PARAMS_TRS(params)                                                 \
    BOOST_PP_SEQ_TRANSFORM(_GET_T,,BOOST_PP_SEQ_FILTER(_IS_TR,,params))

#define IS_TYPE(s, data, elem) BOOST_PP_EQUAL(BOOST_PP_TUPLE_ELEM(4, 3, elem),0)
#define GET_PARAMS_TYPES(params)                                               \
    BOOST_PP_SEQ_TRANSFORM(_GET_T,,BOOST_PP_SEQ_FILTER(IS_TYPE,,params))

#define GEN_DISPATCH(gen_name, state_name, params)                             \
    struct gen_name                                                            \
    {                                                                          \
        typedef StateWrap<StateFactory<state_name>,                            \
                          GET_COMMA_LIST(GET_PARAMS_TRS(params))>              \
            state_wrap_t;                                                      \
        template <class F, class... Extra>                                     \
        static void make_dispatch(python::object ostate, F&& f,                \
                                  Extra&&... args)                             \
        {                                                                      \
            std::array<const char*, BOOST_PP_SEQ_SIZE(params)> names =         \
                {{GET_PARAMS_NAMES(params)}};                                  \
            typedef typename state_wrap_t::template make_dispatch              \
                <GET_COMMA_LIST(GET_PARAMS_TYPES(params))> dispatch_t;         \
            dispatch_t()                                                       \
                (ostate, names,                                                \
                 std::make_index_sequence                                      \
                     <BOOST_PP_SEQ_SIZE(GET_PARAMS_TRS(params))>(),            \
                 std::make_index_sequence                                      \
                     <BOOST_PP_SEQ_SIZE(GET_PARAMS_TYPES(params))>(),          \
                 std::forward<F>(f), std::forward<Extra>(args)...);            \
        }                                                                      \
        template <class F>                                                     \
        static void dispatch(F&& f)                                            \
        {                                                                      \
            state_wrap_t::template dispatch                                    \
                <GET_COMMA_LIST(GET_PARAMS_TYPES(params))>(std::forward<F>(f));\
        }                                                                      \
        template <class F>                                                     \
        static void dispatch(python::object state, F&& f,                      \
                             bool throw_not_found = true)                      \
        {                                                                      \
            state_wrap_t::template dispatch                                    \
                <GET_COMMA_LIST(GET_PARAMS_TYPES(params))>(state,              \
                                                           std::forward<F>(f), \
                                                           throw_not_found);   \
        }                                                                      \
    };

} // namespace graph_tool

#endif // GRAPH_STATE_HH

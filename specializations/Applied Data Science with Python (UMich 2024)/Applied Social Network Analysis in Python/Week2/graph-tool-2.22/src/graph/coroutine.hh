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

#ifndef COROUTINE_HH
#define COROUTINE_HH

#include "config.h"

#include <boost/version.hpp>

#ifdef HAVE_BOOST_COROUTINE
#    if (BOOST_VERSION >= 106200)
#        include <atomic>
#        include <boost/coroutine2/all.hpp>
         namespace graph_tool
         {
             namespace coroutines = boost::coroutines2;
         }
#    else
#        include <boost/coroutine/all.hpp>
         namespace graph_tool
         {
             namespace coroutines = boost::coroutines;
         }
#    endif
#endif // HAVE_BOOST_COROUTINE

#endif // COROUTINE_HH

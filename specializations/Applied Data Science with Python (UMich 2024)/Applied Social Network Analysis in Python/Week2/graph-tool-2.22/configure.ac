dnl Process this file with autoconf to produce a configure script.

dnl graph-tool package version number
m4_define(graph_tool_version_major, 2)
m4_define(graph_tool_version_minor, 22)

AC_INIT([graph-tool],
        [graph_tool_version_major().graph_tool_version_minor()],
        [http://graph-tool.skewed.de/issues],
        [graph-tool],
        [http://graph-tool.skewed.de])

GRAPH_TOOL_VERSION_MAJOR=graph_tool_version_major()
GRAPH_TOOL_VERSION_MINOR=graph_tool_version_minor()
AC_SUBST(GRAPH_TOOL_VERSION_MAJOR)
AC_SUBST(GRAPH_TOOL_VERSION_MINOR)

AC_CANONICAL_TARGET
AC_CONFIG_SRCDIR(src)
AM_INIT_AUTOMAKE([foreign])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])
AM_PROG_CC_C_O
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])

AC_SEARCH_LIBS([strerror],[cposix])
AC_SUBST(CXXFLAGS,$CXXFLAGS)
AC_USE_SYSTEM_EXTENSIONS
AC_PROG_CXX
AC_LANG([C++])
AC_PROG_CC_STDC
AC_HEADER_STDC
AC_DISABLE_STATIC
AC_PROG_INSTALL
LT_INIT

# pkg-config generation
PKG_PROG_PKG_CONFIG
PKG_INSTALLDIR

AX_CXX_COMPILE_STDCXX_14([ext],[mandatory])

dnl turn on warnings
[CXXFLAGS="-Wall -Wextra -ftemplate-backtrace-limit=0 ${CXXFLAGS}"]

dnl Checks for options

dnl Turn debugging on or off
AC_MSG_CHECKING(whether to enable debug info)

AC_ARG_ENABLE([debug],
              [AS_HELP_STRING([--enable-debug],[compile debug information [default=disabled] ])],
              if test $enableval = yes; then
                  [AC_DEFINE([DEBUG], 1, [compile debug info])]
                  [CXXFLAGS="-g ${CXXFLAGS}"]
                  [AC_MSG_RESULT(yes)]
              else
                  [CPPFLAGS="-DNDEBUG ${CPPFLAGS}"]
                  [AC_MSG_RESULT(no)]
              fi,
              [CPPFLAGS="-DNDEBUG ${CPPFLAGS}"]
              [AC_MSG_RESULT(no)])

dnl set template depth
[CXXFLAGS="-ftemplate-depth-250 ${CXXFLAGS}"]

dnl disable deprecation warning, to silence some harmless BGL-related warnings
[CXXFLAGS="-Wno-deprecated ${CXXFLAGS}"]

dnl set default visibility
[CXXFLAGS="-fvisibility=default -fvisibility-inlines-hidden ${CXXFLAGS}"]

dnl set default optimizations
[CXXFLAGS="-O3 ${CXXFLAGS}"]

dnl OpenMP
AC_DEFINE([OPENMP_MIN_THRESH], 300, [default minimum number of vertices for parallel loops])
AC_MSG_CHECKING(whether to enable parallel algorithms with openmp)
AC_ARG_ENABLE([openmp], [AS_HELP_STRING([--disable-openmp],[disable openmp [default=enabled] ])],
              if test $enableval = yes; then
                  [AC_MSG_RESULT(yes)]
                  [USING_OPENMP=yes]
                  [AX_OPENMP([], [USING_OPENMP=no]
                                 [OPENMP_CXXFLAGS="-Wno-unknown-pragmas"])]
              else
                  [AC_MSG_RESULT(no)]              
                  [USING_OPENMP=no]
                  [OPENMP_CXXFLAGS="-Wno-unknown-pragmas"]
              fi,
              [USING_OPENMP=yes]
              [AX_OPENMP([], [USING_OPENMP=no]
                             [OPENMP_CXXFLAGS="-Wno-unknown-pragmas"])])
if test ${USING_OPENMP} = yes; then
    AC_DEFINE([USING_OPENMP], 1, [using openmp])
    dnl clang is retarded
    if test "$(${CXX} --version | grep clang)x" != "x"; then
        [OPENMP_LDFLAGS="-lomp ${OPENMP_LDFLAGS}"]
    fi
fi
[CXXFLAGS="${OPENMP_CXXFLAGS} ${CXXFLAGS}"]

[USING_CAIRO=yes]
AC_MSG_CHECKING(whether to enable cairo drawing)
AC_ARG_ENABLE([cairo], [AS_HELP_STRING([--disable-cairo],[disable cairo drawing [default=enabled] ])],
              if test $enableval = no; then
                 [USING_CAIRO=no]
                 [AC_MSG_RESULT(no)]
              else
                 [AC_MSG_RESULT(yes)]
              fi,
              [AC_MSG_RESULT(yes)])

dnl Override prefix with default value if not set
if test "x${prefix}" = "xNONE"; then
   prefix=${ac_default_prefix}
fi

dnl Checks for programs.

dnl Checks for libraries.
dnl expat
AX_LIB_EXPAT()
if test "$HAVE_EXPAT" = "no"; then
    AC_MSG_ERROR([expat library not found])
fi

dnl python
AM_PATH_PYTHON([2.7])
AC_SUBST(PYTHON_VERSION)
PYTHON_FULL_VERSION=[`${PYTHON} -c "import sys; print(sys.version.split()[0])"`]
AC_SUBST(PYTHON_FULL_VERSION)
AC_PYTHON_DEVEL([== '${PYTHON_FULL_VERSION}'])

# default directory for submodules
[MOD_DIR="${PYTHON_SITE_PKG}"]
AC_ARG_WITH([python-module-path],
            [AS_HELP_STRING([--with-python-module-path=DIR],
                            [directory where python module will be installed
                             [default=auto-detected]])],
            MOD_DIR=$withval)

[MOD_DIR="${MOD_DIR}/graph_tool"]
AC_SUBST(MOD_DIR)

dnl boost
AX_BOOST_BASE([[1.54.0]])
AX_BOOST_PYTHON
if test "$BOOST_PYTHON_LIB" = ""; then
   AC_MSG_ERROR([No usable boost::python found])
fi
AX_BOOST_IOSTREAMS
if test "$BOOST_IOSTREAMS_LIB" = ""; then
   AC_MSG_ERROR([No usable boost::iostreams found])
fi
AX_BOOST_REGEX
if test "$BOOST_REGEX_LIB" = ""; then
   AC_MSG_ERROR([No usable boost::regex found])
fi
AX_BOOST_COROUTINE
if test "$BOOST_COROUTINE_LIB" = ""; then
   AC_MSG_WARN([No usable boost::coroutine found! Some functionality will be disabled in the library.])
fi
AX_BOOST_GRAPH
if test "$BOOST_GRAPH_LIB" = ""; then
   AC_MSG_ERROR([No usable boost::graph found])
fi

[BOOST_LIBS="${BOOST_IOSTREAMS_LIB} -l${BOOST_PYTHON_LIB} ${BOOST_REGEX_LIB} ${BOOST_COROUTINE_LIB}"]

dnl GNU MP library (needed by CGAL)
AC_CHECK_LIB(gmp, __gmpz_init, ,
             [AC_MSG_ERROR([GNU MP not found (CGAL dependency), see https://gmplib.org/])])
dnl CGAL
AX_LIB_CGAL_CORE([], AC_MSG_ERROR([CGAL library not found.]))
[CGAL_FLAGS="-frounding-math"]
AC_MSG_CHECKING(whether to enable cgal debbuging with valgrind)
AC_ARG_ENABLE([cgal-valgrind], [AS_HELP_STRING([--enable-cgal-valgrind],[enable CGAL valgrind debugging [default=disabled] ])],
              if test $enableval = yes; then
                 [AC_MSG_RESULT(yes)]
                 [CGAL_FLAGS="${CGAL_FLAGS} -DCGAL_DISABLE_ROUNDING_MATH_CHECK=ON"]
              else
                 [AC_MSG_RESULT(no)]    
              fi,
              [AC_MSG_RESULT(no)])
AC_SUBST(CGAL_FLAGS)

dnl Checks for header files.

dnl numpy
AX_PYTHON_MODULE(numpy, fatal)
[NUMPY_DIR=`$PYTHON -c "import numpy; print(numpy.get_include())"`]
AC_ARG_WITH([numpy], [AS_HELP_STRING([--with-numpy=DIR],[directory where numpy is installed
                      [default=auto-detected] ])],
            NUMPY_DIR=$withval)
[NUMPY_CPPFLAGS="-I${NUMPY_DIR}"]

[CPPFLAGS_TEMP="${CPPFLAGS}"]
[CPPFLAGS="${PYTHON_CPPFLAGS} ${NUMPY_CPPFLAGS} ${CPPFLAGS}"]
AC_CHECK_HEADER([numpy/arrayobject.h],
                [],
                [AC_MSG_ERROR([Numpy extension header not found])],
                [[#include "Python.h"]]
                [[#define NO_IMPORT_ARRAY]]
                [[#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION]])
AC_COMPILE_IFELSE([AC_LANG_SOURCE([[#include "Python.h"]]
                                  [[// numpy unique symbol weirdness]]
                                  [[#define NO_IMPORT_ARRAY]]
                                  [[#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION]]
                                  [[#include "numpy/arrayobject.h"]]
                                  [[#if NPY_API_VERSION < 0x00000007]]
                                  [[   #error]]
                                  [[#endif]])],
                  [],
                  [AC_MSG_ERROR([Numpy is too old. Version 1.7 or above is required.])])
[CPPFLAGS="${CPPFLAGS_TEMP}"]

dnl cairo
if test "$USING_CAIRO" = "yes"; then
   PKG_CHECK_MODULES(CAIROMM, [cairomm-1.0], AC_DEFINE([HAVE_CAIROMM], [1],
                     [Cairomm is available]), [])
   AC_SUBST(CAIROMM_CFLAGS)
   AC_SUBST(CAIROMM_LIBS)
   AX_PYTHON_MODULE(cairo)
   PYTHON_VERSION_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
   if test "$PYTHON_VERSION_MAJOR" = "3"; then
      [PYCAIRO_HEADER=pycairo/py3cairo.h]
   else
      [PYCAIRO_HEADER=pycairo/pycairo.h]
   fi
   [CPPFLAGS_TEMP="${CPPFLAGS}"]
   [CPPFLAGS="${CAIROMM_CPPFLAGS} ${CAIROMM_CFLAGS} ${PYTHON_CPPFLAGS} ${CPPFLAGS}"]
   AC_DEFINE_UNQUOTED([PYCAIRO_HEADER], <${PYCAIRO_HEADER}>, [pycairo header file])
   AC_CHECK_HEADER(${PYCAIRO_HEADER},
                   [],
                   [AC_MSG_ERROR([pycairo headers not found])])
   [CPPFLAGS="${CPPFLAGS_TEMP}"]
fi

dnl sparsehash
[SPARSEHASH_PREFIX=sparsehash]
AC_ARG_WITH([sparsehash-prefix], [AS_HELP_STRING([--with-sparsehash-prefix=prefix],
                                                 [include directory prefix for sparsehash
                                                  [default=sparsehash] ])],
            [SPARSEHASH_PREFIX=$withval])

[USING_SPARSEHASH=yes]
AC_MSG_CHECKING(whether to enable sparsehash)
AC_ARG_ENABLE([sparsehash],
              [AS_HELP_STRING([--disable-sparsehash],[disable use of google's sparsehash [default=enabled] ])],
              if test $enableval = no; then
                  [USING_SPARSEHASH=no]
                  [AC_MSG_RESULT(no)]
              else
                  [AC_MSG_RESULT(yes)]
              fi,
              [AC_MSG_RESULT(yes)])

if test "$USING_SPARSEHASH" = "yes"; then
   PKG_CHECK_MODULES(SPARSEHASH, [libsparsehash],
                     AC_DEFINE([HAVE_SPARSEHASH], [1], [Using google's sparsehash]),
                     [AC_MSG_RESULT([not found by pkgconfig, trying default...])])
   AC_SUBST(SPARSEHASH_CFLAGS)
   AC_DEFINE_UNQUOTED([SPARSEHASH_PREFIX], [${SPARSEHASH_PREFIX}],
                      [Sparsehash include prefix])
   AC_DEFINE_UNQUOTED([SPARSEHASH_INCLUDE(f)], [<${SPARSEHASH_PREFIX}/f>],
                      [Sparsehash include macro])
   AC_CHECK_HEADER([${SPARSEHASH_PREFIX}/dense_hash_set], [],
                   [AC_MSG_ERROR([sparsehash headers not found])])
fi

dnl Checks for typedefs, structures, and compiler characteristics.
dnl Checks for library functions.

dnl Checks for Additional stuff.

dnl Set PACKAGE PREFIX
if test "x${prefix}" = "xNONE"; then
   packageprefix=${ac_default_prefix}
else
   packageprefix=${prefix}
fi

dnl Set PACKAGE DATA & DOC DIR
packagedatadir=share/${PACKAGE}
packagedocdir=doc/${PACKAGE}


dnl Subst PACKAGE_DATA_DIR.
NO_PREFIX_PACKAGE_DATA_DIR="${packagedatadir}"
AC_SUBST(NO_PREFIX_PACKAGE_DATA_DIR)
PACKAGE_DATA_DIR="${packageprefix}/${packagedatadir}"
AC_SUBST(PACKAGE_DATA_DIR)

dnl Subst PACKAGE_DOC_DIR.
NO_PREFIX_PACKAGE_DOC_DIR="${packagedocdir}"
AC_SUBST(NO_PREFIX_PACKAGE_DOC_DIR)
PACKAGE_DOC_DIR="${packageprefix}/${packagedocdir}"

if test "x${docdir}" = "xNONE"; then
  PACKAGE_DOC_DIR="${packageprefix}/${packagedocdir}"
else
  PACKAGE_DOC_DIR="${docdir}"
fi
AC_SUBST(PACKAGE_DOC_DIR)

# Allow the pkg-config directory to be set
AC_ARG_WITH(pkgconfigdir,
            AC_HELP_STRING([--with-pkgconfigdir],
            [Use the specified pkgconfig dir (default is libdir/pkgconfig)]),
            [pkgconfigdir=${withval}],
            [pkgconfigdir='${libdir}/pkgconfig'])

AC_SUBST([pkgconfigdir])
AC_MSG_NOTICE([pkgconfig directory is ${pkgconfigdir}])

dnl Subst PYTHON_DIR.
AC_DEFINE_UNQUOTED([INSTALL_PREFIX],"${prefix}", [python prefix])
AC_DEFINE_UNQUOTED([PYTHON_DIR], "${PYTHON_SITE_PKG}", [The directory name for the site-packages subdirectory of the standard Python install tree.])

AC_DEFINE_UNQUOTED([CXXFLAGS],"${CXXFLAGS}", [c++ compilation options])
AC_DEFINE_UNQUOTED([CPPFLAGS],"${CPPFLAGS}", [c++ preprocessor compilation options])
AC_DEFINE_UNQUOTED([LDFLAGS],"${LDFLAGS}", [linker options])

AC_DEFINE_UNQUOTED([PACKAGE_DATA_DIR], "${PACKAGE_DATA_DIR}", [package data dir])
AC_DEFINE_UNQUOTED([PACKAGE_DOC_DIR], "${PACKAGE_DOC_DIR}", [package doc dir])

AC_DEFINE_UNQUOTED([AUTHOR], "Tiago de Paula Peixoto <tiago@skewed.de>", [program author(s)])

AC_DEFINE_UNQUOTED([COPYRIGHT],
    "Copyright (C) 2006-2017 Tiago de Paula Peixoto\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.",
        [copyright info])

# git information
AC_DEFINE([GIT_COMMIT], "esyscmd(git show | head -n 1 | sed 's/commit //' |  grep -o -e '.\{8\}' | head -n 1 |tr -d '\n')", [git HEAD commit hash])
AC_DEFINE([GIT_COMMIT_DATE], "esyscmd(git log -1 | head -n 3 | grep 'Date:' | sed s/'Date:   '// | tr -d '\n')", [git HEAD commit date])

# GCC version
AC_DEFINE([GCC_VERSION], [(__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__)], [GCC version value])

# set automake variables

# global CPP flags
AC_SUBST(CPPFLAGS)

# global CXX flags
AC_SUBST(CXXFLAGS)

# extra CPP flags for submodules
[MOD_CPPFLAGS="-I\$(top_srcdir)/src/boost-workaround -DHAVE_CONFIG_H -I\$(top_srcdir)/src/graph -I\$(top_builddir) ${PYTHON_CPPFLAGS} ${BOOST_CPPFLAGS} ${NUMPY_CPPFLAGS} ${EXPAT_CFLAGS}"]
AC_SUBST(MOD_CPPFLAGS)

# extra LIBADD flags for submodules
[MOD_LIBADD="${PYTHON_LIBS} ${BOOST_LIBS} ${EXPAT_LIBS} ${EXPAT_LDFLAGS} ${OPENMP_LDFLAGS}"]
AC_SUBST(MOD_LIBADD)

# needed for typeinfo objects to work across DSO boundaries.
# see http://gcc.gnu.org/faq.html#dso
[MOD_LDFLAGS="-module -avoid-version -export-dynamic -no-undefined -Wl,-E -Wl,--as-needed"]

# MacOS needs different options
if [[ `echo ${target_os} | grep -c -e "^darwin"` == 1 ]]; then
   [MOD_LDFLAGS="-module -dynamiclib"]
fi

AC_SUBST(MOD_LDFLAGS)

AX_CREATE_PKGCONFIG_INFO([graph-tool-py${PYTHON_VERSION}.pc], [],
                         [${PYTHON_LIBS} -l${BOOST_PYTHON_LIB}],
                         [graph-tool Python library],
                         [-ftemplate-depth-250 ${PYTHON_CPPFLAGS} ${BOOST_CPPFLAGS} ${SPARSEHASH_CFLAGS} ${NUMPY_CPPFLAGS} -I${MOD_DIR}/include -I${MOD_DIR}/include/boost-workaround],
                         [])

AC_CONFIG_FILES([
Makefile
src/Makefile
src/graph/Makefile
src/graph/centrality/Makefile
src/graph/clustering/Makefile
src/graph/correlations/Makefile
src/graph/draw/Makefile
src/graph/flow/Makefile
src/graph/generation/Makefile
src/graph/inference/Makefile
src/graph/layout/Makefile
src/graph/search/Makefile
src/graph/spectral/Makefile
src/graph/stats/Makefile
src/graph/topology/Makefile
src/graph/util/Makefile
src/graph_tool/Makefile
])
AC_OUTPUT

if test ${TERM}x != x -a ${TERM} != dumb; then
    color () {
        tput setaf $1
    }
    reset () {
        tput sgr0
    }
else
    color () {
        :
    }
    reset () {
        :
    }
fi

echo "$(color 2)================================================================================$(reset)"
echo "$(color 2)                             CONFIGURATION SUMMARY                              $(reset)"
echo "$(color 2)================================================================================$(reset)"
echo -e "$(color 3)Using python version:   $(color 4)${PYTHON_FULL_VERSION}$(reset)"
echo -e "$(color 3)Python interpreter:     $(color 4)${PYTHON}$(reset)"
echo -e "$(color 3)Installation path:      $(color 4)${MOD_DIR}$(reset)\n"

echo -e "$(color 3)C++ compiler (CXX):     $(color 4)${CXX}$(reset)"
echo -e "$(color 3)C++ compiler version:   $(color 4)`${CXX} -dumpversion`$(reset)\n"

echo -e "$(color 3)Prefix:                 $(color 4)${prefix}$(reset)"
echo -e "$(color 3)Pkgconfigdir:           $(color 4)${pkgconfigdir}$(reset)\n"

echo -e "$(color 3)Python CPP flags:       $(color 4)${PYTHON_CPPFLAGS}$(reset)"
echo -e "$(color 3)Python LD flags:        $(color 4)${PYTHON_LIBS}$(reset)"
echo -e "$(color 3)Boost CPP flags:        $(color 4)${BOOST_CPPFLAGS}$(reset)"
echo -e "$(color 3)Boost LD flags:         $(color 4)${BOOST_LIBS}$(reset)"
echo -e "$(color 3)Numpy CPP flags:        $(color 4)${NUMPY_CPPFLAGS}$(reset)"
echo -e "$(color 3)Sparsehash CPP flags:   $(color 4)${SPARSEHASH_CFLAGS}$(reset)"
echo -e "$(color 3)CGAL CPP flags:         $(color 4)${CGAL_CPPFLAGS}$(reset)"
echo -e "$(color 3)CGAL LD flags:          $(color 4)${CGAL_LDFLAGS}$(reset)"
echo -e "$(color 3)Expat CPP flags:        $(color 4)${EXPAT_CFLAGS}$(reset)"
echo -e "$(color 3)Expat LD flags:         $(color 4)${EXPAT_LDFLAGS} ${EXPAT_LIBS}$(reset)"
echo -e "$(color 3)Cairomm CPP flags:      $(color 4)${CAIROMM_CFLAGS}$(reset)"
echo -e "$(color 3)Cairomm LD flags:       $(color 4)${CAIROMM_LIBS}$(reset)"
echo -e "$(color 3)OpenMP compiler flags:  $(color 4)${OPENMP_CXXFLAGS}$(reset)"
echo -e "$(color 3)OpenMP LD flags:        $(color 4)${OPENMP_LDFLAGS}$(reset)"
echo -e "$(color 3)Extra CPPFLAGS:         $(color 4)${CPPFLAGS}$(reset)"
echo -e "$(color 3)Extra CXXFLAGS:         $(color 4)${CXXFLAGS}$(reset)"
echo -e "$(color 3)Extra LDFLAGS:          $(color 4)${LDFLAGS}$(reset)\n"
echo -n -e "$(color 3)Using OpenMP:           "
if test ${USING_OPENMP} = yes; then
   echo "$(color 5)yes$(reset)"
else
   echo "$(color 1)no$(reset)"
fi
echo -n -e "$(color 3)Using sparsehash:       "
if test ${USING_SPARSEHASH} = yes; then
   echo "$(color 5)yes$(reset)"
else
   echo "$(color 1)no$(reset)"
fi
echo -n -e "$(color 3)Using cairo:            "
if test ${USING_CAIRO} = yes; then
   echo "$(color 5)yes$(reset)"
else
   echo "$(color 1)no$(reset)"
fi
echo -e "$(color 2)================================================================================$(reset)"


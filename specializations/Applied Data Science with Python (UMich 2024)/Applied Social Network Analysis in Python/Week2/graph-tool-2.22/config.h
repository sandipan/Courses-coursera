/* config.h.  Generated from config.h.in by configure.  */
/* config.h.in.  Generated from configure.ac by autoheader.  */

/* program author(s) */
#define AUTHOR "Tiago de Paula Peixoto <tiago@skewed.de>"

/* copyright info */
#define COPYRIGHT "Copyright (C) 2006-2017 Tiago de Paula Peixoto\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

/* c++ preprocessor compilation options */
#define CPPFLAGS "-DNDEBUG "

/* c++ compilation options */
#define CXXFLAGS "-fopenmp -O3 -fvisibility=default -fvisibility-inlines-hidden -Wno-deprecated -ftemplate-depth-250 -Wall -Wextra -ftemplate-backtrace-limit=0 "

/* compile debug info */
/* #undef DEBUG */

/* GCC version value */
#define GCC_VERSION (__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__)

/* git HEAD commit hash */
#define GIT_COMMIT "44bf2b92"

/* git HEAD commit date */
#define GIT_COMMIT_DATE "Thu Mar 2 23:08:39 2017 +0000"

/* define if the Boost library is available */
#define HAVE_BOOST /**/

/* define if the Boost::Coroutine library is available */
#define HAVE_BOOST_COROUTINE /**/

/* define if the Boost::Graph library is available */
#define HAVE_BOOST_GRAPH /**/

/* define if the Boost::IOStreams library is available */
#define HAVE_BOOST_IOSTREAMS /**/

/* define if the Boost::Python library is available */
#define HAVE_BOOST_PYTHON /**/

/* define if the Boost::Regex library is available */
#define HAVE_BOOST_REGEX /**/

/* Cairomm is available */
#define HAVE_CAIROMM 1

/* Indicates presence of CGAL library */
#define HAVE_CGAL 1

/* define if the compiler supports basic C++14 syntax */
#define HAVE_CXX14 1

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have the `gmp' library (-lgmp). */
#define HAVE_LIBGMP 1

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Define if OpenMP is enabled */
#define HAVE_OPENMP 1

/* If available, contains the Python version number currently in use. */
#define HAVE_PYTHON "3.6"

/* Using google's sparsehash */
#define HAVE_SPARSEHASH 1

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* python prefix */
#define INSTALL_PREFIX "/usr/local"

/* linker options */
#define LDFLAGS ""

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#define LT_OBJDIR ".libs/"

/* default minimum number of vertices for parallel loops */
#define OPENMP_MIN_THRESH 300

/* Name of package */
#define PACKAGE "graph-tool"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "http://graph-tool.skewed.de/issues"

/* package data dir */
#define PACKAGE_DATA_DIR "/usr/local/share/graph-tool"

/* package doc dir */
#define PACKAGE_DOC_DIR "${datarootdir}/doc/${PACKAGE_TARNAME}"

/* Define to the full name of this package. */
#define PACKAGE_NAME "graph-tool"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "graph-tool 2.22"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "graph-tool"

/* Define to the home page for this package. */
#define PACKAGE_URL "http://graph-tool.skewed.de"

/* Define to the version of this package. */
#define PACKAGE_VERSION "2.22"

/* pycairo header file */
#define PYCAIRO_HEADER <pycairo/py3cairo.h>

/* The directory name for the site-packages subdirectory of the standard
   Python install tree. */
#define PYTHON_DIR "/usr/lib/python3.6/site-packages"

/* Sparsehash include macro */
#define SPARSEHASH_INCLUDE(f) <sparsehash/f>

/* Sparsehash include prefix */
#define SPARSEHASH_PREFIX sparsehash

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Enable extensions on AIX 3, Interix.  */
#ifndef _ALL_SOURCE
# define _ALL_SOURCE 1
#endif
/* Enable GNU extensions on systems that have them.  */
#ifndef _GNU_SOURCE
# define _GNU_SOURCE 1
#endif
/* Enable threading extensions on Solaris.  */
#ifndef _POSIX_PTHREAD_SEMANTICS
# define _POSIX_PTHREAD_SEMANTICS 1
#endif
/* Enable extensions on HP NonStop.  */
#ifndef _TANDEM_SOURCE
# define _TANDEM_SOURCE 1
#endif
/* Enable general extensions on Solaris.  */
#ifndef __EXTENSIONS__
# define __EXTENSIONS__ 1
#endif


/* using openmp */
#define USING_OPENMP 1

/* Version number of package */
#define VERSION "2.22"

/* Define to 1 if on MINIX. */
/* #undef _MINIX */

/* Define to 2 if the system does not provide POSIX.1 features except with
   this defined. */
/* #undef _POSIX_1_SOURCE */

/* Define to 1 if you need to in order for `stat' and other things to work. */
/* #undef _POSIX_SOURCE */

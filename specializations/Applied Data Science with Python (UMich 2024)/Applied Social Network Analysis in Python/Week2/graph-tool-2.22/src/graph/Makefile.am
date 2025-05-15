## Process this file with automake to produce Makefile.in

SUBDIRS = centrality clustering correlations draw flow generation inference layout search spectral stats topology util

AM_CPPFLAGS = $(MOD_CPPFLAGS)

AM_CFLAGS = $(AM_CXXFLAGS)

libgraph_tool_coredir = $(MOD_DIR)
libgraph_tool_core_LTLIBRARIES = libgraph_tool_core.la

libgraph_tool_core_la_LIBADD = $(MOD_LIBADD)
libgraph_tool_core_la_LDFLAGS = $(MOD_LDFLAGS)

libgraph_tool_core_la_SOURCES = \
    base64.cc \
    demangle.cc \
    graph.cc \
    graph_exceptions.cc \
    graph_bind.cc \
    graph_copy.cc \
    graph_filtering.cc \
    graph_io.cc \
    graph_openmp.cc \
    graph_properties.cc \
    graph_properties_imp1.cc \
    graph_properties_imp2.cc \
    graph_properties_imp3.cc \
    graph_properties_imp4.cc \
    graph_properties_copy.cc \
    graph_properties_copy_imp1.cc \
    graph_properties_group.cc \
    graph_properties_ungroup.cc \
    graph_properties_map_values.cc \
    graph_properties_map_values_imp1.cc \
    graph_python_interface.cc \
    graph_python_interface_imp1.cc \
    graph_python_interface_export.cc \
    graph_selectors.cc \
    graphml.cpp \
    random.cc \
    read_graphviz_new.cpp

libgraph_tool_core_la_includedir = $(MOD_DIR)/include
libgraph_tool_core_la_include_HEADERS = \
    ../../config.h \
    base64.hh \
    coroutine.hh \
    demangle.hh \
    fast_vector_property_map.hh \
    gml.hh \
    graph.hh \
    graph_adjacency.hh \
    graph_adaptor.hh \
    graph_exceptions.hh \
    graph_filtered.hh \
    graph_filtering.hh \
    graph_io_binary.hh \
    graph_properties.hh \
    graph_properties_copy.hh \
    graph_properties_group.hh \
    graph_properties_map_values.hh \
    graph_python_interface.hh \
    graph_reverse.hh \
    graph_selectors.hh \
    graph_tool.hh \
    graph_util.hh \
    hash_map_wrap.hh \
    histogram.hh \
    mpl_nested_loop.hh \
    numpy_bind.hh \
    random.hh \
    str_repr.hh \
    shared_map.hh \
    transform_iterator.hh

libgraph_tool_core_la_workarounddir = $(MOD_DIR)/include/boost-workaround/boost/graph/
libgraph_tool_core_la_workaround_HEADERS = \
    ../boost-workaround/boost/graph/betweenness_centrality.hpp \
    ../boost-workaround/boost/graph/detail/read_graphviz_new.hpp \
    ../boost-workaround/boost/graph/graphml.hpp \
    ../boost-workaround/boost/graph/graphviz.hpp \
    ../boost-workaround/boost/graph/isomorphism.hpp \
    ../boost-workaround/boost/graph/kamada_kawai_spring_layout.hpp \
    ../boost-workaround/boost/graph/metric_tsp_approx.hpp \
    ../boost-workaround/boost/graph/named_function_params-alt.hpp \
    ../boost-workaround/boost/graph/overloading.hpp \
    ../boost-workaround/boost/graph/push_relabel_max_flow.hpp \
    ../boost-workaround/boost/graph/copy_alt.hpp \
    ../boost-workaround/boost/graph/stoer_wagner_min_cut.hpp


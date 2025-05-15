## Process this file with automake to produce Makefile.in

AM_CPPFLAGS = $(MOD_CPPFLAGS) $(CGAL_CPPFLAGS)

AM_CXXFLAGS = $(CXXFLAGS)

libgraph_tool_generationdir = $(MOD_DIR)/generation

libgraph_tool_generation_LTLIBRARIES = libgraph_tool_generation.la

libgraph_tool_generation_la_includedir = $(MOD_DIR)/include/generation

libgraph_tool_generation_la_LIBADD = $(MOD_LIBADD) $(CGAL_LIBADD) $(CGAL_LDFLAGS)

libgraph_tool_generation_la_LDFLAGS = $(MOD_LDFLAGS)

libgraph_tool_generation_la_SOURCES = \
    graph_community_network.cc \
    graph_community_network_eavg.cc \
    graph_community_network_eavg_imp1.cc \
    graph_community_network_edges.cc \
    graph_community_network_vavg.cc \
    graph_complete.cc \
    graph_generation.cc \
    graph_geometric.cc \
    graph_lattice.cc \
    graph_line_graph.cc \
    graph_predecessor.cc \
    graph_price.cc \
    graph_rewiring.cc \
    graph_sbm.cc \
    graph_triangulation.cc \
    graph_union.cc \
    graph_union_eprop.cc \
    graph_union_vprop.cc


libgraph_tool_generation_la_include_HEADERS = \
    dynamic_sampler.hh \
    graph_community_network.hh \
    graph_complete.hh \
    graph_generation.hh \
    graph_geometric.hh \
    graph_lattice.hh \
    graph_predecessor.hh \
    graph_price.hh \
    graph_rewiring.hh \
    graph_sbm.hh \
    graph_triangulation.hh \
    graph_union.hh \
    sampler.hh

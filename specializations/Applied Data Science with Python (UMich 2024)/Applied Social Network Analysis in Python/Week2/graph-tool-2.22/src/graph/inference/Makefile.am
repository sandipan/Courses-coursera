## Process this file with automake to produce Makefile.in

AM_CPPFLAGS = $(MOD_CPPFLAGS)

AM_CFLAGS = $(AM_CXXFLAGS)

libgraph_tool_inferencedir = $(MOD_DIR)/inference

libgraph_tool_inference_LTLIBRARIES = libgraph_tool_inference.la

libgraph_tool_inference_la_includedir = $(MOD_DIR)/include/inference

libgraph_tool_inference_la_LIBADD = $(MOD_LIBADD)

libgraph_tool_inference_la_LDFLAGS = $(MOD_LDFLAGS)

libgraph_tool_inference_la_SOURCES = \
    cache.cc \
    graph_blockmodel.cc \
    graph_blockmodel_imp.cc \
    graph_blockmodel_imp2.cc \
    graph_blockmodel_em.cc \
    graph_blockmodel_exhaustive.cc \
    graph_blockmodel_gibbs.cc \
    graph_blockmodel_layers.cc \
    graph_blockmodel_layers_imp.cc \
    graph_blockmodel_layers_exhaustive.cc \
    graph_blockmodel_layers_gibbs.cc \
    graph_blockmodel_layers_mcmc.cc \
    graph_blockmodel_layers_merge.cc \
    graph_blockmodel_layers_multicanonical.cc \
    graph_blockmodel_layers_multiflip_mcmc.cc \
    graph_blockmodel_layers_overlap.cc \
    graph_blockmodel_layers_overlap_exhaustive.cc \
    graph_blockmodel_layers_overlap_mcmc.cc \
    graph_blockmodel_layers_overlap_mcmc_bundled.cc \
    graph_blockmodel_layers_overlap_multiflip_mcmc.cc \
    graph_blockmodel_layers_overlap_gibbs.cc \
    graph_blockmodel_layers_overlap_multicanonical.cc \
    graph_blockmodel_layers_overlap_vacate.cc \
    graph_blockmodel_marginals.cc \
    graph_blockmodel_mcmc.cc \
    graph_blockmodel_multicanonical.cc \
    graph_blockmodel_multiflip_mcmc.cc \
    graph_blockmodel_merge.cc \
    graph_blockmodel_overlap.cc \
    graph_blockmodel_overlap_exhaustive.cc \
    graph_blockmodel_overlap_gibbs.cc \
    graph_blockmodel_overlap_mcmc.cc \
    graph_blockmodel_overlap_mcmc_bundled.cc \
    graph_blockmodel_overlap_multicanonical.cc \
    graph_blockmodel_overlap_multiflip_mcmc.cc \
    graph_blockmodel_overlap_vacate.cc \
    graph_modularity.cc \
    graph_inference.cc \
    int_part.cc \
    spence.cc

libgraph_tool_inference_la_include_HEADERS = \
    bundled_vacate_loop.hh \
    cache.hh \
    exhaustive_loop.hh \
    gibbs_loop.hh \
    graph_blockmodel.hh \
    graph_blockmodel_em.hh \
    graph_blockmodel_exhaustive.hh \
    graph_blockmodel_gibbs.hh \
    graph_blockmodel_layers.hh \
    graph_blockmodel_layers_util.hh \
    graph_blockmodel_mcmc.hh \
    graph_blockmodel_merge.hh \
    graph_blockmodel_multicanonical.hh \
    graph_blockmodel_multiflip_mcmc.hh \
    graph_blockmodel_overlap.hh \
    graph_blockmodel_overlap_mcmc_bundled.hh \
    graph_blockmodel_overlap_util.hh \
    graph_blockmodel_overlap_vacate.hh \
    graph_blockmodel_util.hh \
    graph_modularity.hh \
    graph_neighbour_sampler.hh \
    graph_state.hh \
    mcmc_loop.hh \
    merge_loop.hh \
    multicanonical_loop.hh \
    parallel_rng.hh \
    int_part.hh \
    util.hh

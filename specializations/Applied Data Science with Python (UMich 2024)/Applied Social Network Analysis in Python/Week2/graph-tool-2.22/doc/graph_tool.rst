.. automodule:: graph_tool
   :no-members:
   :no-undoc-members:

   .. container:: sec_title

      Basic classes

   .. autoclass:: Graph
    :no-members:
    :no-undoc-members:

    .. automethod:: copy

    .. container:: sec_title

       Iterating over vertices and edges

    See :ref:`sec_iteration` for more documentation and examples.

    Iterator-based interface:

    .. automethod:: vertices
    .. automethod:: edges

    Array-based interface:

    .. automethod:: get_vertices
    .. automethod:: get_edges
    .. automethod:: get_out_edges
    .. automethod:: get_in_edges
    .. automethod:: get_out_neighbours
    .. automethod:: get_in_neighbours
    .. automethod:: get_out_degrees
    .. automethod:: get_in_degrees

    .. container:: sec_title

       Obtaining vertex and edge descriptors

    .. automethod:: vertex
    .. automethod:: edge

    .. container:: sec_title

       Number of vertices and edges

    .. automethod:: num_vertices
    .. automethod:: num_edges

    .. container:: sec_title

       Modifying vertices and edges

    The following functions allow for addition and removal of
    vertices in the graph.

    .. automethod:: add_vertex
    .. automethod:: remove_vertex

    The following functions allow for addition and removal of
    edges in the graph.

    .. automethod:: add_edge
    .. automethod:: remove_edge
    .. automethod:: add_edge_list

    .. automethod:: set_fast_edge_removal
    .. automethod:: get_fast_edge_removal

    The following functions allow for easy removal of vertices and
    edges from the graph.

    .. automethod:: clear
    .. automethod:: clear_vertex
    .. automethod:: clear_edges

    After the removal of many edges and/or vertices, the underlying
    containers may have a capacity that significantly exceeds the size
    of the graph. The function below corrects this.
    
    .. automethod:: shrink_to_fit

    .. container:: sec_title

       Directedness and reversal of edges

    .. note::

       These functions do not actually modify the graph, and are fully
       reversible. They are also very cheap, with an :math:`O(1)`
       complexity.

    .. automethod:: set_directed
    .. automethod:: is_directed

    .. automethod:: set_reversed
    .. automethod:: is_reversed


    .. container:: sec_title

       Creation of new property maps

    .. automethod:: new_property
    .. automethod:: new_vertex_property
    .. automethod:: new_vp
    .. automethod:: new_edge_property
    .. automethod:: new_ep
    .. automethod:: new_graph_property
    .. automethod:: new_gp

    New property maps can be created by copying already existing
    ones.

    .. automethod:: copy_property

    .. automethod:: degree_property_map

    .. container:: sec_title

       Index property maps

    .. autoattribute:: vertex_index
    .. autoattribute:: edge_index
    .. autoattribute:: edge_index_range
    .. automethod:: reindex_edges

    .. container:: sec_title

       Internal property maps

    Internal property maps are just like regular property maps, with
    the only exception that they are saved and loaded to/from files
    together with the graph itself. See :ref:`internal property maps <sec_internal_props>`
    for more details.

    .. note::

       All dictionaries below are mutable. However, any dictionary
       returned below is only an one-way proxy to the internally-kept
       properties. If you modify this object, the change will be
       propagated to the internal dictionary, but not
       vice-versa. Keep this in mind if you intend to keep a copy of
       the returned object.

    .. autoattribute:: properties
    .. autoattribute:: vertex_properties
    .. autoattribute:: vp
    .. autoattribute:: edge_properties
    .. autoattribute:: ep
    .. autoattribute:: graph_properties
    .. autoattribute:: gp
    .. automethod:: list_properties


    .. container:: sec_title

       Filtering of vertices and edges.

    See :ref:`sec_graph_filtering` for more details.

    .. note::

       These functions do not actually modify the graph, and are fully
       reversible. They are also very cheap, and have an :math:`O(1)`
       complexity.

    .. automethod:: set_filters
    .. automethod:: set_vertex_filter
    .. automethod:: get_vertex_filter
    .. automethod:: set_edge_filter
    .. automethod:: get_edge_filter
    .. automethod:: clear_filters

    .. warning::

      The purge functions below irreversibly remove the filtered
      vertices or edges from the graph. Note that, contrary to the
      functions above, these are :math:`O(V)` and :math:`O(E)`
      operations, respectively.

    .. automethod:: purge_vertices
    .. automethod:: purge_edges

    .. container:: sec_title

       I/O operations

    See :ref:`sec_graph_io` for more details.

    .. automethod:: load
    .. automethod:: save


   .. autoclass:: GraphView
       :show-inheritance:
   .. autoclass:: Vertex
   .. autoclass:: Edge
   .. autoclass:: PropertyMap
   .. autoclass:: PropertyArray
       :show-inheritance:
       :no-members:
       :members: prop_map

   .. container:: sec_title

      I/O functions
                 
   .. autofunction:: load_graph
   .. autofunction:: load_graph_from_csv

   .. container:: sec_title

      Property map operations

   .. autofunction:: group_vector_property
   .. autofunction:: ungroup_vector_property
   .. autofunction:: map_property_values
   .. autofunction:: infect_vertex_property
   .. autofunction:: edge_endpoint_property
   .. autofunction:: incident_edges_op
   .. autofunction:: perfect_prop_hash
   .. autofunction:: value_types

   .. container:: sec_title

      OpenMP control

   .. autofunction:: openmp_enabled
   .. autofunction:: openmp_get_num_threads
   .. autofunction:: openmp_set_num_threads
   .. autofunction:: openmp_get_schedule
   .. autofunction:: openmp_set_schedule


   .. container:: sec_title

      Misc

   .. autofunction:: show_config

Available subpackages
=====================

.. toctree::
   :maxdepth: 1

   centrality
   clustering
   collection
   correlations
   draw
   flow
   generation
   inference
   search_module
   spectral
   stats
   topology
   util 
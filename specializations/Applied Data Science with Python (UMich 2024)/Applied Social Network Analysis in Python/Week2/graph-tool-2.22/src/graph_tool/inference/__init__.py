#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# graph_tool -- a general graph manipulation python module
#
# Copyright (C) 2006-2017 Tiago de Paula Peixoto <tiago@skewed.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""``graph_tool.inference`` - Statistical inference of generative network models
-----------------------------------------------------------------------------

This module contains algorithms for the identification of large-scale network
structure via the statistical inference of generative models.

.. note::

   An introduction to the concepts used here, as well as a basic HOWTO is
   included in the cookbook section: :ref:`inference-howto`.

Nonparametric stochastic block model inference
++++++++++++++++++++++++++++++++++++++++++++++

High-level functions
====================

.. autosummary::
   :nosignatures:

   minimize_blockmodel_dl
   minimize_nested_blockmodel_dl

State classes
=============

.. autosummary::
   :nosignatures:

   BlockState
   OverlapBlockState
   LayeredBlockState
   NestedBlockState
   TemperingState

Sampling and minimization
=========================

.. autosummary::
   :nosignatures:

   mcmc_equilibrate
   mcmc_anneal
   mcmc_multilevel
   multicanonical_equilibrate
   MulticanonicalState
   bisection_minimize
   hierarchy_minimize

Auxiliary functions
===================

.. autosummary::
   :nosignatures:

   model_entropy
   mf_entropy
   bethe_entropy
   microstate_entropy
   half_edge_graph
   get_block_edge_gradient

Auxiliary classes
=================

.. autosummary::
   :nosignatures:

   PartitionHist
   BlockPairHist

Semiparametric stochastic block model inference
+++++++++++++++++++++++++++++++++++++++++++++++

State classes
=============

.. autosummary::
   :nosignatures:

   EMBlockState

Expectation-maximization Inference
==================================

.. autosummary::
   :nosignatures:

   em_infer

Large-scale descriptors
+++++++++++++++++++++++

.. autosummary::
   :nosignatures:

   modularity

Contents
++++++++

"""

from __future__ import division, absolute_import, print_function
import sys
if sys.version_info < (3,):
    range = xrange

__all__ = ["minimize_blockmodel_dl",
           "minimize_nested_blockmodel_dl",
           "BlockState",
           "OverlapBlockState",
           "LayeredBlockState",
           "NestedBlockState",
           "mcmc_equilibrate",
           "mcmc_anneal",
           "mcmc_multilevel",
           "TemperingState",
           "multicanonical_equilibrate",
           "MulticanonicalState",
           "bisection_minimize",
           "hierarchy_minimize",
           "EMBlockState",
           "em_infer",
           "model_entropy",
           "mf_entropy",
           "bethe_entropy",
           "microstate_entropy",
           "PartitionHist",
           "BlockPairHist",
           "half_edge_graph",
           "get_block_edge_gradient",
           "get_hierarchy_tree",
           "modularity"]

from . blockmodel import *
from . overlap_blockmodel import *
from . layered_blockmodel import *
from . nested_blockmodel import *
from . mcmc import *
from . bisection import *
from . minimize import *
from . blockmodel_em import *
from . util import *
from . modularity import *

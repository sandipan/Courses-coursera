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

from __future__ import division, absolute_import, print_function
import sys
if sys.version_info < (3,):
    range = xrange

import os.path
import tempfile
if sys.version_info < (3,):
    from urllib2 import urlopen
    import shutil
    class TemporaryDirectory(object):
        def __init__(self, suffix="", prefix="", dir=None):
            self.name = tempfile.mkdtemp(suffix, prefix, dir)

        def __enter__(self):
            return self.name

        def __exit__(self, exc, value, tb):
            shutil.rmtree(self.name)
else:
    from urllib.request import urlopen
    from tempfile import TemporaryDirectory
import tarfile
import warnings
import numpy

from .. import Graph

def load_koblenz_dir(dirname):
    g = Graph()
    g.gp.meta = g.new_graph_property("string")
    g.gp.readme = g.new_graph_property("string")
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if file.startswith("README"):
                g.gp.readme = open(os.path.join(root,file)).read()
            if file.startswith("meta."):
                g.gp.meta = open(os.path.join(root,file)).read()
            if file.startswith("out."):
                edges = numpy.loadtxt(os.path.join(root,file), comments="%")
                line = next(open(os.path.join(root,file)))
                if "asym" not in line:
                    g.set_directed(False)
                edges[:,:2] -= 1  # we need zero-based indexing
                if "bip" in line: # bipartite graphs have non-unique indexing
                    edges[:,1] += edges[:,0].max() + 1
                g.add_edge_list(edges[:,:2])
                if edges.shape[1] > 2:
                    g.ep.weight = g.new_edge_property("double")
                    g.ep.weight.a = edges[:,2]
                if edges.shape[1] > 3:
                    g.ep.time = g.new_edge_property("int")
                    g.ep.time.a = edges[:,3]
        for file in files:
            if file.startswith("ent."):
                try:
                    g.vp.meta = g.new_vertex_property("string")
                    meta = g.vp.meta
                    count = 0
                    for line in open(os.path.join(root,file)):
                        vals = line.split()
                        if len(vals) == 1 and vals[0] == "%":
                            continue
                        if vals[0] == "%":
                            g.gp.meta_desc = g.new_graph_property("string", line)
                            continue
                        v = g.vertex(count)
                        meta[v] = line.strip()
                        count += 1
                except ValueError as e:
                    warnings.warn("error automatically reading node metadata from file '%s': %s" % (file, str(e)))
    return g

def get_koblenz_network_data(name):
    with tempfile.TemporaryFile(mode='w+b') as ftemp:
        response = urlopen('http://konect.uni-koblenz.de/downloads/tsv/%s.tar.bz2' % name)
        buflen = 1 << 20
        while True:
            buf = response.read(buflen)
            ftemp.write(buf)
            if len(buf) < buflen:
                break
        ftemp.seek(0)
        with TemporaryDirectory(suffix=name) as tempdir:
            with tarfile.open(fileobj=ftemp, mode='r:bz2') as tar:
                tar.extractall(path=tempdir)
            g = load_koblenz_dir(tempdir)
            return g

class LazyKoblenzDataDict(dict):
    def __getitem__(self, k):
        if k not in self:
            g = get_koblenz_network_data(k)
            dict.__setitem__(self, k, g)
            return g
        return dict.__getitem__(self, k)


konect_data = LazyKoblenzDataDict()

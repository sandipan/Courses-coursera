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
else:
    unicode = str

import os
import warnings
import numpy

from .. topology import shortest_distance, is_bipartite
from .. import _check_prop_scalar, perfect_prop_hash

try:
    import cairo
except ImportError:
    msg = "Error importing cairo. Graph drawing will not work."
    warnings.warn(msg, RuntimeWarning)
    raise

default_cm = None
try:
    import matplotlib.artist
    import matplotlib.backends.backend_cairo
    import matplotlib.cm
    import matplotlib.colors
    from matplotlib.cbook import flatten
    default_clrs = [(0.5529411764705883, 0.8274509803921568, 0.7803921568627451, 1.0),
                    #(1.0, 1.0, 0.7019607843137254, 1.0),
                    (0.7450980392156863, 0.7294117647058823, 0.8549019607843137, 1.0),
                    (0.984313725490196, 0.5019607843137255, 0.4470588235294118, 1.0),
                    (0.5019607843137255, 0.6941176470588235, 0.8274509803921568, 1.0),
                    (0.9921568627450981, 0.7058823529411765, 0.3843137254901961, 1.0),
                    (0.7019607843137254, 0.8705882352941177, 0.4117647058823529, 1.0),
                    (0.9882352941176471, 0.803921568627451, 0.8980392156862745, 1.0),
                    (0.8509803921568627, 0.8509803921568627, 0.8509803921568627, 1.0),
                    (0.7372549019607844, 0.5019607843137255, 0.7411764705882353, 1.0),
                    (0.8, 0.9215686274509803, 0.7725490196078432, 1.0),
                    (1.0, 0.9294117647058824, 0.43529411764705883, 1.0)]
    default_cm = matplotlib.colors.LinearSegmentedColormap.from_list("Set3",
                                                                     default_clrs)
    is_draw_inline = 'inline' in matplotlib.get_backend()
    color_converter = matplotlib.colors.ColorConverter()
except ImportError:
    msg = "Error importing matplotlib module. Graph drawing will not work."
    warnings.warn(msg, RuntimeWarning)
    raise

try:
    import IPython.display
except ImportError:
    pass

import numpy as np
import gzip
import bz2
import zipfile
import copy
import io
from collections import defaultdict

from .. import Graph, GraphView, PropertyMap, ungroup_vector_property,\
     group_vector_property, _prop, _check_prop_vector, map_property_values

from .. stats import label_parallel_edges, label_self_loops

from .. dl_import import dl_import
dl_import("from . import libgraph_tool_draw")
try:
    from .libgraph_tool_draw import vertex_attrs, edge_attrs, vertex_shape,\
        edge_marker
except ImportError:
    msg = "Error importing cairo-based drawing library. " + \
        "Was graph-tool compiled with cairomm support?"
    warnings.warn(msg, RuntimeWarning)

from .. draw import sfdp_layout, random_layout, _avg_edge_distance, \
    coarse_graphs, radial_tree_layout, prop_to_size

from .. generation import graph_union
from .. topology import shortest_path

_vdefaults = {
    "shape": "circle",
    "color": (0.6, 0.6, 0.6, 0.8),
    "fill_color": (0.6470588235294118, 0.058823529411764705, 0.08235294117647059, 0.8),
    "size": 5,
    "aspect": 1.,
    "rotation": 0.,
    "anchor": 1,
    "pen_width": 0.8,
    "halo": 0,
    "halo_color": [0., 0., 1., 0.5],
    "halo_size": 1.5,
    "text": "",
    "text_color": [0., 0., 0., 1.],
    "text_position": -1.,
    "text_rotation": 0.,
    "text_offset": [0., 0.],
    "font_family": "serif",
    "font_slant": cairo.FONT_SLANT_NORMAL,
    "font_weight": cairo.FONT_WEIGHT_NORMAL,
    "font_size": 12.,
    "surface": None,
    "pie_fractions": [0.75, 0.25],
    "pie_colors": default_clrs # ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    }

_edefaults = {
    "color": (0.1796875, 0.203125, 0.2109375, 0.8),
    "pen_width": 1,
    "start_marker": "none",
    "mid_marker": "none",
    "end_marker": "none",
    "marker_size": 4.,
    "mid_marker_pos": .5,
    "control_points": [],
    "gradient": [],
    "dash_style": [],
    "text": "",
    "text_color": (0., 0., 0., 1.),
    "text_distance": 5,
    "text_parallel": True,
    "font_family": "serif",
    "font_slant": cairo.FONT_SLANT_NORMAL,
    "font_weight": cairo.FONT_WEIGHT_NORMAL,
    "font_size": 12.,
    "sloppy": False,
    "seamless": False
    }

_vtypes = {
    "shape": "int",
    "color": "vector<double>",
    "fill_color": "vector<double>",
    "size": "double",
    "aspect": "double",
    "rotation": "double",
    "anchor": "double",
    "pen_width": "double",
    "halo": "bool",
    "halo_color": "vector<double>",
    "halo_size": "double",
    "text": "string",
    "text_color": "vector<double>",
    "text_position": "double",
    "text_rotation": "double",
    "text_offset": "vector<double>",
    "font_family": "string",
    "font_slant": "int",
    "font_weight": "int",
    "font_size": "float",
    "surface": "object",
    "pie_fractions": "vector<double>",
    "pie_colors": "vector<double>"
    }

_etypes = {
    "color": "vector<double>",
    "pen_width": "double",
    "start_marker": "int",
    "mid_marker": "int",
    "end_marker": "int",
    "marker_size": "double",
    "mid_marker_pos": "double",
    "control_points": "vector<double>",
    "gradient": "vector<double>",
    "dash_style": "vector<double>",
    "text": "string",
    "text_color": "vector<double>",
    "text_distance": "double",
    "text_parallel": "bool",
    "font_family": "string",
    "font_slant": "int",
    "font_weight": "int",
    "font_size": "double",
    "sloppy": "bool",
    "seamless": "bool"
    }

for k in list(_vtypes.keys()):
    _vtypes[getattr(vertex_attrs, k)] = _vtypes[k]

for k in list(_etypes.keys()):
    _etypes[getattr(edge_attrs, k)] = _etypes[k]


def shape_from_prop(shape, enum):
    if isinstance(shape, PropertyMap):
        g = shape.get_graph()
        if shape.key_type() == "v":
            prop = g.new_vertex_property("int")
            descs = g.vertices()
        else:
            descs = g.edges()
            prop = g.new_edge_property("int")
        if shape.value_type() == "string":
            def conv(x):
                return int(getattr(enum, x))
            map_property_values(shape, prop, conv)
        else:
            rg = (min(enum.values.keys()),
                  max(enum.values.keys()))
            g.copy_property(shape, prop)
            if prop.fa.min() < rg[0]:
                prop.fa += rg[0]
            prop.fa -= rg[0]
            prop.fa %= rg[1] - rg[0] + 1
            prop.fa += rg[0]
        return prop
    if isinstance(shape, (str, unicode)):
        return int(getattr(enum, shape))
    else:
        return shape

    raise ValueError("Invalid value for attribute %s: %s" %
                     (repr(enum), repr(shape)))

def open_file(name, mode="r"):
    name = os.path.expanduser(name)
    base, ext = os.path.splitext(name)
    if ext == ".gz":
        out = gzip.GzipFile(name, mode)
        name = base
    elif ext == ".bz2":
        out = bz2.BZ2File(name, mode)
        name = base
    elif ext == ".zip":
        out = zipfile.ZipFile(name, mode)
        name = base
    else:
        out = open(name, mode)
    fmt = os.path.splitext(name)[1].replace(".", "")
    return out, fmt

def get_file_fmt(name):
    name = os.path.expanduser(name)
    base, ext = os.path.splitext(name)
    if ext == ".gz":
        name = base
    elif ext == ".bz2":
        name = base
    elif ext == ".zip":
        name = base
    fmt = os.path.splitext(name)[1].replace(".", "")
    return fmt


def surface_from_prop(surface):
    if isinstance(surface, PropertyMap):
        if surface.key_type() == "v":
            prop = surface.get_graph().new_vertex_property("object")
            descs = surface.get_graph().vertices()
        else:
            descs = surface.get_graph().edges()
            prop = surface.get_graph().new_edge_property("object")
        surface_map = {}
        for v in descs:
            if surface.value_type() == "string":
                if surface[v] not in surface_map:
                    sfc = gen_surface(surface[v])
                    surface_map[surface[v]] = sfc
                prop[v] = surface_map[surface[v]]
            elif surface.value_type() == "python::object":
                if isinstance(surface[v], cairo.Surface):
                    prop[v] = surface[v]
                elif surface[v] is not None:
                    raise ValueError("Invalid value type for surface property: " +
                                     str(type(surface[v])))
            else:
                raise ValueError("Invalid value type for surface property: " +
                                 surface.value_type())
        return prop

    if isinstance(surface, (str, unicode)):
        return gen_surface(surface)
    elif isinstance(surface, cairo.Surface) or surface is None:
        return surface

    raise ValueError("Invalid value for attribute surface: " + repr(surface))

def centered_rotation(g, pos, text_pos=True):
    x, y = ungroup_vector_property(pos, [0, 1])
    cm = (x.fa.mean(), y.fa.mean())
    dx = x.fa - cm[0]
    dy = y.fa - cm[0]
    angle = g.new_vertex_property("double")
    angle.fa = numpy.arctan2(dy, dx)
    pi = numpy.pi
    angle.fa += 2 * pi
    angle.fa %= 2 * pi
    if text_pos:
        idx = (angle.a > pi / 2 ) * (angle.a < 3 * pi / 2)
        tpos = g.new_vertex_property("double")
        angle.a[idx] += pi
        tpos.a[idx] = pi
        return angle, tpos
    return angle

def _convert(attr, val, cmap, pmap_default=False, g=None, k=None):
    if attr == vertex_attrs.shape:
        new_val = shape_from_prop(val, vertex_shape)
        if pmap_default and not isinstance(val, PropertyMap):
            new_val = g.new_vertex_property("int", new_val)
        return new_val
    elif attr == vertex_attrs.surface:
        new_val = surface_from_prop(val)
        if pmap_default and not isinstance(val, PropertyMap):
            new_val = g.new_vertex_property("python::object", new_val)
        return new_val
    elif attr in [edge_attrs.start_marker, edge_attrs.mid_marker,
                  edge_attrs.end_marker]:
        new_val = shape_from_prop(val, edge_marker)
        if pmap_default and not isinstance(val, PropertyMap):
            new_val = g.new_edge_property("int", new_val)
        return new_val
    elif attr in [vertex_attrs.pie_colors]:
        if isinstance(val, PropertyMap):
            if val.value_type() in ["vector<double>", "vector<long double>"]:
                return val
            if val.value_type() in ["vector<int32_t>", "vector<int64_t>", "vector<bool>"]:
                g = val.get_graph()
                new_val = g.new_vertex_property("vector<double>")
                rg = [numpy.inf, -numpy.inf]
                for v in g.vertices():
                    for x in val[v]:
                        rg[0] = min(x, rg[0])
                        rg[1] = max(x, rg[1])
                if rg[0] == rg[1]:
                    rg[1] = 1
                map_property_values(val, new_val,
                                    lambda y: flatten([cmap((x - rg[0]) / (rg[1] - rg[0])) for x in y]))
                return new_val
            if val.value_type() == "vector<string>":
                g = val.get_graph()
                new_val = g.new_vertex_property("vector<double>")
                map_property_values(val, new_val,
                                    lambda y: flatten([color_converter.to_rgba(x) for x in y]))
                return new_val
            if val.value_type() == "python::object":
                try:
                    g = val.get_graph()
                    new_val = g.new_vertex_property("vector<double>")
                    def conv(y):
                        try:
                            new_val[v] = [float(x) for x in flatten(y)]
                        except ValueError:
                            new_val[v] = flatten([color_converter.to_rgba(x) for x in y])
                    map_property_values(val, new_val, conv)
                    return new_val
                except ValueError:
                    pass
        else:
            try:
                new_val = [float(x) for x in flatten(val)]
            except ValueError:
                try:
                    new_val = flatten(color_convert.to_rgba(x) for x in val)
                    new_val = list(new_val)
                except ValueError:
                    pass
            if pmap_default:
                val_a = numpy.zeros((g.num_vertices(), len(new_val)))
                for i in range(len(new_val)):
                    val_a[:, i] = new_val[i]
                return g.new_vertex_property("vector<double>", val_a)
            else:
                return new_val
    elif attr in [vertex_attrs.color, vertex_attrs.fill_color,
                  vertex_attrs.text_color, vertex_attrs.halo_color,
                  edge_attrs.color, edge_attrs.text_color]:
        if isinstance(val, list):
            new_val = val
        elif isinstance(val, (tuple, np.ndarray)):
            new_val = list(val)
        elif isinstance(val, (str, unicode)):
            new_val = list(color_converter.to_rgba(val))
        elif isinstance(val, PropertyMap):
            if val.value_type() in ["vector<double>", "vector<long double>"]:
                new_val = val
            elif val.value_type() in ["int32_t", "int64_t", "double",
                                      "long double", "unsigned long",
                                      "unsigned int", "bool"]:
                g = val.get_graph()
                if val.value_type() in ["int32_t", "int64_t", "unsigned long",
                                        "unsigned int"]:
                    nval = perfect_prop_hash([val])[0]
                else:
                    nval = val
                try:
                    vrange = [nval.fa.min(), nval.fa.max()]
                except (AttributeError, ValueError):
                    #vertex index
                    vrange = [int(g.vertex(0, use_index=False)),
                              int(g.vertex(g.num_vertices() - 1,
                                           use_index=False))]
                cnorm = matplotlib.colors.Normalize(vmin=vrange[0],
                                                    vmax=vrange[1])
                g = val.get_graph()
                if val.key_type() == "v":
                    prop = g.new_vertex_property("vector<double>")
                else:
                    prop = g.new_edge_property("vector<double>")
                map_property_values(nval, prop, lambda x: cmap(cnorm(x)))
                new_val = prop
            elif val.value_type() == "string":
                g = val.get_graph()
                if val.key_type() == "v":
                    prop = g.new_vertex_property("vector<double>")
                else:
                    prop = g.new_edge_property("vector<double>")
                map_property_values(val, prop,
                                    lambda x: color_converter.to_rgba(x))
                new_val = prop
            else:
                raise ValueError("Invalid value for attribute %s: %s" %
                                 (repr(attr), repr(val)))
        if pmap_default and not isinstance(val, PropertyMap):
            if attr in [vertex_attrs.color, vertex_attrs.fill_color,
                        vertex_attrs.text_color, vertex_attrs.halo_color]:
                val_a = numpy.zeros((g.num_vertices(),len(new_val)))
                for i in range(len(new_val)):
                    val_a[:, i] = new_val[i]
                return g.new_vertex_property("vector<double>", val_a)
            else:
                val_a = numpy.zeros((g.num_edges(), len(new_val)))
                for i in range(len(new_val)):
                    val_a[:,i] = new_val[i]
                return g.new_edge_property("vector<double>", val_a)
        else:
            return new_val

    if pmap_default and not isinstance(val, PropertyMap):
        if k == "v":
            new_val = g.new_vertex_property(_vtypes[attr], val=val)
        else:
            new_val = g.new_edge_property(_etypes[attr], val=val)
        return new_val

    return val


def _attrs(attrs, d, g, cmap):
    nattrs = {}
    defaults = {}
    for k, v in attrs.items():
        try:
            if d == "v":
                attr = getattr(vertex_attrs, k)
            else:
                attr = getattr(edge_attrs, k)
        except AttributeError:
            warnings.warn("Unknown attribute: " + str(k), UserWarning)
            continue
        if isinstance(v, PropertyMap):
            nattrs[int(attr)] = _prop(d, g, _convert(attr, v, cmap))
        else:
            defaults[int(attr)] = _convert(attr, v, cmap)
    return nattrs, defaults

def _convert_props(props, d, g, cmap, pmap_default=False):
    nprops = {}
    for k, v in props.items():
        try:
            if d == "v":
                attr = getattr(vertex_attrs, k)
            else:
                attr = getattr(edge_attrs, k)
            nprops[k] = _convert(attr, v, cmap, pmap_default=pmap_default,
                                 g=g, k=d)
        except AttributeError:
            warnings.warn("Unknown attribute: " + str(k), UserWarning)
            continue
    return nprops


def get_attr(attr, d, attrs, defaults):
    if attr in attrs:
        p = attrs[attr]
    else:
        p = defaults[attr]
    if isinstance(p, PropertyMap):
        return p[d]
    else:
        return p


def position_parallel_edges(g, pos, loop_angle=float("nan"),
                            parallel_distance=1):
    lp = label_parallel_edges(GraphView(g, directed=False))
    ll = label_self_loops(g)
    if isinstance(loop_angle, PropertyMap):
        angle = loop_angle
    else:
        angle = g.new_vertex_property("double", float(loop_angle))

    g = GraphView(g, directed=True)
    if ((len(lp.fa) == 0 or lp.fa.max() == 0) and
        (len(ll.fa) == 0 or ll.fa.max() == 0)):
        return []
    else:
        spline = g.new_edge_property("vector<double>")
        libgraph_tool_draw.put_parallel_splines(g._Graph__graph,
                                                _prop("v", g, pos),
                                                _prop("e", g, lp),
                                                _prop("e", g, spline),
                                                _prop("v", g, angle),
                                                parallel_distance)
        return spline


def parse_props(prefix, args):
    props = {}
    others = {}
    for k, v in list(args.items()):
        if v is None:
            continue
        if k.startswith(prefix + "_"):
            props[k.replace(prefix + "_", "")] = v
        else:
            others[k] = v
    return props, others


def cairo_draw(g, pos, cr, vprops=None, eprops=None, vorder=None, eorder=None,
               nodesfirst=False, vcmap=default_cm, ecmap=default_cm,
               loop_angle=numpy.nan, parallel_distance=None, fit_view=False,
               res=0, max_render_time=-1, **kwargs):
    r"""
    Draw a graph to a :mod:`cairo` context.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be drawn.
    pos : :class:`~graph_tool.PropertyMap`
        Vector-valued vertex property map containing the x and y coordinates of
        the vertices.
    cr : :class:`~cairo.Context`
        A :class:`~cairo.Context` instance.
    vprops : dict (optional, default: ``None``)
        Dictionary with the vertex properties. Individual properties may also be
        given via the ``vertex_<prop-name>`` parameters, where ``<prop-name>`` is
        the name of the property.
    eprops : dict (optional, default: ``None``)
        Dictionary with the edge properties. Individual properties may also be
        given via the ``edge_<prop-name>`` parameters, where ``<prop-name>`` is
        the name of the property.
    vorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        If provided, defines the relative order in which the vertices are drawn.
    eorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        If provided, defines the relative order in which the edges are drawn.
    nodesfirst : bool (optional, default: ``False``)
        If ``True``, the vertices are drawn first, otherwise the edges are.
    vcmap : :class:`matplotlib.colors.Colormap` (optional, default: :class:`default_cm`)
        Vertex color map.
    ecmap : :class:`matplotlib.colors.Colormap` (optional, default: :class:`default_cm`)
        Edge color map.
    loop_angle : float or :class:`~graph_tool.PropertyMap` (optional, default: ``nan``)
        Angle used to draw self-loops. If ``nan`` is given, they will be placed
        radially from the center of the layout.
    parallel_distance : float (optional, default: ``None``)
        Distance used between parallel edges. If not provided, it will be
        determined automatically.
    fit_view : bool or float or tuple (optional, default: ``True``)
        If ``True``, the layout will be scaled to fit the entire clip region.
        If a float value is given, it will be interpreted as ``True``, and in
        addition the viewport will be scaled out by that factor. If a tuple
        value is given, it should have four values ``(x, y, w, h)`` that
        specify the view in user coordinates.
    bg_color : str or sequence (optional, default: ``None``)
        Background color. The default is transparent.
    res : float (optional, default: ``0.``):
        If shape sizes fall below this value, simplified drawing is used.
    max_render_time : int (optional, default: ``-1``):
        If nonnegative, this function will return an iterator that will perform
        part of the drawing at each step, so that each iteration takes at most
        ``max_render_time`` milliseconds.
    vertex_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``vertex_<prop-name>`` specify the
        vertex property with name ``<prop-name>``, as an alternative to the
        ``vprops`` parameter.
    edge_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``edge_<prop-name>`` specify the edge
        property with name ``<prop-name>``, as an alternative to the ``eprops``
        parameter.

    Returns
    -------
    iterator :
        If ``max_render_time`` is nonnegative, this will be an iterator that will
        perform part of the drawing at each step, so that each iteration takes
        at most ``max_render_time`` milliseconds.
    """

    if vorder is not None:
        _check_prop_scalar(vorder, name="vorder")

    vprops = {} if vprops is None else copy.copy(vprops)
    eprops = {} if eprops is None else copy.copy(eprops)

    props, kwargs = parse_props("vertex", kwargs)
    vprops.update(props)
    props, kwargs = parse_props("edge", kwargs)
    eprops.update(props)
    for k in kwargs:
        warnings.warn("Unknown parameter: " + k, UserWarning)

    cr.save()
    if fit_view != False:
        extents = cr.clip_extents()
        output_size = (extents[2] - extents[0], extents[3] - extents[1])
        try:
            x, y, w, h = fit_view
            cr.scale(output_size[0] / w, output_size[1] / h)
            cr.translate(-x, -y)
        except TypeError:
            pad = fit_view if fit_view != True else 0.95
            offset, zoom = fit_to_view(g, pos, output_size,
                                       vprops.get("size", _vdefaults["size"]),
                                       vprops.get("pen_width", _vdefaults["pen_width"]),
                                       None, vprops.get("text", None),
                                       vprops.get("font_family",
                                                  _vdefaults["font_family"]),
                                       vprops.get("font_size",
                                                  _vdefaults["font_size"]),
                                       pad, cr)
            cr.translate(offset[0], offset[1])
            if not isinstance(fit_view, bool):
                zoom /= fit_view
            cr.scale(zoom, zoom)

    if "control_points" not in eprops:
        if parallel_distance is None:
            parallel_distance = vprops.get("size", _vdefaults["size"])
            if isinstance(parallel_distance, PropertyMap):
                parallel_distance = parallel_distance.fa.mean()
            parallel_distance /= 1.5
            M = cr.get_matrix()
            scale = transform_scale(M, 1,)
            parallel_distance /= scale
        eprops["control_points"] = position_parallel_edges(g, pos, loop_angle,
                                                           parallel_distance)
    if g.is_directed() and "end_marker" not in eprops:
        eprops["end_marker"] = "arrow"

    if vprops.get("text_position", None) == "centered":
        angle, tpos = centered_rotation(g, pos, text_pos=True)
        vprops["text_position"] = tpos
        vprops["text_rotation"] = angle

    vattrs, vdefaults = _attrs(vprops, "v", g, vcmap)
    eattrs, edefaults = _attrs(eprops, "e", g, ecmap)
    vdefs = _attrs(_vdefaults, "v", g, vcmap)[1]
    vdefs.update(vdefaults)
    edefs = _attrs(_edefaults, "e", g, ecmap)[1]
    edefs.update(edefaults)

    if "control_points" not in eprops:
        if parallel_distance is None:
            parallel_distance = _defaults
        eprops["control_points"] = position_parallel_edges(g, pos, loop_angle,
                                                           parallel_distance)
    generator = libgraph_tool_draw.cairo_draw(g._Graph__graph, _prop("v", g, pos),
                                              _prop("v", g, vorder), _prop("e", g, eorder),
                                              nodesfirst, vattrs, eattrs, vdefs, edefs, res,
                                              max_render_time, cr)
    if max_render_time >= 0:
        def gen():
            for count in generator:
                yield count
            cr.restore()
        return gen()
    else:
        for count in generator:
            pass
        cr.restore()

def color_contrast(color):
    c = np.asarray(color)
    y = c[0] * .299 + c[1] * .587 + c[2] * .114
    if y < .5:
        c[:3] = 1
    else:
        c[:3] = 0
    return c

def auto_colors(g, bg, pos, back):
    if not isinstance(bg, PropertyMap):
        if isinstance(bg, (str, unicode)):
            bg = color_converter.to_rgba(bg)
        bg = g.new_vertex_property("vector<double>", val=bg)
    if not isinstance(pos, PropertyMap):
        if pos == "centered":
            pos = 0
        pos = g.new_vertex_property("double", pos)
    bg_a = bg.get_2d_array(range(4))
    bgc_pos = numpy.zeros((g.num_vertices(), 5))
    for i in range(4):
        bgc_pos[:, i] = bg_a[i, :]
    bgc_pos[:, 4] = pos.fa
    bgc_pos = g.new_vertex_property("vector<double>", bgc_pos)
    def conv(x):
        bgc = x[:4]
        p = x[4]
        if p < 0:
            return color_contrast(bgc)
        else:
            return color_contrast(back)
    c = g.new_vertex_property("vector<double>")
    map_property_values(bgc_pos, c, conv)
    return c

def graph_draw(g, pos=None, vprops=None, eprops=None, vorder=None, eorder=None,
               nodesfirst=False, output_size=(600, 600), fit_view=True,
               inline=is_draw_inline, mplfig=None, output=None, fmt="auto",
               **kwargs):
    r"""Draw a graph to screen or to a file using :mod:`cairo`.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be drawn.
    pos : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        Vector-valued vertex property map containing the x and y coordinates of
        the vertices. If not given, it will be computed using :func:`sfdp_layout`.
    vprops : dict (optional, default: ``None``)
        Dictionary with the vertex properties. Individual properties may also be
        given via the ``vertex_<prop-name>`` parameters, where ``<prop-name>`` is
        the name of the property.
    eprops : dict (optional, default: ``None``)
        Dictionary with the edge properties. Individual properties may also be
        given via the ``edge_<prop-name>`` parameters, where ``<prop-name>`` is
        the name of the property.
    vorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        If provided, defines the relative order in which the vertices are drawn.
    eorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        If provided, defines the relative order in which the edges are drawn.
    nodesfirst : bool (optional, default: ``False``)
        If ``True``, the vertices are drawn first, otherwise the edges are.
    output_size : tuple of scalars (optional, default: ``(600,600)``)
        Size of the drawing canvas. The units will depend on the output format
        (pixels for the screen, points for PDF, etc).
    fit_view : bool, float or tuple (optional, default: ``True``)
        If ``True``, the layout will be scaled to fit the entire clip region.
        If a float value is given, it will be interpreted as ``True``, and in
        addition the viewport will be scaled out by that factor. If a tuple
        value is given, it should have four values ``(x, y, w, h)`` that
        specify the view in user coordinates.
    inline : bool (optional, default: ``False``)
        If ``True`` and an `IPython notebook <http://ipython.org/notebook>`_  is
        being used, an inline version of the drawing will be returned.
    mplfig : :mod:`matplotlib` container object (optional, default: ``None``)
        The ``mplfig`` object needs to have an ``artists`` attribute. This can
        for example be a :class:`matplotlib.figure.Figure` or
        :class:`matplotlib.axes.Axes`. Only the cairo backend is supported; use
        ``switch_backend('cairo')``.
    output : string or file object (optional, default: ``None``)
        Output file name (or object). If not given, the graph will be displayed via
        :func:`interactive_window`.
    fmt : string (default: ``"auto"``)
        Output file format. Possible values are ``"auto"``, ``"ps"``, ``"pdf"``,
        ``"svg"``, and ``"png"``. If the value is ``"auto"``, the format is
        guessed from the ``output`` parameter.
    bg_color : str or sequence (optional, default: ``None``)
        Background color. The default is transparent.
    vertex_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``vertex_<prop-name>`` specify the
        vertex property with name ``<prop-name>``, as an alternative to the
        ``vprops`` parameter.
    edge_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``edge_<prop-name>`` specify the edge
        property with name ``<prop-name>``, as an alternative to the ``eprops``
        parameter.
    **kwargs
        Any extra parameters are passed to :func:`~graph_tool.draw.interactive_window`,
        :class:`~graph_tool.draw.GraphWindow`, :class:`~graph_tool.draw.GraphWidget`
        and :func:`~graph_tool.draw.cairo_draw`.

    Returns
    -------
    pos : :class:`~graph_tool.PropertyMap`
        Vector vertex property map with the x and y coordinates of the vertices.
    selected : :class:`~graph_tool.PropertyMap` (optional, only if ``output is None``)
        Boolean-valued vertex property map marking the vertices which were
        selected interactively.

    Notes
    -----


    .. table:: **List of vertex properties**

        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | Name          | Description                                       | Accepted types         | Default Value                    |
        +===============+===================================================+========================+==================================+
        | shape         | The vertex shape. Can be one of the following     | ``str`` or ``int``     | ``"circle"``                     |
        |               | strings: "circle", "triangle", "square",          |                        |                                  |
        |               | "pentagon", "hexagon", "heptagon", "octagon"      |                        |                                  |
        |               | "double_circle", "double_triangle",               |                        |                                  |
        |               | "double_square", "double_pentagon",               |                        |                                  |
        |               | "double_hexagon", "double_heptagon",              |                        |                                  |
        |               | "double_octagon", "pie", "none".                  |                        |                                  |
        |               | Optionally, this might take a numeric value       |                        |                                  |
        |               | corresponding to position in the list above.      |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | color         | Color used to stroke the lines of the vertex.     | ``str`` or list of     | ``[0., 0., 0., 1]``              |
        |               |                                                   | ``floats``             |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | fill_color    | Color used to fill the interior of the vertex.    | ``str`` or list of     | ``[0.640625, 0, 0, 0.9]``        |
        |               |                                                   | ``floats``             |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | size          | The size of the vertex, in the default units of   | ``float`` or ``int``   | ``5``                            |
        |               | the output format (normally either pixels or      |                        |                                  |
        |               | points).                                          |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | aspect        | The aspect ratio of the vertex.                   | ``float`` or ``int``   | ``1.0``                          |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | rotation      | Angle (in radians) to rotate the vertex.          | ``float``              | ``0.``                           |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | anchor        | Specifies how the edges anchor to the vertices.   |  ``int``               | ``1``                            |
        |               | If `0`, the anchor is at the center of the vertex,|                        |                                  |
        |               | otherwise it is at the border.                    |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | pen_width     | Width of the lines used to draw the vertex, in    | ``float`` or ``int``   | ``0.8``                          |
        |               | the default units of the output format (normally  |                        |                                  |
        |               | either pixels or points).                         |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | halo          | Whether to draw a circular halo around the        | ``bool``               | ``False``                        |
        |               | vertex.                                           |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | halo_color    | Color used to draw the halo.                      | ``str`` or list of     | ``[0., 0., 1., 0.5]``            |
        |               |                                                   | ``floats``             |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | halo_size     | Relative size of the halo.                        | ``float``              | ``1.5``                          |
        |               |                                                   |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | text          | Text to draw together with the vertex.            | ``str``                | ``""``                           |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_color    | Color used to draw the text. If the value is      | ``str`` or list of     | ``"auto"``                       |
        |               | ``"auto"``, it will be computed based on          | ``floats``             |                                  |
        |               | fill_color to maximize contrast.                  |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_position | Position of the text relative to the vertex.      | ``float`` or ``int``   | ``-1``                           |
        |               | If the passed value is positive, it will          |  or ``"centered"``     |                                  |
        |               | correspond to an angle in radians, which will     |                        |                                  |
        |               | determine where the text will be placed outside   |                        |                                  |
        |               | the vertex. If the value is negative, the text    |                        |                                  |
        |               | will be placed inside the vertex. If the value is |                        |                                  |
        |               | ``-1``, the vertex size will be automatically     |                        |                                  |
        |               | increased to accommodate the text. The special    |                        |                                  |
        |               | value ``"centered"`` positions the texts rotated  |                        |                                  |
        |               | radially around the center of mass.               |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_offset   | Text position offset.                             | list of ``float``      | ``[0.0, 0.0]``                   |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_rotation | Angle of rotation (in radians) for the text.      | ``float``              | ``0.0``                          |
        |               | The center of rotation is the position of the     |                        |                                  |
        |               | vertex.                                           |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_family   | Font family used to draw the text.                | ``str``                | ``"serif"``                      |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_slant    | Font slant used to draw the text.                 | ``cairo.FONT_SLANT_*`` | :data:`cairo.FONT_SLANT_NORMAL`  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_weight   | Font weight used to draw the text.                | ``cairo.FONT_WEIGHT_*``| :data:`cairo.FONT_WEIGHT_NORMAL` |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_size     | Font size used to draw the text.                  | ``float`` or ``int``   | ``12``                           |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | surface       | The cairo surface used to draw the vertex. If     | :class:`cairo.Surface` | ``None``                         |
        |               | the value passed is a string, it is interpreted   | or ``str``             |                                  |
        |               | as an image file name to be loaded.               |                        |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | pie_fractions | Fractions of the pie sections for the vertices if | list of ``int`` or     | ``[0.75, 0.25]``                 |
        |               | ``shape=="pie"``.                                 | ``float``              |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+
        | pie_colors    | Colors used in the pie sections if                | list of strings or     | ``('b','g','r','c','m','y','k')``|
        |               | ``shape=="pie"``.                                 | ``float``.             |                                  |
        +---------------+---------------------------------------------------+------------------------+----------------------------------+


    .. table:: **List of edge properties**

        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | Name           | Description                                       | Accepted types         | Default Value                    |
        +================+===================================================+========================+==================================+
        | color          | Color used to stroke the edge lines.              | ``str`` or list of     | ``[0.179, 0.203,0.210, 0.8]``    |
        |                |                                                   | floats                 |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | pen_width      | Width of the line used to draw the edge, in       | ``float`` or ``int``   | ``1.0``                          |
        |                | the default units of the output format (normally  |                        |                                  |
        |                | either pixels or points).                         |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | start_marker,  | Edge markers. Can be one of "none", "arrow",      | ``str`` or ``int``     | ``none``                         |
        | mid_marker,    | "circle", "square", "diamond", or "bar".          |                        |                                  |
        | end_marker     | Optionally, this might take a numeric value       |                        |                                  |
        |                | corresponding to position in the list above.      |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | mid_marker_pos | Relative position of the middle marker.           | ``float``              | ``0.5``                          |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | marker_size    | Size of edge markers, in units appropriate to the | ``float`` or ``int``   | ``4``                            |
        |                | output format (normally either pixels or points). |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | control_points | Control points of a Bézier spline used to draw    | sequence of ``floats`` | ``[]``                           |
        |                | the edge. Each spline segment requires 6 values   |                        |                                  |
        |                | corresponding to the (x,y) coordinates of the two |                        |                                  |
        |                | intermediary control points and the final point.  |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | gradient       | Stop points of a linear gradient used to stroke   | sequence of ``floats`` | ``[]``                           |
        |                | the edge. Each group of 5 elements is interpreted |                        |                                  |
        |                | as ``[o, r, g, b, a]`` where ``o`` is the offset  |                        |                                  |
        |                | in the range [0, 1] and the remaining values      |                        |                                  |
        |                | specify the colors.                               |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | dash_style     | Dash pattern is specified by an array of positive | sequence of ``floats`` | ``[]``                           |
        |                | values. Each value provides the length of         |                        |                                  |
        |                | alternate "on" and "off" portions of the stroke.  |                        |                                  |
        |                | The last value specifies an offset into the       |                        |                                  |
        |                | pattern at which the stroke begins.               |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | text           | Text to draw next to the edges.                   | ``str``                | ``""``                           |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_color     | Color used to draw the text.                      | ``str`` or list of     | ``[0., 0., 0., 1.]``             |
        |                |                                                   | ``floats``             |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_distance  | Distance from the edge and its text.              | ``float`` or ``int``   | ``4``                            |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | text_parallel  | If ``True`` the text will be drawn parallel to    | ``bool``               | ``True``                         |
        |                | the edges.                                        |                        |                                  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_family    | Font family used to draw the text.                | ``str``                | ``"serif"``                      |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_slant     | Font slant used to draw the text.                 | ``cairo.FONT_SLANT_*`` | :data:`cairo.FONT_SLANT_NORMAL`  |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_weight    | Font weight used to draw the text.                | ``cairo.FONT_WEIGHT_*``| :data:`cairo.FONT_WEIGHT_NORMAL` |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+
        | font_size      | Font size used to draw the text.                  | ``float`` or ``int``   | ``12``                           |
        +----------------+---------------------------------------------------+------------------------+----------------------------------+

    Examples
    --------
    .. testcode::
       :hide:

       np.random.seed(42)
       gt.seed_rng(42)
       from numpy import sqrt

    >>> g = gt.price_network(1500)
    >>> deg = g.degree_property_map("in")
    >>> deg.a = 4 * (sqrt(deg.a) * 0.5 + 0.4)
    >>> ebet = gt.betweenness(g)[1]
    >>> ebet.a /= ebet.a.max() / 10.
    >>> eorder = ebet.copy()
    >>> eorder.a *= -1
    >>> pos = gt.sfdp_layout(g)
    >>> control = g.new_edge_property("vector<double>")
    >>> for e in g.edges():
    ...     d = sqrt(sum((pos[e.source()].a - pos[e.target()].a) ** 2)) / 5
    ...     control[e] = [0.3, d, 0.7, d]
    >>> gt.graph_draw(g, pos=pos, vertex_size=deg, vertex_fill_color=deg, vorder=deg,
    ...               edge_color=ebet, eorder=eorder, edge_pen_width=ebet,
    ...               edge_control_points=control, # some curvy edges
    ...               output="graph-draw.pdf")
    <...>

    .. testcode::
       :hide:

       gt.graph_draw(g, pos=pos, vertex_size=deg, vertex_fill_color=deg, vorder=deg,
                     edge_color=ebet, eorder=eorder, edge_pen_width=ebet,
                     edge_control_points=control,
                     output="graph-draw.png")


    .. figure:: graph-draw.*
        :align: center

        SFDP force-directed layout of a Price network with 1500 nodes. The
        vertex size and color indicate the degree, and the edge color and width
        the edge betweenness centrality.

    """

    vprops = vprops.copy() if vprops is not None else {}
    eprops = eprops.copy() if eprops is not None else {}

    props, kwargs = parse_props("vertex", kwargs)
    props = _convert_props(props, "v", g, kwargs.get("vcmap", default_cm))
    vprops.update(props)
    props, kwargs = parse_props("edge", kwargs)
    props = _convert_props(props, "e", g, kwargs.get("ecmap", default_cm))
    eprops.update(props)

    if pos is None:
        if (g.num_vertices() > 2 and output is None and
            not inline and kwargs.get("update_layout", True) and
            mplfig is None):
            L = np.sqrt(g.num_vertices())
            pos = random_layout(g, [L, L])
            if g.num_vertices() > 1000:
                if "multilevel" not in kwargs:
                    kwargs["multilevel"] = True
            if "layout_K" not in kwargs:
                kwargs["layout_K"] = _avg_edge_distance(g, pos) / 10
        else:
            pos = sfdp_layout(g)
    else:
        _check_prop_vector(pos, name="pos", floating=True)
        if output is None and not inline:
            if "layout_K" not in kwargs:
                kwargs["layout_K"] = _avg_edge_distance(g, pos)
            if "update_layout" not in kwargs:
                kwargs["update_layout"] = False

    if "pen_width" in eprops and "marker_size" not in eprops:
        pw = eprops["pen_width"]
        if isinstance(pw, PropertyMap):
            pw = pw.copy("double")
            pw.fa *= 2.75
            eprops["marker_size"] = pw
        else:
            eprops["marker_size"] = pw * 2.75

    if "text" in eprops and "text_distance" not in eprops and "pen_width" in eprops:
        pw = eprops["pen_width"]
        if isinstance(pw, PropertyMap):
            pw = pw.copy("double")
            pw.fa *= 2
            eprops["text_distance"] = pw
        else:
            eprops["text_distance"] = pw * 2

    if "text" in vprops and ("text_color" not in vprops or vprops["text_color"] == "auto"):
        vcmap = kwargs.get("vcmap", matplotlib.cm.jet)
        bg = _convert(vertex_attrs.fill_color,
                      vprops.get("fill_color", _vdefaults["fill_color"]),
                      vcmap)
        bg_color = kwargs.get("bg_color", [1., 1., 1., 1.])
        vprops["text_color"] = auto_colors(g, bg,
                                           vprops.get("text_position",
                                                      _vdefaults["text_position"]),
                                           bg_color)

    if mplfig:
        ax = None
        if isinstance(mplfig, matplotlib.figure.Figure):
            ctr = ax = mplfig.gca()
        elif isinstance(mplfig, matplotlib.axes.Axes):
            ctr = ax = mplfig
        else:
            ctr = mplfig

        artist = GraphArtist(g, pos, vprops, eprops, vorder, eorder, nodesfirst,
                             ax, **kwargs)
        ctr.artists.append(artist)

        if fit_view != False and ax is not None:
            try:
                x, y, w, h = fit_view
            except TypeError:
                x, y = ungroup_vector_property(pos, [0, 1])
                l, r = x.a.min(), x.a.max()
                b, t = y.a.min(), y.a.max()
                w = r - l
                h = t - b
            if fit_view != True:
                w *= float(fit_view)
                h *= float(fit_view)
            ax.set_xlim(l - w * .1, r + w * .1)
            ax.set_ylim(b - h * .1, t + h * .1)

        return pos

    if inline:
        if fmt == "auto":
            if output is None:
                fmt = "png"
            else:
                fmt = get_file_fmt(output)
        output_file = output
        output = io.BytesIO()

    if output is None:
        fit_area = fit_view if fit_view != True else 0.95
        return interactive_window(g, pos, vprops, eprops, vorder, eorder,
                                  nodesfirst, geometry=output_size,
                                  fit_area=fit_area, **kwargs)
    else:
        if isinstance(output, (str, unicode)):
            out, auto_fmt = open_file(output, mode="wb")
        else:
            out = output
            if fmt == "auto":
                raise ValueError("File format must be specified.")

        if fmt == "auto":
            fmt = auto_fmt
        if fmt == "pdf":
            srf = cairo.PDFSurface(out, output_size[0], output_size[1])
        elif fmt == "ps":
            srf = cairo.PSSurface(out, output_size[0], output_size[1])
        elif fmt == "eps":
            srf = cairo.PSSurface(out, output_size[0], output_size[1])
            srf.set_eps(True)
        elif fmt == "svg":
            srf = cairo.SVGSurface(out, output_size[0], output_size[1])
        elif fmt == "png":
            srf = cairo.ImageSurface(cairo.FORMAT_ARGB32, output_size[0],
                                     output_size[1])
        else:
            raise ValueError("Invalid format type: " + fmt)

        cr = cairo.Context(srf)

        adjust_default_sizes(g, output_size, vprops, eprops)
        if fit_view != False:
            try:
                x, y, w, h = fit_view
                offset, zoom = [0, 0], 1
            except TypeError:
                pad = fit_view if fit_view != True else 0.95
                offset, zoom = fit_to_view(g, pos, output_size, vprops["size"],
                                           vprops["pen_width"], None,
                                           vprops.get("text", None),
                                           vprops.get("font_family",
                                                      _vdefaults["font_family"]),
                                           vprops.get("font_size",
                                                      _vdefaults["font_size"]),
                                           pad, cr)
                fit_view = False
        else:
            offset, zoom = [0, 0], 1

        if "bg_color" in kwargs:
            bg_color = kwargs["bg_color"]
            del  kwargs["bg_color"]
            cr.set_source_rgba(bg_color[0], bg_color[1],
                               bg_color[2], bg_color[3])
            cr.paint()

        cr.translate(offset[0], offset[1])
        cr.scale(zoom, zoom)

        cairo_draw(g, pos, cr, vprops, eprops, vorder, eorder,
                   nodesfirst, fit_view=fit_view, **kwargs)

        if fmt == "png":
            srf.write_to_png(out)

        del cr

        if inline:
            img = None
            if fmt == "png":
                img = IPython.display.Image(data=out.getvalue())
            if fmt == "svg":
                img = IPython.display.SVG(data=out.getvalue())
            if img is None:
                inl_out = io.BytesIO()
                inl_srf = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                             output_size[0],
                                             output_size[1])
                inl_cr = cairo.Context(inl_srf)
                inl_cr.set_source_surface(srf, 0, 0)
                inl_cr.paint()
                inl_srf.write_to_png(inl_out)
                del inl_srf
                img = IPython.display.Image(data=inl_out.getvalue())
            srf.finish()
            if output_file is not None:
                if isinstance(output_file, (str, unicode)):
                    ofile, auto_fmt = open_file(output_file, mode="wb")
                else:
                    ofile = output_file
                ofile.write(out.getvalue())
                if isinstance(output_file, (str, unicode)):
                    ofile.close()
            IPython.display.display(img)
        del srf
        return pos


def adjust_default_sizes(g, geometry, vprops, eprops, force=False):
    if "size" not in vprops or force:
        A = geometry[0] * geometry[1]
        N = max(g.num_vertices(), 1)
        vprops["size"] = np.sqrt(A / N) / 3.5

    if "pen_width" not in vprops or force:
        size = vprops["size"]
        if isinstance(vprops["size"], PropertyMap):
            size = vprops["size"].fa.mean()
        vprops["pen_width"] = size / 10
        if "pen_width" not in eprops or force:
            eprops["pen_width"] = size / 10
        if "marker_size" not in eprops or force:
            eprops["marker_size"] = size * 0.8


def scale_ink(scale, vprops, eprops):
    if "size" not in vprops:
        vprops["size"] = _vdefaults["size"]
    if "pen_width" not in vprops:
        vprops["pen_width"] = _vdefaults["pen_width"]
    if "font_size" not in vprops:
        vprops["font_size"] = _vdefaults["font_size"]
    if "pen_width" not in eprops:
        eprops["pen_width"] = _edefaults["pen_width"]
    if "marker_size" not in eprops:
        eprops["marker_size"] = _edefaults["marker_size"]
    if "font_size" not in eprops:
        eprops["font_size"] = _edefaults["font_size"]
    if "text_distance" not in eprops:
        eprops["text_distance"] = _edefaults["text_distance"]

    for props in [vprops, eprops]:
        if isinstance(props["pen_width"], PropertyMap):
            props["pen_width"].fa *= scale
        else:
            props["pen_width"] *= scale
    if isinstance(vprops["size"], PropertyMap):
        vprops["size"].fa *= scale
    else:
        vprops["size"] *= scale
    if isinstance(vprops["font_size"], PropertyMap):
        vprops["font_size"].fa *= scale
    else:
        vprops["font_size"] *= scale
    if isinstance(eprops["marker_size"], PropertyMap):
        eprops["marker_size"].fa *= scale
    else:
        eprops["marker_size"] *= scale
    if isinstance(eprops["font_size"], PropertyMap):
        eprops["font_size"].fa *= scale
    else:
        eprops["font_size"] *= scale
    if isinstance(eprops["text_distance"], PropertyMap):
        eprops["text_distance"].fa *= scale
    else:
        eprops["text_distance"] *= scale

def get_bb(g, pos, size, pen_width, size_scale=1, text=None, font_family=None,
           font_size=None, cr=None):
    size = size.fa if isinstance(size, PropertyMap) else size
    pen_width = pen_width.fa if isinstance(pen_width, PropertyMap) else pen_width
    pos_x, pos_y = ungroup_vector_property(pos, [0, 1])
    if text is not None and text != "":
        if not isinstance(size, PropertyMap):
            uniform = (not isinstance(font_size, PropertyMap) and
                       not isinstance(font_family, PropertyMap))
            size = np.ones(len(pos_x.fa)) * size
        else:
            uniform = False
        for i, v in enumerate(g.vertices()):
            ff = font_family[v] if isinstance(font_family, PropertyMap) \
               else font_family
            cr.select_font_face(ff)
            fs = font_size[v] if isinstance(font_family, PropertyMap) \
               else font_size
            if not isinstance(font_size, PropertyMap):
                cr.set_font_size(fs)
            t = text[v] if isinstance(text, PropertyMap) else text
            if not isinstance(t, (str, unicode)):
                t = str(t)
            extents = cr.text_extents(t)
            s = max(extents[2], extents[3]) * 1.4
            size[i] = max(size[i] * size_scale, s) / size_scale
            if uniform:
                size[:] = size[i]
                break
    sl = label_self_loops(g)
    slm = sl.fa.max() * 0.75 if g.num_edges() > 0 else 0
    delta = (size * size_scale * (slm + 1)) / 2 + pen_width * 2
    x_range = [pos_x.fa.min(), pos_x.fa.max()]
    y_range = [pos_y.fa.min(), pos_y.fa.max()]
    x_delta = [x_range[0] - (pos_x.fa - delta).min(),
               (pos_x.fa + delta).max() - x_range[1]]
    y_delta = [y_range[0] - (pos_y.fa - delta).min(),
               (pos_y.fa + delta).max() - y_range[1]]
    return x_range, y_range, x_delta, y_delta


def fit_to_view(g, pos, geometry, size, pen_width, M=None, text=None,
                font_family=None, font_size=None, pad=0.95, cr=None):
    if g.num_vertices() == 0:
        return [0, 0], 1
    if M is not None:
        pos_x, pos_y = ungroup_vector_property(pos, [0, 1])
        P = np.zeros((2, len(pos_x.fa)))
        P[0, :] = pos_x.fa
        P[1, :] = pos_y.fa
        T = np.zeros((2, 2))
        O = np.zeros(2)
        T[0, 0], T[1, 0], T[0, 1], T[1, 1], O[0], O[1] = M
        P = np.dot(T, P)
        P[0] += O[0]
        P[1] += O[1]
        pos_x.fa = P[0, :]
        pos_y.fa = P[1, :]
        pos = group_vector_property([pos_x, pos_y])
    x_range, y_range, x_delta, y_delta = get_bb(g, pos, size, pen_width,
                                                1, text, font_family,
                                                font_size, cr)
    dx = (x_range[1] - x_range[0])
    dy = (y_range[1] - y_range[0])
    if dx == 0:
        dx = 1
    if dy == 0:
        dy = 1
    zoom_x = (geometry[0] - sum(x_delta)) / dx
    zoom_y = (geometry[1] - sum(y_delta)) / dy
    if np.isnan(zoom_x) or np.isinf(zoom_x) or zoom_x == 0:
        zoom_x = 1
    if np.isnan(zoom_y) or np.isinf(zoom_y) or zoom_y == 0:
        zoom_y = 1
    zoom = min(zoom_x, zoom_y) * pad
    empty_x = (geometry[0] - sum(x_delta)) - dx * zoom
    empty_y = (geometry[1] - sum(y_delta)) - dy * zoom
    offset = [-x_range[0] * zoom + empty_x / 2 + x_delta[0],
              -y_range[0] * zoom + empty_y / 2 + y_delta[0]]
    return offset, zoom


def transform_scale(M, scale):
    p = M.transform_distance(scale / np.sqrt(2),
                             scale / np.sqrt(2))
    return np.sqrt(p[0] ** 2 + p[1] ** 2)

def get_hierarchy_control_points(g, t, tpos, beta=0.8, cts=None, is_tree=True,
                                 max_depth=None):
    r"""Return the Bézier spline control points for the edges in ``g``, given the hierarchical structure encoded in graph `t`.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be drawn.
    t : :class:`~graph_tool.Graph`
        Directed graph containing the hierarchy of ``g``. It must be a directed
        tree with a single root. The direction of the edges point from the root
        to the leaves, and the vertices in ``t`` with index in the range
        :math:`[0, N-1]`, with :math:`N` being the number of vertices in ``g``,
        must correspond to the respective vertex in ``g``.
    tpos : :class:`~graph_tool.PropertyMap`
        Vector-valued vertex property map containing the x and y coordinates of
        the vertices in graph ``t``.
    beta : ``float`` (optional, default: ``0.8`` or :class:`~graph_tool.PropertyMap`)
        Edge bundling strength. For ``beta == 0`` the edges are straight lines,
        and for ``beta == 1`` they strictly follow the hierarchy. This can be
        optionally an edge property map, which specified a different bundling
        strength for each edge.
    cts : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        Edge property map of type ``vector<double>`` where the control points
        will be stored.
    is_tree : ``bool`` (optional, default: ``True``)
        If ``True``, ``t`` must be a directed tree, otherwise it can be any
        connected graph.
    max_depth : ``int`` (optional, default: ``None``)
        If supplied, only the first ``max_depth`` bottom levels of the hierarchy
        will be used.


    Returns
    -------

    cts : :class:`~graph_tool.PropertyMap`
        Vector-valued edge property map containing the Bézier spline control
        points for the edges in ``g``.

    Notes
    -----
    This is an implementation of the edge-bundling algorithm described in
    [holten-hierarchical-2006]_.


    Examples
    --------
    .. testsetup:: nested_cts

       gt.seed_rng(42)
       np.random.seed(42)

    .. doctest:: nested_cts

       >>> g = gt.collection.data["netscience"]
       >>> g = gt.GraphView(g, vfilt=gt.label_largest_component(g))
       >>> g.purge_vertices()
       >>> state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)
       >>> t = gt.get_hierarchy_tree(state)[0]
       >>> tpos = pos = gt.radial_tree_layout(t, t.vertex(t.num_vertices() - 1), weighted=True)
       >>> cts = gt.get_hierarchy_control_points(g, t, tpos)
       >>> pos = g.own_property(tpos)
       >>> b = state.levels[0].b
       >>> shape = b.copy()
       >>> shape.a %= 14
       >>> gt.graph_draw(g, pos=pos, vertex_fill_color=b, vertex_shape=shape, edge_control_points=cts,
       ...               edge_color=[0, 0, 0, 0.3], vertex_anchor=0, output="netscience_nested_mdl.pdf")
       <...>

    .. testcleanup:: nested_cts

       gt.graph_draw(g, pos=pos, vertex_fill_color=b, vertex_shape=shape, edge_control_points=cts, edge_color=[0, 0, 0, 0.3], vertex_anchor=0, output="netscience_nested_mdl.png")

    .. figure:: netscience_nested_mdl.*
       :align: center

       Block partition of a co-authorship network, which minimizes the description
       length of the network according to the nested (degree-corrected) stochastic blockmodel.



    References
    ----------

    .. [holten-hierarchical-2006] Holten, D. "Hierarchical Edge Bundles:
       Visualization of Adjacency Relations in Hierarchical Data.", IEEE
       Transactions on Visualization and Computer Graphics 12, no. 5, 741–748
       (2006). :doi:`10.1109/TVCG.2006.147`
    """

    if cts is None:
        cts = g.new_edge_property("vector<double>")
    if cts.value_type() != "vector<double>":
        raise ValueError("cts property map must be of type 'vector<double>' not '%s' " % cts.value_type())

    u = GraphView(g, directed=True)
    tu = GraphView(t, directed=True)

    if not isinstance(beta, PropertyMap):
        beta = u.new_edge_property("double", beta)
    else:
        beta = beta.copy("double")

    if max_depth is None:
        max_depth = t.num_vertices()

    tu = GraphView(tu, skip_vfilt=True)
    tpos = tu.own_property(tpos)
    libgraph_tool_draw.get_cts(u._Graph__graph,
                               tu._Graph__graph,
                               _prop("v", tu, tpos),
                               _prop("e", u, beta),
                               _prop("e", u, cts),
                               is_tree, max_depth)
    return cts

#
# The functions and classes below depend on GTK
# =============================================
#

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GdkPixbuf
    from gi.repository import GObject as gobject
    from .gtk_draw import *
except (ImportError, RuntimeError) as e:
    msg = "Error importing Gtk module: %s; GTK+ drawing will not work." % str(e)
    warnings.warn(msg, RuntimeWarning)

def gen_surface(name):
    fobj, fmt = open_file(name)
    if fmt in ["png", "PNG"]:
        sfc = cairo.ImageSurface.create_from_png(fobj)
        return sfc
    else:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(name)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, pixbuf.get_width(),
                                     pixbuf.get_height())
        cr = cairo.Context(surface)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        return surface
#
# matplotlib
# ==========
#

class GraphArtist(matplotlib.artist.Artist):
    """:class:`matplotlib.artist.Artist` specialization that draws
       :class:`graph_tool.Graph` instances.

    .. warning::

        Only Cairo-based backends are supported.

    """

    def __init__(self, g, pos, vprops, eprops, vorder, eorder,
                nodesfirst, ax=None, **kwargs):
        matplotlib.artist.Artist.__init__(self)
        self.g = g
        self.pos = pos
        self.vprops = vprops
        self.eprops = eprops
        self.vorder = vorder
        self.eorder = eorder
        self.nodesfirst = nodesfirst
        self.ax = ax
        self.kwargs = kwargs

    def draw(self, renderer):
        if not isinstance(renderer, matplotlib.backends.backend_cairo.RendererCairo):
            raise NotImplementedError("graph plotting is supported only on Cairo backends")

        ctx = renderer.gc.ctx

        if not isinstance(ctx, cairo.Context):
            ctx = _UNSAFE_cairocffi_context_to_pycairo(ctx)

        ctx.save()

        if self.ax is not None:
            m = self.ax.transData.get_affine().get_matrix()
            m = cairo.Matrix(m[0,0], m[1, 0], m[0, 1], m[1, 1], m[0, 2], m[1,2])
            ctx.set_matrix(m)

            l, r = self.ax.get_xlim()
            b, t = self.ax.get_ylim()
            ctx.rectangle(l, b, r-l, t-b)
            ctx.clip()

        # flip y direction
        x, y = ungroup_vector_property(self.pos, [0, 1])
        l, t, r, b = ctx.clip_extents()
        y.fa = b + t - y.fa
        pos = group_vector_property([x, y])

        cairo_draw(self.g, pos, ctx, self.vprops, self.eprops,
                   self.vorder, self.eorder, self.nodesfirst, self.kwargs)

        ctx.restore()


#
# Drawing hierarchies
# ===================
#

def draw_hierarchy(state, pos=None, layout="radial", beta=0.8, node_weight=None,
                   vprops=None, eprops=None, hvprops=None, heprops=None,
                   subsample_edges=None, deg_order=True, deg_size=True,
                   vsize_scale=1, hsize_scale=1, hshortcuts=0, hide=0,
                   bip_aspect=1., empty_branches=True, **kwargs):
    r"""Draw a nested block model state in a circular hierarchy layout with edge
    bundling.

    Parameters
    ----------
    state : :class:`~graph_tool.community.NestedBlockState`
        Nested block state to be drawn.
    pos : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
        If supplied, this specifies a vertex property map with the positions of
        the vertices in the layout.
    layout : ``str`` or :class:`~graph_tool.PropertyMap` (optional, default: ``"radial"``)
        If ``layout == "radial"`` :func:`~graph_tool.draw.radial_tree_layout`
        will be used. If ``layout == "sfdp"``, the hierarchy tree will be
        positioned using :func:`~graph_tool.draw.sfdp_layout`. If ``layout ==
        "bipartite"`` a bipartite layout will be used. If instead a
        :class:`~graph_tool.PropertyMap` is provided, it must correspond to the
        position of the hierarchy tree.
    beta : ``float`` (optional, default: ``.8``)
        Edge bundling strength.
    vprops : dict (optional, default: ``None``)
        Dictionary with the vertex properties. Individual properties may also be
        given via the ``vertex_<prop-name>`` parameters, where ``<prop-name>`` is
        the name of the property. See :func:`~graph_tool.draw.graph_draw` for
        details.
    eprops : dict (optional, default: ``None``)
        Dictionary with the edge properties. Individual properties may also be
        given via the ``edge_<prop-name>`` parameters, where ``<prop-name>`` is
        the name of the property. See :func:`~graph_tool.draw.graph_draw` for
        details.
    hvprops : dict (optional, default: ``None``)
        Dictionary with the vertex properties for the *hierarchy tree*.
        Individual properties may also be given via the ``hvertex_<prop-name>``
        parameters, where ``<prop-name>`` is the name of the property. See
        :func:`~graph_tool.draw.graph_draw` for details.
    heprops : dict (optional, default: ``None``)
        Dictionary with the edge properties for the *hierarchy tree*. Individual
        properties may also be given via the ``hedge_<prop-name>`` parameters,
        where ``<prop-name>`` is the name of the property. See
        :func:`~graph_tool.draw.graph_draw` for details.
    subsample_edges : ``int`` or list of :class:`~graph_tool.Edge` instances (optional, default: ``None``)
        If provided, only this number of random edges will be drawn. If the
        value is a list, it should include the edges that are to be drawn.
    deg_order : ``bool`` (optional, default: ``True``)
        If ``True``, the vertices will be ordered according to degree inside
        each group.
    deg_size : ``bool`` (optional, default: ``True``)
        If ``True``, the (total) node degrees will be used for the default
        vertex sizes..
    vsize_scale : ``float`` (optional, default: ``1.``)
        Multiplicative factor for the default vertex sizes.
    hsize_scale : ``float`` (optional, default: ``1.``)
        Multiplicative factor for the default sizes of the hierarchy nodes.
    hshortcuts : ``int`` (optional, default: ``0``)
        Include shortcuts to the number of upper layers in the hierarchy
        determined by this parameter.
    hide : ``int`` (optional, default: ``0``)
        Hide upper levels of the hierarchy.
    bip_aspect : ``float`` (optional, default: ``1.``)
        If ``layout == "bipartite"``, this will define the aspect ratio of layout.
    empty_branches : ``bool`` (optional, default: ``False``)
        If ``empty_branches == False``, dangling branches at the upper layers
        will be pruned.
    vertex_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``vertex_<prop-name>`` specify the
        vertex property with name ``<prop-name>``, as an alternative to the
        ``vprops`` parameter. See :func:`~graph_tool.draw.graph_draw` for
        details.
    edge_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``edge_<prop-name>`` specify the edge
        property with name ``<prop-name>``, as an alternative to the ``eprops``
        parameter. See :func:`~graph_tool.draw.graph_draw` for details.
    hvertex_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``hvertex_<prop-name>`` specify the
        vertex property with name ``<prop-name>``, as an alternative to the
        ``hvprops`` parameter. See :func:`~graph_tool.draw.graph_draw` for
        details.
    hedge_* : :class:`~graph_tool.PropertyMap` or arbitrary types (optional, default: ``None``)
        Parameters following the pattern ``hedge_<prop-name>`` specify the edge
        property with name ``<prop-name>``, as an alternative to the ``heprops``
        parameter. See :func:`~graph_tool.draw.graph_draw` for details.
    **kwargs :
        All remaining keyword arguments will be passed to the
        :func:`~graph_tool.draw.graph_draw` function.

    Returns
    -------
    pos : :class:`~graph_tool.PropertyMap`
        This is a vertex property map with the positions of
        the vertices in the layout.
    t : :class:`~graph_tool.Graph`
        This is a the hierarchy tree used in the layout.
    tpos : :class:`~graph_tool.PropertyMap`
        This is a vertex property map with the positions of
        the hierarchy tree in the layout.

    Examples
    --------
    .. testsetup:: draw_hierarchy

       gt.seed_rng(42)
       np.random.seed(42)

    .. doctest:: draw_hierarchy

       >>> g = gt.collection.data["celegansneural"]
       >>> state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)
       >>> gt.draw_hierarchy(state, output="celegansneural_nested_mdl.pdf")
       (...)

    .. testcleanup:: draw_hierarchy

       gt.draw_hierarchy(state, output="celegansneural_nested_mdl.png")

    .. figure:: celegansneural_nested_mdl.*
       :align: center

       Hierarchical block partition of the C. elegans neural network, which
       minimizes the description length of the network according to the nested
       (degree-corrected) stochastic blockmodel.


    References
    ----------
    .. [holten-hierarchical-2006] Holten, D. "Hierarchical Edge Bundles:
       Visualization of Adjacency Relations in Hierarchical Data.", IEEE
       Transactions on Visualization and Computer Graphics 12, no. 5, 741–748
       (2006). :doi:`10.1109/TVCG.2006.147`
    """

    g = state.g

    overlap = state.levels[0].overlap
    if overlap:
        ostate = state.levels[0]
        bv, bcin, bcout, bc = ostate.get_overlap_blocks()
        be = ostate.get_edge_blocks()
        orig_state = state
        state = state.copy()
        b = ostate.get_majority_blocks()
        state.levels[0] = BlockState(g, b=b)
    else:
        b = state.levels[0].b

    if subsample_edges is not None:
        emask = g.new_edge_property("bool", False)
        if isinstance(subsample_edges, int):
            eidx = g.edge_index.copy("int").fa.copy()
            numpy.random.shuffle(eidx)
            emask = g.new_edge_property("bool")
            emask.a[eidx[:subsample_edges]] = True
        else:
            for e in subsample_edges:
                emask[e] = True
        g = GraphView(g, efilt=emask)

    t, tb, vorder = get_hierarchy_tree(state,
                                       empty_branches=empty_branches)

    if layout == "radial":
        if not deg_order:
            vorder = None
        if pos is not None:
            x, y = ungroup_vector_property(pos, [0, 1])
            x.fa -= x.fa.mean()
            y.fa -= y.fa.mean()
            angle = g.new_vertex_property("double")
            angle.fa = (numpy.arctan2(y.fa, x.fa) + 2 * numpy.pi) % (2 * numpy.pi)
            vorder = angle
        if node_weight is not None:
            node_weight = t.own_property(node_weight.copy())
            node_weight.a[node_weight.a == 0] = 1
        tpos = radial_tree_layout(t, root=t.vertex(t.num_vertices() - 1,
                                                   use_index=False),
                                  node_weight=node_weight,
                                  rel_order=vorder)
    elif layout == "bipartite":
        tpos = get_bip_hierachy_pos(state, aspect=bip_aspect,
                                    node_weight=node_weight)
        tpos = t.own_property(tpos)
    elif layout == "sfdp":
        if pos is None:
            tpos = sfdp_layout(t)
        else:
            x, y = ungroup_vector_property(pos, [0, 1])
            x.fa -= x.fa.mean()
            y.fa -= y.fa.mean()
            K = numpy.sqrt(x.fa.std() + y.fa.std()) / 10
            tpos = t.new_vertex_property("vector<double>")
            for v in t.vertices():
                if int(v) < g.num_vertices(True):
                    tpos[v] = [x[v], y[v]]
                else:
                    tpos[v] = [0, 0]
            pin = t.new_vertex_property("bool")
            pin.a[:g.num_vertices(True)] = True
            tpos = sfdp_layout(t, K=K, pos=tpos, pin=pin, multilevel=False)
    else:
        tpos = t.own_property(layout)

    hvvisible = t.new_vertex_property("bool", True)
    if hide > 0:
        root = t.vertex(t.num_vertices(True) - 1)
        dist = shortest_distance(t, source=root)
        hvvisible.fa = dist.fa >= hide

    pos = g.own_property(tpos.copy())

    cts = get_hierarchy_control_points(g, t, tpos, beta,
                                       max_depth=len(state.levels) - hshortcuts)

    vprops_orig = vprops
    eprops_orig = eprops
    hvprops_orig = vprops
    heprops_orig = eprops
    kwargs_orig = kwargs

    vprops = vprops.copy() if vprops is not None else {}
    eprops = eprops.copy() if eprops is not None else {}

    props, kwargs = parse_props("vertex", kwargs)
    vprops.update(props)
    vprops.setdefault("fill_color", b)
    vprops.setdefault("color", b)
    vprops.setdefault("shape", _vdefaults["shape"] if not overlap else "pie")
    s = max(200 / numpy.sqrt(g.num_vertices()), 5)
    vprops.setdefault("size", prop_to_size(g.degree_property_map("total"), s/5, s))

    if vprops.get("text_position", None) == "centered":
        angle, text_pos = centered_rotation(g, pos, text_pos=True)
        vprops["text_position"] = text_pos
        vprops["text_rotation"] = angle

    self_loops = label_self_loops(g, mark_only=True)
    if self_loops.fa.max() > 0:
        parallel_distance = vprops.get("size", _vdefaults["size"])
        if isinstance(parallel_distance, PropertyMap):
            parallel_distance = parallel_distance.fa.mean()
        cts_p = position_parallel_edges(g, pos, numpy.nan,
                                        parallel_distance)
        gu = GraphView(g, efilt=self_loops)
        for e in gu.edges():
            cts[e] = cts_p[e]


    vprops = _convert_props(vprops, "v", g, kwargs.get("vcmap", default_cm),
                            pmap_default=True)

    props, kwargs = parse_props("edge", kwargs)
    eprops.update(props)
    eprops.setdefault("control_points", cts)
    eprops.setdefault("pen_width", _edefaults["pen_width"])
    eprops.setdefault("color", list(_edefaults["color"][:-1]) + [.6])
    eprops.setdefault("end_marker", "arrow" if g.is_directed() else "none")
    eprops = _convert_props(eprops, "e", g, kwargs.get("ecmap", default_cm),
                            pmap_default=True)

    hvprops = hvprops.copy() if hvprops is not None else {}
    heprops = heprops.copy() if heprops is not None else {}

    props, kwargs = parse_props("hvertex", kwargs)
    hvprops.update(props)

    blue = list(color_converter.to_rgba("#729fcf"))
    blue[-1] = .6
    hvprops.setdefault("fill_color", blue)
    hvprops.setdefault("color", [1, 1, 1, 0])
    hvprops.setdefault("shape", "square")
    hvprops.setdefault("size", 10)

    if hvprops.get("text_position", None) == "centered":
        angle, text_pos = centered_rotation(t, tpos, text_pos=True)
        hvprops["text_position"] = text_pos
        hvprops["text_rotation"] = angle

    hvprops = _convert_props(hvprops, "v", t, kwargs.get("vcmap", default_cm),
                             pmap_default=True)

    props, kwargs = parse_props("hedge", kwargs)
    heprops.update(props)

    heprops.setdefault("color", blue)
    heprops.setdefault("end_marker", "arrow")
    heprops.setdefault("marker_size", 8.)
    heprops.setdefault("pen_width", 1.)

    heprops = _convert_props(heprops, "e", t, kwargs.get("ecmap", default_cm),
                             pmap_default=True)

    vcmap = kwargs.get("vcmap", default_cm)
    ecmap = kwargs.get("ecmap", vcmap)

    B = state.levels[0].B

    if overlap and "pie_fractions" not in vprops:
        vprops["pie_fractions"] = bc.copy("vector<double>")
        if "pie_colors" not in vprops:
            vertex_pie_colors = g.new_vertex_property("vector<double>")
            nodes = defaultdict(list)
            def conv(k):
                clrs = [vcmap(r / (B - 1) if B > 1 else 0) for r in k]
                return [item for l in clrs for item in l]
            map_property_values(bv, vertex_pie_colors, conv)
            vprops["pie_colors"] = vertex_pie_colors

    gradient = eprops.get("gradient", None)
    if gradient is None:
        gradient = g.new_edge_property("double")
        gradient = group_vector_property([gradient])
        ecolor = eprops.get("ecolor", _edefaults["color"])
        eprops["gradient"] = gradient
        if overlap:
            for e in g.edges():                       # ******** SLOW *******
                r, s = be[e]
                if not g.is_directed() and e.source() > e.target():
                    r, s = s, r
                gradient[e] = [0] + list(vcmap(r / (B - 1))) + \
                              [1] + list(vcmap(s / (B - 1)))
                if isinstance(ecolor, PropertyMap):
                    gradient[e][4] = gradient[e][9] = ecolor[e][3]
                else:
                    gradient[e][4] = gradient[e][9] = ecolor[3]


    t_orig = t
    t = GraphView(t,
                  vfilt=lambda v: int(v) >= g.num_vertices(True) and hvvisible[v])

    t_vprops = {}
    t_eprops = {}

    props = []
    for k in set(list(vprops.keys()) + list(hvprops.keys())):
        t_vprops[k] = (vprops.get(k, None), hvprops.get(k, None))
        props.append(t_vprops[k])
    for k in set(list(eprops.keys()) + list(heprops.keys())):
        t_eprops[k] = (eprops.get(k, None), heprops.get(k, None))
        props.append(t_eprops[k])

    props.append((pos, tpos))
    props.append((g.vertex_index, tb))
    props.append((b, None))

    u, props = graph_union(g, t, props=props)

    for k in set(list(vprops.keys()) + list(hvprops.keys())):
        t_vprops[k] = props.pop(0)
    for k in set(list(eprops.keys()) + list(heprops.keys())):
        t_eprops[k] = props.pop(0)
    pos = props.pop(0)
    tb = props.pop(0)
    b = props.pop(0)

    def update_cts(widget, gg, picked, pos, vprops, eprops):
        vmask = gg.vertex_index.copy("int")
        u = GraphView(gg, directed=False, vfilt=vmask.fa < g.num_vertices(True))
        cts = eprops["control_points"]
        get_hierarchy_control_points(u, t_orig, pos, beta, cts=cts,
                                     max_depth=len(state.levels) - hshortcuts)

    def draw_branch(widget, gg, key_id, picked, pos, vprops, eprops):
        if key_id == ord('b'):
            if picked is not None and not isinstance(picked, PropertyMap) and int(picked) > g.num_vertices(True):
                p = shortest_path(t_orig, source=t_orig.vertex(t_orig.num_vertices(True) - 1),
                                  target=picked)[0]
                l = len(state.levels) - max(len(p), 1)

                bstack = state.get_bstack()
                bs = [s.vp["b"].a for s in bstack[:l+1]]
                bs[-1][:] = 0

                if not overlap:
                    b = state.project_level(l).b
                    u = GraphView(g, vfilt=b.a == tb[picked])
                    u.vp["b"] = state.levels[0].b
                    u = Graph(u, prune=True)
                    b = u.vp["b"]
                    bs[0] = b.a
                else:
                    be = orig_state.project_level(l).get_edge_blocks()
                    emask = g.new_edge_property("bool")
                    for e in g.edges():
                        rs = be[e]
                        if rs[0] == tb[picked] and rs[1] == tb[picked]:
                            emask[e] = True
                    u = GraphView(g, efilt=emask)
                    d = u.degree_property_map("total")
                    u = GraphView(u, vfilt=d.fa > 0)
                    u.ep["be"] = orig_state.levels[0].get_edge_blocks()
                    u = Graph(u, prune=True)
                    be = u.ep["be"]
                    s = OverlapBlockState(u, b=be)
                    bs[0] = s.b.a.copy()

                nstate = NestedBlockState(u, bs=bs,
                                          base_type=type(state.levels[0]),
                                          deg_corr=state.deg_corr)

                kwargs_ = kwargs_orig.copy()
                if "no_main" in kwargs_:
                    del kwargs_["no_main"]
                draw_hierarchy(nstate, beta=beta, vprops=vprops_orig,
                               eprops=eprops_orig, hvprops=hvprops_orig,
                               heprops=heprops_orig,
                               subsample_edges=subsample_edges,
                               deg_order=deg_order, empty_branches=False,
                               no_main=True, **kwargs_)

        if key_id == ord('r'):
            if layout == "radial":
                x, y = ungroup_vector_property(pos, [0, 1])
                x.fa -= x.fa.mean()
                y.fa -= y.fa.mean()
                angle = gg.new_vertex_property("double")
                angle.fa = (numpy.arctan2(y.fa, x.fa) + 2 * numpy.pi) % (2 * numpy.pi)
                tpos = radial_tree_layout(t_orig,
                                          root=t_orig.vertex(t_orig.num_vertices(True) - 1),
                                          rel_order=angle)
                gg.copy_property(tpos, pos)

            update_cts(widget, gg, picked, pos, vprops, eprops)

            if widget.vertex_matrix is not None:
                widget.vertex_matrix.update()
            widget.picked = None
            widget.selected.fa = False

            widget.fit_to_window()
            widget.regenerate_surface(reset=True)
            widget.queue_draw()

    if kwargs.get("output", None) is None:
        kwargs["layout_callback"] = update_cts
        kwargs["key_press_callback"] = draw_branch

    pos = graph_draw(u, pos, vprops=t_vprops, eprops=t_eprops, vorder=vorder,
                     **kwargs)

    if isinstance(pos, PropertyMap):
        pos = g.own_property(pos)
        t_orig.copy_property(pos, tpos, g=u)
    else:
        pos = (g.own_property(pos[0]),
               g.own_property(pos[1]))
        t_orig.copy_property(pos[0], tpos, g=u)
    return pos, t_orig, tpos


def get_bip_hierachy_pos(state, aspect=1., node_weight=None):

    if state.levels[0].overlap:
        g = state.g
        ostate = state.levels[0]
        bv, bcin, bcout, bc = ostate.get_overlap_blocks()
        be = ostate.get_edge_blocks()

        n_r = zeros(ostate.B)
        b = g.new_vertex_property("int")
        for v in g.vertices():
            i = bc[v].a.argmax()
            b[v] = bv[v][i]
            n_r[b[v]] += 1

        orphans = [r for r in range(ostate.B) if n_r[r] == 0]

        for v in g.vertices():
            for r in orphans:
                b[v] = r

        orig_state = state
        state = state.copy()
        state.levels[0] = BlockState(g, b=b)

    g = state.g

    deg = g.degree_property_map("total")

    t, tb, order = get_hierarchy_tree(state)

    root = t.vertex(t.num_vertices(True) - 1)
    if root.out_degree() > 2:
        clabel = is_bipartite(g, partition=True)[1].copy("int")
        if state.levels[0].overlap:
            ostate = OverlapBlockState(g, b=clabel)
            ostate = orig_state.copy(clabel=clabel)
            bc = ostate.propagate_clabel(len(state.levels) - 2)
        else:
            state = state.copy(clabel=clabel)
            bc = state.propagate_clabel(len(state.levels) - 2)

        ps = list(root.out_neighbours())
        t.clear_vertex(root)

        p1 = t.add_vertex()
        p2 = t.add_vertex()

        t.add_edge(root, p1)
        t.add_edge(root, p2)
        for p in ps:
            if bc.a[tb[p]] == 0:
                t.add_edge(p2, p)
            else:
                t.add_edge(p1, p)

    w = t.new_vertex_property("double")
    for v in t.vertices():
        if v.in_degree() == 0:
            break
        if v.out_degree() == 0:
            w[v] = 1 if node_weight is None else node_weight[v]
        parent, = v.in_neighbours()
        w[parent] += w[v]

    pos = t.new_vertex_property("vector<double>")

    pos[root] = (0., 0.)

    p1, p2 = root.out_neighbours()

    if ((w[p1] == w[p2] and p1.out_degree() > p2.out_degree()) or
        w[p1] > w[p2]):
        p1, p2 = p2, p1

    L = len(state.levels)
    pos[p1] = (-1 / L * .5 * aspect, 0)
    pos[p2] = (+1 / L * .5 * aspect, 0)

    for i, p in enumerate([p1, p2]):
        roots = [p]
        while len(roots) > 0:
            nroots = []
            for r in roots:
                cw = pos[r][1] - w[r] / (2. * w[p])
                for v in sorted(r.out_neighbours(), key=lambda a: order[a]):
                    pos[v] = (0, 0)
                    if i == 0:
                        pos[v][0] = pos[r][0] - 1 / L * .5 * aspect
                    else:
                        pos[v][0] = pos[r][0] + 1 / L * .5 * aspect
                    pos[v][1] = cw + w[v] / (2. * w[p])
                    cw += w[v] / w[p]
                    nroots.append(v)
            roots = nroots
    return pos


# Handle cairo contexts from cairocffi

try:
    import cairocffi
    import ctypes
    pycairo = ctypes.PyDLL(cairo._cairo.__file__)
    pycairo.PycairoContext_FromContext.restype = ctypes.c_void_p
    pycairo.PycairoContext_FromContext.argtypes = 3 * [ctypes.c_void_p]
    ctypes.pythonapi.PyList_Append.argtypes = 2 * [ctypes.c_void_p]
except ImportError:
    pass

def _UNSAFE_cairocffi_context_to_pycairo(cairocffi_context):
    # Sanity check. Continuing with another type would probably segfault.
    if not isinstance(cairocffi_context, cairocffi.Context):
        raise TypeError('Expected a cairocffi.Context, got %r'
                        % cairocffi_context)

    # Create a reference for PycairoContext_FromContext to take ownership of.
    cairocffi.cairo.cairo_reference(cairocffi_context._pointer)
    # Casting the pointer to uintptr_t (the integer type as wide as a pointer)
    # gets the context’s integer address.
    # On CPython id(cairo.Context) gives the address to the Context type,
    # as expected by PycairoContext_FromContext.
    address = pycairo.PycairoContext_FromContext(
        int(cairocffi.ffi.cast('uintptr_t', cairocffi_context._pointer)),
        id(cairo.Context),
        None)
    assert address
    # This trick uses Python’s C API
    # to get a reference to a Python object from its address.
    temp_list = []
    assert ctypes.pythonapi.PyList_Append(id(temp_list), address) == 0
    return temp_list[0]

# Bottom imports to avoid circular dependency issues
from .. inference import get_hierarchy_tree, NestedBlockState, BlockState, \
    OverlapBlockState

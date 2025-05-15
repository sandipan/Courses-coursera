from __future__ import division, absolute_import, print_function
import sys
if sys.version_info < (3,):
    range = xrange
else:
    unicode = str

import os
from matplotlib import rc
from matplotlib import rcParams

font_size=14
rcParams["backend"] = "PDF"
rcParams["figure.figsize"] = (4, 3)
rcParams["font.family"] = "Serif"
rcParams["font.serif"] = ["Palatino"]
rcParams["font.size"] = font_size
rcParams["axes.labelsize"] = font_size
rcParams["xtick.labelsize"] = font_size - 2
rcParams["ytick.labelsize"] = font_size - 2
rcParams["legend.numpoints"] = 1
rcParams["legend.fontsize"] = "small"
rcParams["lines.markersize"] = 4
rcParams["figure.subplot.right"] = 0.95
rcParams["figure.subplot.top"] = 0.95
rcParams["figure.subplot.right"] = 0.95
rcParams["figure.subplot.top"] = 0.95
rcParams["figure.subplot.left"] = 0.2
rcParams["figure.subplot.bottom"] = 0.2

rcParams["image.cmap"] = "hot"

rcParams["text.usetex"] = True

rcParams["ps.usedistiller"] = "xpdf"
rcParams["pdf.compression"] = 9
rcParams["ps.useafm"] = True
rcParams["path.simplify"] = True
rcParams["text.latex.preamble"] = [#"\usepackage{times}",
                                   #"\usepackage{euler}",
                                   r"\usepackage{amssymb}",
                                   r"\usepackage{amsmath}"]

import scipy
import scipy.stats
import numpy as np
from pylab import *
from numpy import *
import graph_tool.all as gt
import random as prandom

figure()

try:
    gt.openmp_set_num_threads(1)
except RuntimeError:
    pass

prandom.seed(42)
np.random.seed(42)
gt.seed_rng(42)

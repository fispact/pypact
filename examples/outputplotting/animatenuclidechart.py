#!/usr/bin/env python3

from __future__ import division
import os
from operator import attrgetter

import numpy as np

import pypact as pp
import pypact.analysis as ppa

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test127.out"
)

plt = ppa.AnimatedMatrixPlotAdapter()

# Property to animate
prop = "grams"

matricies = []
with pp.Reader(filename) as output:
    for t in output:
        minN = min(t.nuclides, key=attrgetter("isotope")).isotope
        maxN = max(t.nuclides, key=attrgetter("isotope")).isotope
        minZ = ppa.find_z(min(t.nuclides, key=lambda x: ppa.find_z(x.element)).element)
        maxZ = ppa.find_z(max(t.nuclides, key=lambda x: ppa.find_z(x.element)).element)

        matrix = np.zeros((maxN + 1, maxZ + 1))

        for n in t.nuclides:
            matrix[n.isotope, ppa.find_z(n.element)] = getattr(n, prop)

        matricies.append(matrix)

anim = plt.animatedchart(
    matricies,
    xlabel="Nucleon Number (N)",
    ylabel="Proton Number (Z)",
    zstep=2,
    nstep=2,
    minX=minN,
    maxX=maxN,
    minY=minZ,
    maxY=maxZ,
    timeinterval=1,
)
anim.save("./animation.gif", writer="imagemagick", fps=3)
# plt.matrixplot(matrix)

# show the plots
plt.show()

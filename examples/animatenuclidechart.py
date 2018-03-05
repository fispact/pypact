#!/usr/bin/env python3

from __future__ import division
import os
from operator import attrgetter

import numpy as np

from pypact.reader import Reader
from pypact.library.nuclidelib import findZ
from pypact.analysis.plotadapter import AnimatedMatrixPlotAdapter

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', 'reference', 'test127.out')

plt = AnimatedMatrixPlotAdapter()

# Property to animate
prop = 'grams'

matricies = []
with Reader(filename) as output:
    for t in output:
        minN = min(t.nuclides,key=attrgetter('isotope')).isotope
        maxN = max(t.nuclides,key=attrgetter('isotope')).isotope
        minZ = findZ(min(t.nuclides,key=lambda x: findZ(x.element)).element)
        maxZ = findZ(max(t.nuclides,key=lambda x: findZ(x.element)).element)

        matrix = np.zeros((maxN+1,maxZ+1))

        for n in t.nuclides:
            matrix[n.isotope, findZ(n.element)] = getattr(n, prop)

        matricies.append(matrix)

anim = plt.animatedchart(matricies,
                         xlabel="Nucleon Number (N)",
                         ylabel="Proton Number (Z)",
                         zstep=2,
                         nstep=2,
                         minX=minN,
                         maxX=maxN,
                         minY=minZ,
                         maxY=maxZ,
                         timeinterval=1)
#plt.matrixplot(matrix)

# show the plots
plt.show()

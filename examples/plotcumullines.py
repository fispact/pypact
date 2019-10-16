#!/usr/bin/env python3

"""
    Example on showing the cumulative number of gamma lines
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference', 'printlib5.out')

logX = True

X = np.linspace(0, 1e7, 1000)
if logX:
    X = np.logspace(1, 7, 1000)

energies = []
with pp.PrintLib5Reader(filename) as output:
    for m in tqdm(output.spectral_data):
        # all gamma lines
        if m.type == "gamma":
            for l in m.lines:
                energies.append(l[0])

energies = sorted(energies)
cumulative = []
for x in tqdm(X):
    count = np.count_nonzero(energies < x)
    cumulative.append(count)

if logX:
    plt.loglog(X, cumulative, color='k', linewidth=3, alpha=1.0)
else:
    plt.semilogy(X, cumulative, color='k', linewidth=3, alpha=1.0)
plt.xlabel("Energy (eV)")
plt.ylabel("Cumulative number of lines")
plt.show()

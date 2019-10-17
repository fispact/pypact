#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', '..', 'reference', 'printlib5.out')

mean_energy = 0.0
energies = []
intensities = []
with pp.PrintLib5Reader(filename) as output:
    for m in output.spectral_data:
        if m.zai == 110240 and m.type == "gamma":
            mean_energy = m.mean_energy
            for l in m.lines:
                # add zeros either side to make plotting nicer
                energies.append(l[0]-0.1)
                intensities.append(1e-10)
                # actual data
                energies.append(l[0])
                intensities.append(l[2])
                # add zeros either side to make plotting nicer
                energies.append(l[0]+0.1)
                intensities.append(1e-10)
            break

#plt.axvline(x=mean_energy, color='r', linewidth=2.0, label="Mean energy")
plt.semilogy(energies, intensities, color='k', linewidth=0.4, label="Gamma spectra")
#plt.ylim(1e-5, 2)
plt.xlabel("Energy (eV)")
plt.ylabel("Intensity")
#plt.title("U235")
plt.legend()
plt.show()

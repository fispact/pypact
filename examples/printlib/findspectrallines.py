#!/usr/bin/env python3

import os
import pyfispact as pf
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "printlib5.out"
)

monitor = pf.Monitor()
pf.initialise(monitor)

# tolerance in eV
tolerance = 0.5e3
desired_energy = 511e3
zais = []
energies = []
intensities = []
with pp.PrintLib5Reader(filename) as output:
    for m in output.spectral_data:
        if m.type == "gamma":
            for l in m.lines:
                if abs(l[0] - desired_energy) < tolerance:
                    zais.append(m.zai)
                    energies.append(l[0] * 1e-3)
                    intensities.append(l[2] * l[4])

# intensity threshold
threshold = 1e-5
for i in range(len(zais)):
    if intensities[i] > threshold:
        print(
            "{} @ {:.1f} keV with {:.3e}".format(
                pf.util.nuclide_from_zai(monitor, zais[i]), energies[i], intensities[i]
            )
        )

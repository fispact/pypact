#!/usr/bin/env python3

import os
import pypact as pp


name_spectrum = '1102_PWR-MOX-40'

newgroup = 709
newenergies = list(reversed(pp.ALL_GROUPS[newgroup]))
newvalues = []
with pp.SpectrumLibJSONReader() as lib:
    manager = pp.SpectrumLibManager(lib)
    energies, values = manager.get(name_spectrum)
    newvalues = pp.groupconvert.by_lethargy(
        energies, values, newenergies)

flux = pp.FluxesFile(name=f"{name_spectrum}_convertedto{newgroup}", norm=1.0)
flux.setGroup(newgroup)
flux.values = newvalues
flux.validate()

pp.to_file(flux, 'fluxes')



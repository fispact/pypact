#!/usr/bin/env python3

import os
import pypact as pp


# fluxes file
# set monoenergetic flux at 14 MeV for group 709
flux = pp.FluxesFile(name="14 MeV (almost) monoenergetic", norm=1.0)
flux.setGroup(709)

# set values at energies 12, 13 and 14 MeV
flux.setValue(12.0e6, 0.1)
flux.setValue(13.0e6, 0.4)
flux.setValue(14.0e6, 1.0)

# validate the data
flux.validate()

pp.to_file(flux, os.path.join('files', 'fluxes'))



#!/usr/bin/env python3

import os
import pypact as pp


name_spectrum = "1102_PWR-MOX-40"
newgroup = 709

with pp.SpectrumLibJSONReader() as lib:
    manager = pp.SpectrumLibManager(lib)
    energies, newvalues = manager.get_and_convert(name_spectrum, group=newgroup)

    ff = pp.FluxesFile(name=f"{name_spectrum}_convertedto{newgroup}", norm=1.0)
    ff.setGroup(newgroup)
    ff.values = newvalues
    ff.validate()

    pp.to_file(ff, os.path.join("files", "newfilesfile"))

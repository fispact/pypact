#!/usr/bin/env python3

import os
import pypact as pp


runname = 'test'
id = pp.InputData(name=runname)

# control setup
id.overwriteExisting()
id.enableJSON()
id.approxGammaSpectrum()
id.doCollapse(709)
id.doCondense()
id.enableHalflifeInOutput()
id.enableHazardsInOutput()
id.setProjectile(pp.PROJECTILE_NEUTRON)
id.enableSystemMonitor()
id.readGammaGroup()
id.enableInitialInventoryInOutput()
id.setLogLevel(pp.LOG_SEVERITY_ERROR)

# thresholds
id.setXSThreshold(1e-12)
id.setAtomsThreshold(1e5)

# set target
id.setDensity(19.5)
id.setMass(1.0)
id.addElement('Ti', percentage=80.0)
id.addElement('Fe', percentage=14.8)
id.addElement('Cr', percentage=5.2)

# irradiate and cooling times
id.addIrradiation(300.0, 1.1e15)
id.addCooling(10.0)
id.addCooling(100.0)
id.addCooling(1000.0)
id.addCooling(10000.0)
id.addCooling(100000.0)

# validate data
id.validate()

# write to file
pp.serialize(id, os.path.join('files', '{}.i'.format(runname)))

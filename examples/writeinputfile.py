#!/usr/bin/env python3

import os
import pypact as pp


id = pp.InputData(name='test')

# control setup
id.overwriteExisting()
id.enableJSON()
id.approxGammaSpectrum()
id.readXSData(709)
id.readDecayData()
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

#print(pp.to_string(id))

# write to file
pp.to_file(id, os.path.join('files', '{}.i'.format(id.name)))

import pypact as pp

runname = 'test'
id = pp.InputData(name=runname)

# control setup
id.overwriteExisting()
id.enableJSON()
id.approxGammaSpectrum()
id.collapse(709)
id.condense()
id.outputHalflife()
id.outputHazards()
id.useNeutron()
id.enableMonitor()
id.readGammaGroup()
id.outputInitialInventory()
id.setLogLevel(pp.LOG_SEVERITY_ERROR)

# thresholds
id.setXSThreshold(1e-12)
id.setAtomsThreshold(1e5)

# set target
id.setDensity(19.5)
id.setMass(1.0)
id.addElement('Ti', percentage=80.0)
id.addElement('Fe', percentage=20.0)
id.addElement('Cr', percentage=5.2)

# write to file
pp.serialize(id, '{}.i'.format(runname))

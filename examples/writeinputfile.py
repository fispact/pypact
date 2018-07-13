import pypact as pp

runname = 'test'
id = pp.InputData(name=runname)

id.overwriteExisting()
id.enableJSON()
id.approxGammaSpectrum()
id.collapse(709)
id.condense()
id.useNeutron()

# write to file
pp.serialize(id, '{}.i'.format(runname))

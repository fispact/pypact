import os
import pypact as pp

filename = "files"
base_dir = os.path.join(os.sep, 'opt', 'fispact', 'nuclear_data')

# write a files file
ff = pp.FilesFile(base_dir=base_dir)

ff.setXS('TENDL2017')
ff.setFissionYield('GEFY52')
ff.setProbTab('TENDL2015')
ff.setDecay('DECAY')
ff.setRegulatory('DECAY')
ff.setGammaAbsorb('DECAY')

pp.serialize(ff, filename)


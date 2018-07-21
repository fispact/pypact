#!/usr/bin/env python3

import os
import pypact as pp


base_dir = os.getenv('NUCLEAR_DATA', os.path.join(os.sep, 'opt', 'fispact', 'nuclear_data'))

# write a files file
ff = pp.FilesFile(base_dir=base_dir)

ff.setXS('TENDL2017')
ff.setFissionYield('GEFY52')
ff.setProbTab('TENDL2015')
ff.setDecay('DECAY')
ff.setRegulatory('DECAY')
ff.setGammaAbsorb('DECAY')

pp.serialize(ff, "files")


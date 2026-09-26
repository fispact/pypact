#!/usr/bin/env python3

import os
import pypact as pp
import pypact.analysis as ppa
from pypact.library.nuclidelib import get_zai

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'reference', 'second_modif.out')

tz = ppa.TimeZone.BOTH
properties = ['atoms']

# plot all isotopes of a specific element regardless of state, here I
isotopes = [ ppa.NuclideDataEntry(i) for i in ppa.get_all_isotopes() if ppa.find_z(i[0]) > 89]

# plot specific isotope with specific state, here Sc45m
# isotopes = [ ppa.NuclideDataEntry(i) for i in ppa.get_all_isotopes_states() if get_zai(i[0]+str(i[1])+str(i[2])) == 210451 ]

# plot all isotopes and states of an element, here Sc
# isotopes = [ ppa.NuclideDataEntry(i) for i in ppa.get_all_isotopes_states() ]


plt = ppa.LinePlotAdapter()

with pp.Reader(filename) as output:
    for p in properties:
        ppa.plotproperty(output=output,
                         property=p,
                         isotopes=isotopes,
                         plotter=plt,
                         fractional=False,
                         timeperiod=tz)

plt.show()
plt.savefig("graph_01.png")
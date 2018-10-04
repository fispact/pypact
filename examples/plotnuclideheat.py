#!/usr/bin/env python3

import os
import pypact as pp
import pypact.analysis as ppa

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test127.out')

tz = ppa.TimeZone.COOL
properties = ['heat', 'grams', 'ingestion']
isotopes = [ ppa.NuclideDataEntry(i) for i in ppa.getallisotopes() if ppa.findZ(i[0]) <= 10]

plt = ppa.LinePlotAdapter()

with pp.Reader(filename) as output:
    for p in properties:
        ppa.plotproperty(output=output,
                         property=p,
                         isotopes=isotopes,
                         plotter=plt,
                         fractional=True,
                         timeperiod=tz)

plt.show()

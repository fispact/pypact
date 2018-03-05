#!/usr/bin/env python3

import os

from pypact.analysis.propertyplotter import plotproperty
from pypact.analysis.propertyplotter import NuclideDataEntry
from pypact.analysis.plotadapter import LinePlotAdapter
from pypact.analysis.timezone import TimeZone
from pypact.library.nuclidelib import getallisotopes
from pypact.library.nuclidelib import findZ
from pypact.reader import Reader

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test127.out')

tz = TimeZone.COOL
properties = ['heat', 'grams', 'ingestion']
isotopes = [ NuclideDataEntry(i) for i in getallisotopes() if findZ(i[0]) <= 10]

plt = LinePlotAdapter()

with Reader(filename) as output:
    for p in properties:
        plotproperty(output=output,
                     property=p,
                     isotopes=isotopes,
                     plotter=plt,
                     fractional=True,
                     timeperiod=tz)

plt.show()

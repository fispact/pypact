#!/usr/bin/env python3

import os

from pypact.analysis.propertyplotter import plotproperty
from pypact.analysis.propertyplotter import NuclideDataEntry
from pypact.analysis.matplotlibengine import MatplotLibPlotEngine
from pypact.analysis.timezone import TimeZone
from pypact.library.nuclidelib import getallisotopes
from pypact.library.nuclidelib import findZ
from pypact.reader import Reader

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test127.out')

fispact_output = Reader()(filename)

plt = MatplotLibPlotEngine()
tz = TimeZone.COOL

isotopes = [ NuclideDataEntry(i) for i in getallisotopes() if findZ(i[0]) <= 10]

properties = ['heat', 'grams', 'ingestion']
for p in properties:
    plotproperty(output=fispact_output,
                 property=p,
                 isotopes=isotopes,
                 engine=plt,
                 fractional=True,
                 timeperiod=tz)

plt.show()

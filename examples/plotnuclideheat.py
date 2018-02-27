#!/usr/bin/env python3

import os

from pypact.reader import Reader
from pypact.analysis.plotter import Entry, plotproperty, showplots
from pypact.analysis.timezone import TimeZone
from pypact.library.nuclidelib import getallisotopes

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test127.out')

o = Reader()(filename)

# plot for cooling time only
timeperiod=TimeZone.COOL
isotopes_with_low_A = [Entry(i) for i in getallisotopes() if i[1] <= 40]
plotproperty(output=o, isotopes=isotopes_with_low_A, prop='heat', fractional=True, timeperiod=timeperiod)

# show the plots
showplots()

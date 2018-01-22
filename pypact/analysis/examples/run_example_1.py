import re
from pypact.reader.filerecord import FileRecord
from pypact.output.output import Output
from pypact.analysis.plotter import Entry, plotproperty, showplots
from pypact.analysis.timezone import TimeZone
from pypact.library.nuclidelib import getallisotopes

# script starts here
filename = 'pypact/reference/test127.out'
o = Output()
o.fispact_deserialize(FileRecord(filename))

isotopes_with_low_A = [Entry(i) for i in getallisotopes() if i[1] <= 20]
all_isotopes = [Entry(i) for i in getallisotopes()]
only_isotopes_with_C_in_name = [Entry(i) for i in getallisotopes() if re.search("C", i[0], re.IGNORECASE) ]

# plot for cooling time only
timeperiod=TimeZone.COOL
plotproperty(output=o, isotopes=isotopes_with_low_A, prop='grams', fractional=True, timeperiod=timeperiod)
plotproperty(output=o, isotopes=all_isotopes, prop='heat', fractional=True, timeperiod=timeperiod)
plotproperty(output=o, isotopes=only_isotopes_with_C_in_name, prop='ingestion', fractional=True, timeperiod=timeperiod)

# show the plots
showplots()

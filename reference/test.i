<< CONTROL PHASE >>
<< enable JSON output >>
JSON 
<< overwrite existing output files of same name >>
CLOBBER 
<< read gamma groups from file, specify ggbins in files file >>
READGG 
<< monitor FISPACT-II progress >>
MONITOR 1
<< the minimum cross section (barns) for inclusion in pathways analysis >>
XSTHRESHOLD 1e-12
<< perform collapse >>
GETXS 1 709
<< get decay data >>
GETDECAY 1
<< enable logging at level 1 >>
LOGLEVEL 1
<< approximate spectra when not available >>
SPEK 
<< end control >>
FISPACT 
* test

<< INITIALIZATION PHASE >>
<< output half life values >>
HALF 
<< output ingestion and inhalation values >>
HAZARDS 
<< set the target via MASS >>
MASS 1.0 3
Ti 80.0
Fe 14.8
Cr 5.2 
<< set the target density >>
DENSITY 19.5
<< set the threshold for atoms in the inventory >>
MIND 100000.0
<< output the initial inventory >>
ATOMS 

<< INVENTORY PHASE >>
<< irradiation schedule >>
FLUX 1100000000000000.0
TIME 300.0 SECS
FLUX 42.0
TIME 200.0 SECS
ATOMS 
<< end of irradiation >>
FLUX 0.0
ZERO 
TIME 10.0 SECS
ATOMS 
TIME 100.0 SECS
ATOMS 
TIME 1000.0 SECS
ATOMS 
TIME 10000.0 SECS
ATOMS 
TIME 100000.0 SECS
ATOMS 
<< end of cooling >>

<< end of input >>
END 
* end

MONITOR 1
<< Overwrite existing inventory.log and inventory.out files >>
CLOBBER
<< Enable JSON file format output for inventory data >>
JSON
<< Read ARRAYX and COLLAPX files >>
GETXS 1 709
GETDECAY 1
<< Read gamma bounds from file >>
READGG
<< End of control >>
FISPACT
* FNS 5 Minutes Inconel-600
<< Material definition - start of initialisation phase >>
<< Density is in units of g/cm3 >>
DENSITY 8.42
<< Elemental definition of material >>
<< total mass = 1g, with 4 elements>>
MASS 1.0E-3 4
<< Nickel at 75.82%>>
NI  75.82
<< Manganese at 0.39%>>
MN   0.39
<< Iron at 7.82%>>
FE   7.82
<< Chromium at 15.97%>>
CR  15.97
<< Set the minimum number of atoms to track - 1000 atom threshold>>
<< 1e5 atoms is the default >>
MIND 1E3
<< Produce some graph files for GNU plot for post processing >>
<< from left to right: 1 graph, 2= .gra and .plt for gnuplot, 1=use uncertainties, 3=total heat output>>
GRAPH 1 2 1 3
<< Output estimates of both uncertainty and pathway analysis >>
UNCERTAINTY 2
<< Output half lives to output inventory information >>
HALF
<< Output ingestion and inhalation doses to output >>
HAZARDS
<< Signify start of inventory phase >>
<< -----irradiation phase----- >>
<< Flux amplitude in /cm2 /s >>
FLUX 1.116E+10
<< ATOMS= tells F-II to solve rate equations and dump output to file >>
<< No time is given so it will use 0.0 (initial) >>
ATOMS
<< Solve and output at 5 minutes of irradiation>>
TIME 5.0 MINS
ATOMS
<< -----cooling phase----- >>
<< Set flux to 0 to tell F-II that no irradiation is occuring and it is decay only >>
FLUX 0.
<< Whilst it is possible to irradiate again FLUX >0, ZERO tells F-II that no more irradiation can occur >> 
<< From here on only cooling can happen - this keyword is important for pathways analysis>>
ZERO
<< Cooling time - note use of ATOMS to indicate solving and output >>
<< we could also use STEP or SPECTRUM to reduce output>>
<< Default time unit is seconds, these are all in seconds >> 
TIME    36 ATOMS
TIME    15 ATOMS
TIME    16 ATOMS
TIME    15 ATOMS
TIME    15 ATOMS
TIME    26 ATOMS
TIME    33 ATOMS
TIME    36 ATOMS
TIME    53 ATOMS
TIME    66 ATOMS
TIME    66 ATOMS
TIME    97 ATOMS
TIME   127 ATOMS
TIME   126 ATOMS
TIME   187 ATOMS
TIME   246 ATOMS
TIME   244 ATOMS
TIME   246 ATOMS
TIME   428 ATOMS
TIME   606 ATOMS
TIME   607 ATOMS
<< End of file >>
END
* END

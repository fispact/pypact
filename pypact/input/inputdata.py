import os

from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactOutOfRangeException
from pypact.util.exceptions import PypactInvalidOptionException
from pypact.util.exceptions import PypactIncompatibleOptionException
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.loglevels import *
from pypact.library.projectiles import PROJECTILE_NEUTRON, VALID_PROJECTILES
from pypact.input.keywords import CONTROL_KEYWORDS, INIT_KEYWORDS, INVENTORY_KEYWORDS

COMMENT_START = '<<'
COMMENT_END   = '>>'

class InventoryType(JSONSerializable):
    def __init__(self, precision=10):
        # a list of tuples, the first entry is the element/nuclide symbol
        # the second is the value
        self.entries = []
        self._prec = precision


@freeze_it
class MassInventory(InventoryType):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        # the total mass in kg
        self.totalMass = 0.0

    def __str__(self):
        strrep = "{} {} {}".format('MASS', self.totalMass, len(self.entries))
        for e in self.entries:
            strrep += f"\n{e[0]} {e[1]:.{self._prec}E}".format(e[0], e[1])

        return strrep


@freeze_it
class FuelInventory(InventoryType):
    def __str__(self):
        strrep = f"FUEL {len(self.entries)}"
        for i in self.entries:
            strrep += f"\n{i[0]} {i[1]:.{self._prec}E}"
        return strrep   

@freeze_it
class SSFFuelInventory(InventoryType):
    def __str__(self):
        strrep = f"SSFFUEL {len(self.entries)}"
        for i in self.entries:
            strrep += f"\n{i[0]} {i[1]:.{self._prec}E}"
        return strrep  



@freeze_it
class InputData(JSONSerializable):

    def __init__(self, name: str = "run", precision = 10):
        """
            Constructor
            
            Initialises all input data
        """
        self.name= name
        self._prec = precision
        
        self._overwrite             = False
        self._json                  = False
        self._ignorecollapse        = True
        self._ignorecondense        = True
        self._condense              = False
        self._binaryxs              = False
        self._useeaf                = False
        self._approxgamma           = False
        self._outputhalflife        = False
        self._outputhazards         = False
        self._initialinventory      = False
        self._readgammagroup        = False
        self._readspontfission      = False
        self._ignoreuncert          = False
        self._enablemonitor         = False
        self._usecumfissyield       = False
        self._usefissyield          = False
        self._clearancedata         = False
        self._loglevel              = LOG_SEVERITY_WARNING
        self._probtable             = False
        self._SSFgeometry           = False
        self._SSFchoose             = False
        self._SSFnuclides           = []
        self._FYactinides           = []
        self._FYactinidesoptions    = -2
        self._SSFfuel               = False
        self._usefission            = False
        self._fisyield              = False
        self._tolerance             = False
        self._tolerance_pathway     = False
        self._itol                  = 0  # inventory
        self._atol                  = 1E4  # default
        self._rtol                  = 2E-3 # default
        self._itol2                 = 1  # pathway
        self._atol2                 = 1E4  # default
        self._rtol2                 = 2E-3 # default
        self._tab1                  = False
        self._uncertainty           = False
        self._unctype               = False
        self._lookahead             = False
        self._nucgraph              = False
        self._graph                 = False
        self._geom_type             = 2 # wire as default for SSFGeometry
        self._len1                  = 0.0 # default length 1 in cm
        self._printlib4             = False
        self._fullxs                = False
        self._sortdominant          = False
        self._topcount              = 20 # Default are top 20
        
        self._depletion_unc         = False
        self._depletion_nucs        = []
        
        # default is 1.0E-12 barns
        self._xsthreshold           = 1.0e-12
        self._group                 = 0
        self._projectile            = PROJECTILE_NEUTRON

        # set the minimum number of atoms deemed significant for the inventory output
        self._atomsthreshold       = 0.0
        
        # the total mass in grams per cubic centimetre (g/cc)
        self._density              = 0.0

        self._inventoryismass      = False
        self._inventoryisfuel      = False 
        
        self._inventorymass        = MassInventory(precision=precision)
        self._inventoryfuel        = FuelInventory(precision=precision)
        self._inventoryssffuel     = SSFFuelInventory(precision=precision)
    
        # irradiation schedule
        # a list of tuples of (time interval in seconds, flux amplitude)
        self._irradschedule = []

        # power schedule
        # a list of tuples of (time interval in seconds, power amplitude)
        self._powerschedule = []
        
        # cooling schedule
        # a list of time interval in seconds
        self._coolingschedule = []
    
    def reset(self):
        """
            Reset the data
            
            Reinitialises all input data to defaults
        """
        self.__init__(self.name)

    def validate(self):
        """
            Validate the input data
            
            Not implemented yet
        """
        # to do
        pass

    def overwriteExisting(self, overwrite = True):
        """
            Enables overwriting of output files
            uses keyword CLOBBER
        """
        self._overwrite = overwrite

    def enableJSON(self, enable = True):
        """
            Enables JSON output file
            uses keyword JSON
        """
        self._json = enable

    def enableFullXS(self, enable = True):  
        """  
            Enables full cross-section output  
            uses keyword FULLXS  
        """  
        self._fullxs = enable

   
    def enableInitialInventoryInOutput(self, output = True):
        """
            Performs the time = 0, inventory step,
            the initial inventory
        """
        self._initialinventory = output
    
    def enableHalflifeInOutput(self, output = True):
        """
            Enables half lives to be written to the output file
        """
        self._outputhalflife = output
    
    def enableHazardsInOutput(self, output = True):
        self._outputhazards = output
    
    def readXSData(self, group, binary = False):
        if self._useeaf and binary:
            raise PypactIncompatibleOptionException("Cannot enable binary format reading when using EAF")

        self._ignorecollapse = False
        self._group = group
        self._binaryxs = binary
    
    def useEAFLibraries(self, use = True):
        if self._binaryxs and use:
            raise PypactIncompatibleOptionException("Cannot enable EAF data libraries with binary format")

        self._useeaf = use
    
    def useCumulativeFissionYieldData(self, use = True):
        self._usecumfissyield = use

    def useFissionYieldData(self, use = True):
        self._usefissyield = use
    
    def includeClearanceData(self, include = True):
        self._clearancedata = include
    
    def readDecayData(self, condense = True):
        self._ignorecondense = False
        self._condense = condense
    
    def approxGammaSpectrum(self, approxgamma = True):
        self._approxgamma = approxgamma
    
    def ignoreUncertainties(self, ignore = True):
        self._ignoreuncert = ignore
    
    def setXSThreshold(self, threshold):
        self._xsthreshold = threshold
    
    def setProjectile(self, proj):
        if proj not in VALID_PROJECTILES:
            raise PypactInvalidOptionException("{} is not a valid projectile option.")
            
        self._projectile = proj

    def readGammaGroup(self, readgg = True):
        self._readgammagroup = readgg
    
    def enableSystemMonitor(self, enable = True):
        self._enablemonitor = enable

    def setAtomsThreshold(self, threshold):
        self._atomsthreshold = threshold
    
    def addIrradiation(self, timeInSecs, fluxAmp):
        self._irradschedule.append((timeInSecs, fluxAmp))
    
    def resetIrradiation(self):
        self._irradschedule = []

    def addPower(self, timeInSecs, powerAmp):
        self._powerschedule.append((timeInSecs, powerAmp))
    
    def resetPower(self):
        self._powerschedule = []

    def includeProbtable(self):
        self._probtable = True

    def includeSSFgeometry(self, geom_type, len1): # only for wire geometry
        self._SSFgeometry = True
        self._geom_type = geom_type
        self._len1 = len1
        

    def includeSSFchoose(self, SSFnuclides:[]):
        """Sets nuclides for self-shielding.

        Arguments
        -----------

        SSFnuclides: [str]
             Only valid nuclides are allowed, format 'U238'
        """
        self._SSFchoose = True
        for x in SSFnuclides:
            self._SSFnuclides.append(x)
    
    def includeSSFfuel(self):
        self._SSFfuel = True

    def includeSortDominant(self, top_count):
        self._sortdominant = True
        self._topcount = top_count

    def includeDepletion(self, depletion_nucs:[]):
        self._depletion_unc = True
        for x in depletion_nucs:
            self._depletion_nucs.append(x)

    def includeFisyield(self, option, FYActinides:[]):
        self._fisyield = True
        self._FYactinidesoptions = option
        for x in FYActinides:
            self._FYactinides.append(x)

    def includeUsefission(self):
        self._usefission = True

    def includeTolerance(self, itol, atol, rtol):
        self._tolerance = True
        self._itol = itol
        self._atol = atol
        self._rtol = rtol

    def includeTolerance_pathway(self, itol2, atol2, rtol2):
        self._tolerance_pathway = True
        self._itol2 = itol2
        self._atol2 = atol2
        self._rtol2 = rtol2
    
    def includeTab1(self):
        self._tab1 = True

    def includeUncertainty(self):
        self._uncertainty = True

    def includeUnctype(self):
        self._unctype = True

    def includeLookahead(self):
        self._lookahead = True

    def includeNucgraph(self):
        self._nucgraph = True

    def includeGraph(self):
        self._graph = True

    def includePrintlib4(self):
        self._printlib4 = True
    
    def addCooling(self, timeInSecs):
        self._coolingschedule.append(timeInSecs)
    
    def resetCooling(self):
        self._coolingschedule = []
    
    def setLogLevel(self, severity):
        if severity < LOG_SEVERITY_FATAL or severity > LOG_SEVERITY_TRACE:
            raise PypactOutOfRangeException("Log level {} not valid.".format(severity))
        self._loglevel = severity

    def setDensity(self, densityInGPCC):
        """
            Sets the density of the target in g/cc
            densityInGPCC: density in g/cc, must be positive
        """
        if not densityInGPCC > 0.0:
            raise PypactOutOfRangeException("Density must be positive.")

        self._density = densityInGPCC

    def setMass(self, totalMassInKg):
        """
            Sets the material mode to Mass
            Sets the total mass of the target in kg
            totalMassInKg: mass in kg, must be positive
        """
        if not totalMassInKg > 0.0:
            raise PypactOutOfRangeException("Total mass must be positive.")

        self._inventorymass.totalMass = totalMassInKg
        self._inventoryismass = True
        self._inventoryisfuel = False

    def setFuel(self):
        """
            Sets the material mode to Fuel
        """

        self._inventoryismass = False
        self._inventoryisfuel = True

    def addIsotope(self, isotope: str, numberOfAtoms):
        """
            Add an isotope
            isotope: character symbol of element name, e.g. 'Fe' and the mass number of the isotpe e.g '56'
            numberOfAtoms: the number of atoms present 
        """
        if numberOfAtoms < 0:
            raise PypactUnphysicalValueException("Number of atoms must be positive")
        #could check for integer value and raise here PypactTypeException
        
        self._inventoryfuel.entries.append((isotope, numberOfAtoms))

    def clearIsotopes(self):
        self._inventoryfuel.entries = []
        
    def addSSFIsotope(self, isotope: str, numberOfAtoms):
        """
            Add an SSF isotope
            SSF isotope: character symbol of element name, e.g. 'Fe' and the mass number of the isotpe e.g '56'
            numberOfAtoms: the number of atoms present 
        """
        if numberOfAtoms < 0:
            raise PypactUnphysicalValueException("Number of atoms must be positive")
        #could check for integer value and raise here PypactTypeException
        
        self._inventoryssffuel.entries.append((isotope, numberOfAtoms))

    def clearIsotopes(self):
        self._inventoryssffuel.entries = []


    def addElement(self, element, percentage = 100.0):
        """
            Add an element
            element: character symbol of element name, e.g. 'Fe'
            percentage: percentage contribution of total mass, should not exceed 100%
        """
        if percentage > 100.0:
            raise PypactOutOfRangeException("Cannot set the element percentage above 100%.")
        
        self._inventorymass.entries.append((element, percentage))
        
    def clearElements(self):
        self._inventorymass.entries = []
    
    def _serialize(self, f):
        """
            The serialization method
            f: file object
        """
        inputdata = []
        
        def addnewline():
            inputdata.append("")
        
        def addcomment(comment):
            inputdata.append(f"{COMMENT_START} {comment} {COMMENT_END}")
        
        def addkeyword(keyword, args=[]):
            strargs = ' '.join([str(a) for a in args])
            inputdata.append(f"{keyword} {strargs}")
        
        # control keywords
        addcomment("CONTROL PHASE")
        if self._json:
            addcomment("enable JSON output")
            addkeyword('JSON')

        if self._fullxs:  
            addcomment("enable full cross-section output")        
            addkeyword('FULLXS')
                
        if self._overwrite:
            addcomment("overwrite existing output files of same name")
            addkeyword('CLOBBER')
        
        if self._readgammagroup:
            addcomment("read gamma groups from file, specify ggbins in files file")
            addkeyword('READGG')
        
        if self._readspontfission:
            addcomment("read spontaneous fission from file, specify sf_endf in files file")
            addkeyword('READSF')
        
        if self._useeaf:
            addcomment("use EAF nuclear data libraries")
            addkeyword('LIBVERSION', args=[0])
        
        if self._usecumfissyield:
            addcomment("use cumulative fission yield data mt=459 instead of mt=454")
            addkeyword('CUMFYLD')

        if self._usefissyield:
            addcomment("use fission data")
            addkeyword('USEFISSION')
            
        if self._enablemonitor:
            addcomment("monitor FISPACT-II progress")
            addkeyword('MONITOR', args=[1])
        
        addcomment("the minimum cross section (barns) for inclusion in pathways analysis")
        addkeyword('XSTHRESHOLD', args=[self._xsthreshold])
        
        if self._ignorecollapse:
            addcomment("collapse ignored, just read the existing file")
            addkeyword('GETXS', args=[0])
        else:
            if self._group != 0:
                addcomment("perform collapse")
                addkeyword('GETXS', args=[-1 if self._binaryxs and not self._useeaf else 1, self._group])
            else:
                addcomment("no group specified, just read the existing file")
                addkeyword('GETXS', args=[0])


        if self._ignorecondense or not self._condense:
            addkeyword('GETDECAY', args=[0])
        else:
            addcomment("get decay data")
            addkeyword('GETDECAY', args=[1])

    
        if self._loglevel != LOG_SEVERITY_WARNING:
            addcomment("enable logging at level {}".format(self._loglevel))
            addkeyword('LOGLEVEL', args=[self._loglevel])

        if self._approxgamma:
            addcomment("approximate spectra when not available")
            addkeyword('SPEK')
        
        if self._ignoreuncert:
            addcomment("ignore uncertainties")
            addkeyword('NOERROR')
    
        if self._projectile != PROJECTILE_NEUTRON:
            addcomment("set projectile (n=1, d=2, p=3, a=4, g=5)")
            addkeyword('PROJ', args=[self._projectile])

        if self._probtable:
            addcomment("energy self-shielding default")
            addkeyword('PROBTABLE', args=[0,1])

        if self._SSFgeometry:
            addcomment("geometry self-shielding (wire as default)")
            addkeyword('SSFGEOMETRY', args=[self._geom_type, self._len1])
            #addkeyword('SSFGEOMETRY', args=[1,0.0711]) # foil with thickness     
            #addkeyword('SSFGEOMETRY', args=[1,0.0711/2]) # foil with thickness/2 
            #addkeyword('SSFGEOMETRY', args=[1,0.0711*2]) # foil with thickness*2
            #addkeyword('SSFGEOMETRY', args=[1,0.0711*100]) # foil with thickness*100
            #addkeyword('SSFGEOMETRY', args=[2,0.0711/10]) # wire with thickness d/10 as radius
            #addkeyword('SSFGEOMETRY', args=[2,0.0711/2]) # wire with 1/2*thickness d as radius
            #addkeyword('SSFGEOMETRY', args=[2,0.0711]) # wire with thickness d as radius
            

        if self._SSFchoose:
            addcomment("nuclides for energy self-shielding")
            addkeyword('SSFCHOOSE', args=[len(self._SSFnuclides), 1])
            addkeyword("\n".join([str(a) for a in self._SSFnuclides]))
        
        if self._SSFfuel:
            addcomment("ssf nuclides concentrations from previous run")
            addkeyword(str(self._inventoryssffuel))

        # end control phase
        addcomment("end control")
        addkeyword('FISPACT')
        addkeyword('*', args=[self.name])

        # initial phase
        addnewline()
        addcomment("INITIALIZATION PHASE")

        if self._depletion_unc:
            addkeyword('DEPLETION', args=[len(self._depletion_nucs)])
            addkeyword("\n".join([str(a) for a in self._depletion_nucs]))

        if self._sortdominant:
            addkeyword('SORTDOMINANT', args=[self._topcount, self._topcount])
        
        if self._printlib4:
            addcomment("print out the collapsed 1-g XS for the spectrum")
            addkeyword('PRINTLIB', args=[4])
        
        if self._outputhalflife:
            addcomment("output half life values")
            addkeyword('HALF')

        if self._outputhazards:
            addcomment("output ingestion and inhalation values")
            addkeyword('HAZARDS')

        if self._clearancedata:
            addcomment("include clearance data of radionuclides to be input")
            addkeyword('CLEAR')
            
        if self._inventoryismass and not self._inventoryisfuel:
            if self._inventorymass.totalMass > 0.0:
                addcomment("set the target via MASS")
                addkeyword(str(self._inventorymass))

        if self._inventoryisfuel and not self._inventoryismass:
            if self._density > 0.0:
                addcomment("set the target via FUEL")
                addkeyword(str(self._inventoryfuel))  
        
        if self._density > 0.0:
            addcomment("set the target density")
            addkeyword('DENSITY', args=[self._density])
        
        if self._atomsthreshold > 0.0:
            addcomment("set the threshold for atoms in the inventory")
            addkeyword('MIND', args=[self._atomsthreshold])

        if self._usefission:
            addcomment("use fission")
            addkeyword('USEFISSION')
        
        if self._fisyield:
            addcomment("isotopes for fission yield")
            addkeyword('FISYIELD', args=[self._FYactinidesoptions])
            addkeyword("\n".join([str(a) for a in self._FYactinides]))
            #addkeyword('FISYIELD', args=[self._FYactinidesoptions, "\n".join([str(a) for a in self._FYactinides])])

        if self._tolerance:
            addcomment("tolerance settings itol, atol , rtol")
            addkeyword('TOLERANCE', args=[self._itol, self._atol, self._rtol])

        if self._tolerance_pathway:
            addcomment("tolerance pathway settings itol, atol , rtol")
            addkeyword('TOLERANCE', args=[self._itol2, self._atol2, self._rtol2])

        if self._tab1:
            addcomment('natoms output for next run')
            addkeyword('TAB1', args=[21])

        if self._uncertainty:
            addcomment('uncertainty and the info')
            #addkeyword('UNCERTAINTY', args=[-1, 0.01, 0.01, 5, 2])
            addkeyword('UNCERTAINTY', args=[-1, 0.01, 0.01, 10, 2]) # default by FP
            #addkeyword('UNCERTAINTY', args=[-1, 0.0005, 0.001, 50, 2]) # my default setting

        if self._unctype:
            addcomment('3 --> xs and t12 uncertainties')
            addkeyword('UNCTYPE', args=[3])

        if self._lookahead:
            addcomment("Adding late-time nucs to dominant")
            addkeyword('LOOKAHEAD')         
        
        if self._nucgraph:
            addcomment('No graphs, cutof for dom nuc 10%, inc. uncert., graph types')
            addkeyword('NUCGRAPH', args=[7, 0.1, 1, 1, 2, 3, 4, 5, 6, 7])

        if self._graph:
            addcomment('No graphs, output type, include uncert, graph types')
            addkeyword('GRAPH', args=[7, 2, 1, 1, 2, 3, 4, 5, 6, 7])
                
        if self._initialinventory:
            addcomment("output the initial inventory")
            addkeyword('ATOMS')

        # inventory phase
        addnewline()
        addcomment("INVENTORY PHASE")
        # flux plus cooling
        if len(self._irradschedule) > 0:
            addcomment("irradiation schedule")
            for i, (time, fluxamp) in enumerate(self._irradschedule):
                
                #The first GETXS 0 is called in the control phase preceding to 'FISPACT' 
                # if self._ignorecollapse and i > 0:
                #     addkeyword('GETXS', args=[0])

                addkeyword('FLUX', args=[f"{fluxamp:.{self._prec}E}"])
                addkeyword('TIME', args=[f"{time:.{self._prec}E}", 'SECS'])
                addkeyword('ATOMS')

            addcomment("end of irradiation")

            addkeyword('FLUX', args=[0.])
            addkeyword('ZERO')
            for time in self._coolingschedule:
                
                # Note sure this is needed for cooling
                # if self._ignorecollapse:
                #     addkeyword('GETXS', args=[0])
                    
                addkeyword('TIME', args=[f"{time:.{self._prec}E}", 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of cooling")
       
        # power plus cooling
        if len(self._powerschedule) > 0:
            addcomment("power schedule")
            for time, poweramp in self._powerschedule:
                addkeyword('POWER', args=[f"{poweramp:.{self._prec}E} 1 301"])
                addkeyword('TIME', args=[f"{time:.{self._prec}E}", 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of power")

            addkeyword('FLUX', args=[0.])
            addkeyword('ZERO')
            for time in self._coolingschedule:
                addkeyword('TIME', args=[f"{time:.{self._prec}E}", 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of cooling")

 
        # Cooling only run, if any of schedule not 0 they are caught above already
        if (len(self._irradschedule) == 0 and len(self._powerschedule) == 0):
            addcomment("cooling schedule only")
            for time in self._coolingschedule:
                addkeyword('TIME', args=[f"{time:.{self._prec}E}", 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of cooling")

        # end file
        addnewline()
        addcomment("end of input")
        addkeyword('END')
        addkeyword('*', args=['end'])
        
        for line in inputdata:
            f.write("{}\n".format(line))

    def _deserialize(self, f):
        """
            The deserialization method
            f: file object
        """
        self.reset()

        lines = iter(f.readlines())  # Convert lines to an iterator
        in_mass_section = False
        irradiation_active = True  # Flag to track if irradiation schedule is active
        flux_set = False  # Flag to ensure FLUX is set to a non-zero value before the first irradiation step

        time_unit_to_seconds = {
            "SECS": 1,
            "MINS": 60,
            "HOURS": 3600,
            "DAYS": 86400,
            "YEARS": 31536000
        }

        for line in lines:
            line = line.strip()
            if line.startswith("MASS"):
                # Parse the MASS line
                parts = line.split()
                if len(parts) != 3:
                    raise PypactInvalidOptionException("Invalid MASS line format.")
                self.setMass(float(parts[1]))
                num_elements = int(parts[2])
                in_mass_section = True
                continue

            if in_mass_section:
                # Parse the elements following the MASS line
                if len(line.split()) == 2:
                    element, percentage = line.split()
                    self.addElement(element, float(percentage))
                    num_elements -= 1
                    if num_elements == 0:
                        in_mass_section = False
                else:
                    if line.startswith(COMMENT_START) and line.endswith(COMMENT_END):
                        # Ignore comments
                        continue
                    raise PypactInvalidOptionException("Invalid element line format in MASS section.")

            elif line.startswith("DENSITY"):
                parts = line.split()
                if len(parts) != 2:
                    raise PypactInvalidOptionException("Invalid DENSITY line format.")
                self.setDensity(float(parts[1]))

            elif line.startswith("FLUX") and irradiation_active:
                # Parse the FLUX line
                parts = line.split()
                if len(parts) != 2:
                    raise PypactInvalidOptionException("Invalid FLUX line format.")
                fluxAmp = float(parts[1])

                # Ensure FLUX is set to a non-zero value before the first irradiation step
                if not flux_set and fluxAmp <= 0.0:
                    raise PypactInvalidOptionException("FLUX must be set to a non-zero positive value before the first irradiation step.")
                flux_set = True

                # Store the current flux amplitude - we'll use it when we find a TIME command
                current_flux_amp = fluxAmp

                # If FLUX is 0.0, we're entering the cooling phase
                if fluxAmp == 0.0:
                    continue

            # Handle TIME entries - can appear after any number of intermediate commands following FLUX
            elif line.startswith("TIME") and flux_set:
                time_parts = line.split()

                # Ensure we have at least the TIME keyword and a value
                if len(time_parts) < 2:
                    raise PypactInvalidOptionException(
                        "Invalid TIME line format: missing time value."
                    )

                # Get the time value
                time_value = float(time_parts[1])
                timeInSecs = time_value  # Default unit is seconds

                # Handle different TIME formats
                if len(time_parts) >= 3:
                    # Check if the third part is a time unit
                    if time_parts[2] in time_unit_to_seconds:
                        # Format: TIME 10.0 SECS or TIME 0.1 YEARS ATOMS
                        timeInSecs = time_value * time_unit_to_seconds[time_parts[2]]
                    # Otherwise, the third part is likely "ATOMS" or something else
                    # We keep the default assumption of seconds

                # Add the time to the appropriate schedule based on whether we're in irradiation or cooling phase
                if irradiation_active:
                    # Still in irradiation phase
                    self.addIrradiation(timeInSecs, current_flux_amp)
                else:
                    # In cooling phase after ZERO
                    self.addCooling(timeInSecs)

            elif line.startswith("ZERO"):
                # Ensure FLUX is set to zero before using ZERO
                if not flux_set:
                    raise PypactInvalidOptionException(
                        "FLUX must be set before using the ZERO keyword."
                    )
                # Stop processing irradiation schedule
                irradiation_active = False
                current_flux_amp = 0.0

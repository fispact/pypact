import os
from typing import List

from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactOutOfRangeException
from pypact.util.exceptions import PypactInvalidOptionException
from pypact.util.exceptions import PypactIncompatibleOptionException
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.loglevels import *
from pypact.input.keywords import CONTROL_KEYWORDS, INIT_KEYWORDS, INVENTORY_KEYWORDS
from pypact.input.projectiles import PROJECTILE_NEUTRON, VALID_PROJECTILES

COMMENT_START = '<<'
COMMENT_END   = '>>'

class InventoryType(JSONSerializable):
    def __init__(self):
        # a list of tuples, the first entry is the element/nuclide symbol
        # the second is the value
        self.entries: List(str, float) = []

@freeze_it
class MassInventory(InventoryType):
    def __init__(self):
        super().__init__()

        # the total mass in kg
        self.totalMass: float = 0.0

    def __str__(self) -> str:
        strrep = "{} {} {}".format('MASS', self.totalMass, len(self.entries))
        for e in self.entries:
            strrep += "\n{} {}".format(e[0], e[1])

        return strrep

@freeze_it
class FuelInventory(InventoryType):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        strrep = "{} {}".format('FUEL', len(self.entries))
        for i in self.entries:
            strrep += "\n{} {}".format(i[0], i[1])

        return strrep   

@freeze_it
class InputData(JSONSerializable):

    def __init__(self, name: str ="run"):
        """
            Constructor
            
            Initialises all input data
        """
        self.name: str = name
        
        self._overwrite: bool             = False
        self._json: bool                  = False
        self._ignorecollapse: bool        = True
        self._ignorecondense: bool        = True
        self._condense: bool              = False
        self._binaryxs: bool              = False
        self._useeaf: bool                = False
        self._approxgamma: bool           = False
        self._outputhalflife: bool        = False
        self._outputhazards: bool         = False
        self._initialinventory: bool      = False
        self._readgammagroup: bool        = False
        self._readspontfission: bool      = False
        self._ignoreuncert: bool          = False
        self._enablemonitor: bool         = False
        self._usecumfissyield: bool       = False
        self._clearancedata: bool         = False
        self._loglevel: bool              = LOG_SEVERITY_WARNING
        
        # default is 1.0E-12 barns
        self._xsthreshold: float         = 1.0e-12
        self._group: int                 = 0
        self._projectile: int            = PROJECTILE_NEUTRON

        # set the minimum number of atoms deemed significant for the inventory output
        self._atomsthreshold: float       = 0.0
        
        # the total mass in grams per cubic centimetre (g/cc)
        self._density: float              = 0.0

        self._inventoryismass: bool       = False
        self._inventoryisfuel: bool       = False 
        
        self._inventorymass: InventoryType = MassInventory()
        self._inventoryfuel: InventoryType = FuelInventory()
    
        # irradiation schedule
        # a list of tuples of (time interval in seconds, flux amplitude)
        self._irradschedule: list = []
        
        # cooling schedule
        # a list of time interval in seconds
        self._coolingschedule: list = []
    
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

    def overwriteExisting(self, overwrite: bool = True):
        """
            Enables overwriting of output files
            uses keyword CLOBBER
        """
        self._overwrite = overwrite

    def enableJSON(self, enable: bool = True):
        """
            Enables JSON output file
            uses keyword JSON
        """
        self._json = enable
    
    def enableInitialInventoryInOutput(self, output: bool = True):
        """
            Performs the time = 0, inventory step,
            the initial inventory
        """
        self._initialinventory = output
    
    def enableHalflifeInOutput(self, output: bool = True):
        """
            Enables half lives to be written to the output file
        """
        self._outputhalflife = output
    
    def enableHazardsInOutput(self, output: bool = True):
        self._outputhazards = output
    
    def doCollapse(self, group: int, binary: bool = False):
        if self._useeaf and binary:
            raise PypactIncompatibleOptionException("Cannot enable binary format reading when using EAF")

        self._ignorecollapse = False
        self._group = group
        self._binaryxs = binary
    
    def useEAFLibraries(self, use: bool = True):
        if self._binaryxs and use:
            raise PypactIncompatibleOptionException("Cannot enable EAF data libraries with binary format")

        self._useeaf = use
    
    def useCumulativeFissionYieldData(self, use: bool = True):
        self._usecumfissyield = use
    
    def includeClearanceData(self, include: bool = True):
        self._clearancedata = include
    
    def doCondense(self, condense: bool = True):
        self._ignorecondense = False
        self._condense = condense
    
    def approxGammaSpectrum(self, approxgamma: bool = True):
        self._approxgamma = approxgamma
    
    def ignoreUncertainties(self, ignore: bool = True):
        self._ignoreuncert = ignore
    
    def setXSThreshold(self, threshold: float):
        self._xsthreshold = threshold
    
    def setProjectile(self, proj: int):
        if proj not in VALID_PROJECTILES:
            raise PypactInvalidOptionException("{} is not a valid projectile option.")
            
        self._projectile = proj

    def readGammaGroup(self, readgg: bool = True):
        self._readgammagroup = readgg
    
    def enableSystemMonitor(self, enable: bool = True):
        self._enablemonitor = enable

    def setAtomsThreshold(self, threshold: float):
        self._atomsthreshold = threshold
    
    def addIrradiation(self, timeInSecs: float, fluxAmp: float):
        self._irradschedule.append((timeInSecs, fluxAmp))
    
    def resetIrradiation(self):
        self._irradschedule: List[float, float] = []
    
    def addCooling(self, timeInSecs: float):
        self._coolingschedule.append(timeInSecs)
    
    def resetCooling(self):
        self._coolingschedule: List[float] = []
    
    def setLogLevel(self, severity: int):
        if severity < LOG_SEVERITY_FATAL or severity > LOG_SEVERITY_TRACE:
            raise PypactOutOfRangeException("Log level {} not valid.".format(severity))
        self._loglevel = severity

    def setDensity(self, densityInGPCC: float):
        """
            Sets the density of the target in g/cc
            densityInGPCC: density in g/cc, must be positive
        """
        if not densityInGPCC > 0.0:
            raise PypactOutOfRangeException("Density must be positive.")

        self._density = densityInGPCC

    def setMass(self, totalMassInKg: float):
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

        self._inventoryismass: bool = False
        self._inventoryisfuel: bool = True

    def addIsotope(self, isotope: str, numberOfAtoms: float):
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
        self._inventoryfuel.entries: List[str, float] = []

    def addElement(self, element: str, percentage: float = 100.0):
        """
            Add an element
            element: character symbol of element name, e.g. 'Fe'
            percentage: percentage contribution of total mass, should not exceed 100%
        """
        if percentage > 100.0:
            raise PypactOutOfRangeException("Cannot set the element percentage above 100%.")
        
        self._inventorymass.entries.append((element, percentage))
        
    def clearElements(self):
        self._inventorymass.entries: List[str, float] = []
    
    def _serialize(self, f):
        """
            The serialization method
            f: file object
        """
        inputdata = []
        
        def addnewline():
            inputdata.append("")
        
        def addcomment(comment):
            inputdata.append("{} {} {}".format(COMMENT_START, comment, COMMENT_END))
        
        def addkeyword(keyword, args=[]):
            strargs = ' '.join([str(a) for a in args])
            inputdata.append("{} {}".format(keyword, strargs))
        
        # control keywords
        addcomment("CONTROL PHASE")
        if self._json:
            addcomment("enable JSON output")
            addkeyword('JSON')
                
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
            
        if self._enablemonitor:
            addcomment("monitor FISPACT-II progress")
            addkeyword('MONITOR', args=[1])
        
        addcomment("the minimum cross section (barns) for inclusion in pathways analysis")
        addkeyword('XSTHRESHOLD', args=[self._xsthreshold])
        
        if not self._ignorecollapse:
            if self._group != 0:
                addcomment("perform collapse")
                addkeyword('GETXS', args=[-1 if self._binaryxs and not self._useeaf else 1, self._group])
            else:
                addcomment("don't do collapse, just read the existing file")
                addkeyword('GETXS', args=[0])

        if not self._ignorecondense:
            addcomment("get decay data")
            addkeyword('GETDECAY', args=[1 if self._condense else 0])
    
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
        
        # end control phase
        addcomment("end control")
        addkeyword('FISPACT')
        addkeyword('*', args=[self.name])

        # initial phase
        addnewline()
        addcomment("INITIALIZATION PHASE")
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
        
        if self._initialinventory:
            addcomment("output the initial inventory")
            addkeyword('ATOMS')

        # inventory phase
        addnewline()
        addcomment("INVENTORY PHASE")
        if len(self._irradschedule) > 0:
            addcomment("irradiation schedule")
            for time, fluxamp in self._irradschedule:
                addkeyword('FLUX', args=[fluxamp])
                addkeyword('TIME', args=[time, 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of irradiation")

            addkeyword('FLUX', args=[0.0])
            addkeyword('ZERO')
            for time in self._coolingschedule:
                addkeyword('TIME', args=[time, 'SECS'])
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
        pass



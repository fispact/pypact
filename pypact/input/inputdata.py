import os

from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactOutOfRangeException, PypactInvalidOptionException
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.loglevels import *
from pypact.input.keywords import CONTROL_KEYWORDS, INIT_KEYWORDS, INVENTORY_KEYWORDS
from pypact.input.projectiles import PROJECTILE_NEUTRON, VALID_PROJECTILES

COMMENT_START = '<<'
COMMENT_END   = '>>'

@freeze_it
class MassInventory(JSONSerializable):
    def __init__(self):
        # the total mass in kg
        self.totalMass    = 0.0
        
        # a list of tuples, the first entry is the element symbol
        # the second is the percentage contribution
        self.elements     = []

    def __str__(self):
        strrep = "{} {} {}".format('MASS', self.totalMass, len(self.elements))
        for e in self.elements:
            strrep += "\n{} {}".format(e[0], e[1])

        return strrep

@freeze_it
class InputData(JSONSerializable):

    def __init__(self, name="run"):
        """
            Constructor
            
            Initialises all input data
        """
        self.name = name
        
        self.overwrite             = False
        self.json                  = False
        self.condense              = False
        self.binaryxs              = False
        self.useeaf                = False
        self.approxgamma           = False
        self.outputhalflife        = False
        self.outputhazards         = False
        self.initialinventory      = False
        self.readgammagroup        = False
        self.readspontfission      = False
        self.ignoreuncert          = False
        self.enablemonitor         = False
        self.usecumfissyield       = False
        self.clearancedata         = False
        self.loglevel              = LOG_SEVERITY_WARNING
        
        self.xsthreshold           = 0
        self.group                 = 0
        self.projectile            = PROJECTILE_NEUTRON

        # set the minimum number of atoms deemed significant for the inventory output
        self.atomsthreshold        = 0.0
        
        # the total mass in grams per cubic centimetre (g/cc)
        self.density               = 0.0
        
        self.inventorymass         = MassInventory()
    
        # irradiation schedule
        # a list of tuples of (time interval in seconds, flux amplitude)
        self.irradschedule         = []
        
        # cooling schedule
        # a list of time interval in seconds
        self.coolingschedule       = []
    
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

    def overwriteExisting(self, overwrite=True):
        """
            Enables overwriting of output files
            uses keyword CLOBBER
        """
        self.overwrite = overwrite

    def enableJSON(self, enable=True):
        """
            Enables JSON output file
            uses keyword JSON
        """
        self.json = enable
    
    def enableInitialInventoryInOutput(self, output=True):
        """
            Performs the time = 0, inventory step,
            the initial inventory
        """
        self.initialinventory = output
    
    def enableHalflifeInOutput(self, output=True):
        """
            Enables half lives to be written to the output file
        """
        self.outputhalflife = output
    
    def enableHazardsInOutput(self, output=True):
        self.outputhazards = output
    
    def doCollapse(self, group, binary=False):
        self.group = group
        self.binaryxs = binary
    
    def useEAFLibraries(self, use=True):
        self.useeaf = use
    
    def useCumulativeFissionYieldData(self, use=True):
        self.usecumfissyield = use
    
    def includeClearanceData(self, include=True):
        self.clearancedata = include
    
    def doCondense(self, condense=True):
        self.condense = condense
    
    def approxGammaSpectrum(self, approxgamma=True):
        self.approxgamma = approxgamma
    
    def ignoreUncertainties(self, ignore=True):
        self.ignoreuncert = ignore
    
    def setXSThreshold(self, threshold):
        self.xsthreshold = threshold
    
    def setProjectile(self, proj):
        if proj not in VALID_PROJECTILES:
            raise PypactInvalidOptionException("{} is not a valid projectile option.")
            
        self.projectile = proj

    def readGammaGroup(self, readgg=True):
        self.readgammagroup = readgg
    
    def enableSystemMonitor(self, enable=True):
        self.enablemonitor = enable

    def setAtomsThreshold(self, threshold):
        self.atomsthreshold = threshold
    
    def addIrradiation(self, timeInSecs, fluxAmp):
        self.irradschedule.append((timeInSecs, fluxAmp))
    
    def resetIrradiation(self):
        self.irradschedule = []
    
    def addCooling(self, timeInSecs):
        self.coolingschedule.append(timeInSecs)
    
    def resetCooling(self):
        self.coolingschedule = []
    
    def setLogLevel(self, severity):
        if severity < LOG_SEVERITY_FATAL or severity > LOG_SEVERITY_TRACE:
            raise PypactOutOfRangeException("Log level {} not valid.".format(severity))
        self.loglevel = severity

    def setDensity(self, densityInGPCC):
        """
            Sets the density of the target in g/cc
            densityInGPCC: density in g/cc, must be positive
        """
        if not densityInGPCC > 0.0:
            raise PypactOutOfRangeException("Density must be positive.")

        self.density = densityInGPCC

    def setMass(self, totalMassInKg):
        """
            Sets the total mass of the target in kg
            totalMassInKg: mass in kg, must be positive
        """
        if not totalMassInKg > 0.0:
            raise PypactOutOfRangeException("Total mass must be positive.")

        self.inventorymass.totalMass = totalMassInKg

    def addElement(self, element, percentage=100.0):
        """
            Add an element
            element: character symbol of element name, e.g. 'Fe'
            percentage: percentage contribution of total mass, should not exceed 100%
        """
        if percentage > 100.0:
            raise PypactOutOfRangeException("Cannot set the element percentage above 100%.")
        
        self.inventorymass.elements.append((element, percentage))
        
    def clearElements(self):
        self.inventorymass.elements = []
    
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
        if self.json:
            addcomment("enable JSON output")
            addkeyword('JSON')
                
        if self.overwrite:
            addcomment("overwrite existing output files of same name")
            addkeyword('CLOBBER')
        
        if self.readgammagroup:
            addcomment("read gamma groups from file, specify ggbins in files file")
            addkeyword('READGG')
        
        if self.readspontfission:
            addcomment("read spontaneous fission from file, specify sf_endf in files file")
            addkeyword('READSF')
        
        if self.useeaf:
            addcomment("use EAF nuclear data libraries")
            addkeyword('LIBVERSION', args=[0])
        
        if self.usecumfissyield:
            addcomment("use cumulative fission yield data mt=459 instead of mt=454")
            addkeyword('CUMFYLD')
            
        if self.enablemonitor:
            addcomment("monitor FISPACT-II progress")
            addkeyword('MONITOR', args=[1])
        
        if self.xsthreshold > 0:
            addcomment("alter the default minimum cross section for inclusion in pathways analysis")
            addkeyword('XSTHRESHOLD', args=[self.xsthreshold])
            
        if self.group != 0:
            addcomment("perform collapse")
            addkeyword('GETXS', args=[-1 if self.binaryxs and not self.useeaf else 1, self.group])
        else:
            addcomment("don't do collapse, just read the existing file")
            addkeyword('GETXS', args=[0])

        addcomment("get decay data")
        addkeyword('GETDECAY', args=[1 if self.condense else 0])
    
        addcomment("enable logging at level {}".format(self.loglevel))
        addkeyword('LOGLEVEL', args=[self.loglevel])

        if self.approxgamma:
            addcomment("approximate spectra when not available")
            addkeyword('SPEK')
        
        if self.ignoreuncert:
            addcomment("ignore uncertainties")
            addkeyword('NOERROR')
    
        addcomment("set projectile (n=1, d=2, p=3, a=4, g=5)")
        addkeyword('PROJ', args=[self.projectile])
        
        # end control phase
        addcomment("end control")
        addkeyword('FISPACT')
        addkeyword('*', args=[self.name])

        # initial phase
        addnewline()
        addcomment("INITIALIZATION PHASE")
        if self.outputhalflife:
            addcomment("output half life values")
            addkeyword('HALF')

        if self.outputhazards:
            addcomment("output ingestion and inhalation values")
            addkeyword('HAZARDS')

        if self.clearancedata:
            addcomment("include clearance data of radionuclides to be input")
            addkeyword('CLEAR')
            
        if self.inventorymass.totalMass > 0.0:
            addcomment("set the target via MASS")
            addkeyword(str(self.inventorymass))
        
        if self.density > 0.0:
            addcomment("set the target density")
            addkeyword('DENSITY', args=[self.density])
        
        if self.atomsthreshold > 0.0:
            addcomment("set the threshold for atoms in the inventory")
            addkeyword('MIND', args=[self.atomsthreshold])
        
        if self.initialinventory:
            addcomment("output the initial inventory")
            addkeyword('ATOMS')

        # inventory phase
        addnewline()
        addcomment("INVENTORY PHASE")

        addcomment("irradiation schedule")
        for time, fluxamp in self.irradschedule:
            addkeyword('FLUX', args=[fluxamp])
            addkeyword('TIME', args=[time, 'SECS'])
            addkeyword('ATOMS')
        addcomment("end of irradiation")

        addkeyword('FLUX', args=[0.0])
        addkeyword('ZERO')
        for time in self.coolingschedule:
            addkeyword('TIME', args=[time, 'SECS'])
            addkeyword('ATOMS')
        addcomment("end of cooling")

        # end file
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



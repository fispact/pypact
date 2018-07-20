import os

from pypact.input.keywords import CONTROL_KEYWORDS, INIT_KEYWORDS, INVENTORY_KEYWORDS
from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactOutOfRangeException
from pypact.util.loglevels import *

PROJECTILE_NEUTRON  = 1
PROJECTILE_DEUTERON = 2
PROJECTILE_PROTRON  = 3
PROJECTILE_ALPHA    = 4
PROJECTILE_GAMMA    = 5

VALID_PROJECTILES = [
    PROJECTILE_NEUTRON,
    PROJECTILE_DEUTERON,
    PROJECTILE_PROTRON,
    PROJECTILE_ALPHA,
    PROJECTILE_GAMMA
]

COMMENT_START = '<<'
COMMENT_END   = '>>'

@freeze_it
class MassInventory(object):
    def __init__(self):
        # the total mass in kg
        self._totalMass    = 0.0
        
        # a list of tuples, the first entry is the element symbol
        # the second is the percentage contribution
        self._elements     = []

    def __str__(self):
        strrep = "{} {} {}".format('MASS', self._totalMass, len(self._elements))
        for e in self._elements:
            strrep += "\n{} {}".format(e[0], e[1])

        return strrep

@freeze_it
class InputData(object):

    def __init__(self, name="run"):
        self._name      = name
        
        self._overwrite             = False
        self._json                  = False
        self._condense              = False
        self._binaryXS              = False
        self._useEAF                = False
        self._approxGamma           = False
        self._outputHalflife        = False
        self._outputHazards         = False
        self._outputInitialInventory= False
        self._readGammaGroup        = False
        self._readSF                = False
        self._ignoreUncertainties   = False
        self._enableMonitor         = False
        self._useCumFY              = False
        self._logLevel              = LOG_SEVERITY_WARNING
        
        self._xsThreshold           = 0
        self._group                 = 0
        self._projectile            = PROJECTILE_NEUTRON

        # set the minimum number of atoms deemed significant for the inventory output
        self._atomsThreshold        = 0.0
        
        # the total mass in grams per cubic centimetre (g/cc)
        self._density               = 0.0
        
        self._inventoryMass         = MassInventory()
    
        # irradiation schedule
        # a list of tuples of (time interval in seconds, flux amplitude)
        self._irradSchedule         = []
        
        # cooling schedule
        # a list of time interval in seconds
        self._coolingSchedule       = []
    
    def reset(self):
        self.__init__(self._name)

    def validate(self):
        # to do
        pass

    def overwriteExisting(self, overwrite=True):
        self._overwrite = overwrite

    def enableJSON(self, enable=True):
        self._json = enable
    
    def outputInitialInventory(self, output=True):
        self._outputInitialInventory = output
    
    def outputHalflife(self, output=True):
        self._outputHalflife = output
    
    def outputHazards(self, output=True):
        self._outputHazards = output
    
    def collapse(self, group, binary=False):
        self._group = group
        self._binaryXS = binary
    
    def useEAF(self, use=True):
        self._useEAF = use
    
    def useCumulativeFissionYieldData(self, use=True):
        self._useCumFY = use
    
    def condense(self, condense=True):
        self._condense = condense
    
    def approxGammaSpectrum(self, approxGamma=True):
        self._approxGamma = approxGamma
    
    def ignoreUncertainties(self, ignore=True):
        self._ignoreUncertainties = ignore
    
    def setXSThreshold(self, threshold):
        self._xsThreshold = threshold
    
    def _useParticle(self, particle):
        self._projectile = particle
    
    def useNeutron(self):
        self._useParticle(PROJECTILE_NEUTRON)
    
    def useDeuteron(self):
        self._useParticle(PROJECTILE_DEUTERON)
    
    def useProton(self):
        self._useParticle(PROJECTILE_PROTRON)
    
    def useAlpha(self):
        self._useParticle(PROJECTILE_ALPHA)
    
    def useGamma(self):
        self._useParticle(PROJECTILE_GAMMA)

    def readGammaGroup(self, readgg=True):
        self._readGammaGroup = readgg
    
    def enableMonitor(self, enable=True):
        self._enableMonitor = enable

    def setAtomsThreshold(self, threshold):
        self._atomsThreshold = threshold
    
    def addIrradiation(self, timeInSecs, fluxAmp):
        self._irradSchedule.append((timeInSecs, fluxAmp))
    
    def resetIrradiation(self):
        self._irradSchedule = []
    
    def addCooling(self, timeInSecs):
        self._coolingSchedule.append(timeInSecs)
    
    def resetCooling(self):
        self._coolingSchedule = []
    
    def setLogLevel(self, severity):
        if severity < LOG_SEVERITY_FATAL or severity > LOG_SEVERITY_TRACE:
            raise PypactOutOfRangeException("Log level {} not valid.".format(severity))
        self._logLevel = severity

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
            Sets the total mass of the target in kg
            totalMassInKg: mass in kg, must be positive
        """
        if not totalMassInKg > 0.0:
            raise PypactOutOfRangeException("Total mass must be positive.")

        self._inventoryMass._totalMass = totalMassInKg

    def addElement(self, element, percentage=100.0):
        """
            Add an element
            element: character symbol of element name, e.g. 'Fe'
            percentage: percentage contribution of total mass, should not exceed 100%
        """
        if percentage > 100.0:
            raise PypactOutOfRangeException("Cannot set the element percentage above 100%.")
        
        self._inventoryMass._elements.append((element, percentage))
        
    def clearElements(self):
        self._inventoryMass._elements = []
    
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
        
        if self._readGammaGroup:
            addcomment("read gamma groups from file, specify ggbins in files file")
            addkeyword('READGG')
        
        if self._readSF:
            addcomment("read spontaneous fission from file, specify sf_endf in files file")
            addkeyword('READSF')
        
        if self._useEAF:
            addcomment("use EAF nuclear data libraries")
            addkeyword('LIBVERSION', args=[0])
        
        if self._useCumFY:
            addcomment("use cumulative fission yield data mt=459 instead of mt=454")
            addkeyword('CUMFYLD')
            
        if self._enableMonitor:
            addcomment("monitor FISPACT-II progress")
            addkeyword('MONITOR', args=[1])
        
        if self._xsThreshold > 0:
            addcomment("alter the default minimum cross section for inclusion in pathways analysis")
            addkeyword('XSTHRESHOLD', args=[self._xsThreshold])
            
        if self._group != 0:
            addcomment("perform collapse")
            addkeyword('GETXS', args=[-1 if self._binaryXS and not self._useEAF else 1, self._group])
        else:
            addcomment("don't do collapse, just read the existing file")
            addkeyword('GETXS', args=[0])

        addcomment("get decay data")
        addkeyword('GETDECAY', args=[1 if self._condense else 0])
    
        addcomment("enable logging at level {}".format(self._logLevel))
        addkeyword('LOGLEVEL', args=[self._logLevel])

        if self._approxGamma:
            addcomment("approximate spectra when not available")
            addkeyword('SPEK')
        
        if self.ignoreUncertainties:
            addcomment("ignore uncertainties")
            addkeyword('NOERROR')
    
        addcomment("set projectile (n=1, d=2, p=3, a=4, g=5)")
        addkeyword('PROJ', args=[self._projectile])
        
        # end control phase
        addcomment("end control")
        addkeyword('FISPACT')
        addkeyword('*', args=[self._name])

        # initial phase
        addnewline()
        addcomment("INITIALIZATION PHASE")
        if self._outputHalflife:
            addcomment("output half life values")
            addkeyword('HALF')

        if self._outputHazards:
            addcomment("output ingestion and inhalation values")
            addkeyword('HAZARDS')
            
        if self._inventoryMass._totalMass > 0.0:
            addcomment("set the target via MASS")
            addkeyword(str(self._inventoryMass))
        
        if self._density > 0.0:
            addcomment("set the target density")
            addkeyword('DENSITY', args=[self._density])
        
        if self._atomsThreshold > 0.0:
            addcomment("set the threshold for atoms in the inventory")
            addkeyword('MIND', args=[self._atomsThreshold])
        
        if self._outputInitialInventory:
            addcomment("output the initial inventory")
            addkeyword('ATOMS')
        
        # inventory phase
        addnewline()
        addcomment("INVENTORY PHASE")
        
        addcomment("irradiation schedule")
        for time, fluxamp in self._irradSchedule:
            addkeyword('FLUX', args=[fluxamp])
            addkeyword('TIME', args=[time, 'SECS'])
            addkeyword('ATOMS')
        
        addcomment("end of irradiation")
        addkeyword('FLUX', args=[0.0])
        addkeyword('ZERO')
        for time in self._coolingSchedule:
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



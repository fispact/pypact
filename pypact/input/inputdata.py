import os

from pypact.input.keywords import CONTROL_KEYWORDS, INIT_KEYWORDS, INVENTORY_KEYWORDS
from pypact.util.decorators import freeze_it

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

@freeze_it
class InputData(object):
    def __init__(self, name="run"):
        self._name      = name
        
        self._overwrite     = False
        self._json          = False
        self._condense      = False
        self._binaryXS      = False
        self._useEAF        = False
        self._approxGamma   = False
        self._ignoreUncertainties = False
        
        self._group         = 0
        self._projectile    = PROJECTILE_NEUTRON

    def reset(self):
        self.__init__(self._name)

    def validate(self):
        # to do
        return True

    def overwriteExisting(self, overwrite=True):
        self._overwrite = overwrite

    def enableJSON(self, enable=True):
        self._json = enable
    
    def collapse(self, group, binary=False):
        self._group = group
        self._binaryXS = binary
    
    def useEAF(self, use=True):
        self._useEAF = use
    
    def condense(self, condense=True):
        self._condense = condense
    
    def approxGammaSpectrum(self, approxGamma=True):
        self._approxGamma = approxGamma
    
    def ignoreUncertainties(self, ignore=True):
        self._ignoreUncertainties = ignore
    
    def useNeutron(self):
        self._projectile = PROJECTILE_NEUTRON
    
    def useDeuteron(self):
        self._projectile = PROJECTILE_DEUTERON
    
    def useProtron(self):
        self._projectile = PROJECTILE_PROTRON
    
    def useAlpha(self):
        self._projectile = PROJECTILE_ALPHA
    
    def useGamma(self):
        self._projectile = PROJECTILE_GAMMA

    
    def _serialize(self, f):
        """
            The serialization method
            f: file object
        """
        inputdata = []
        
        # control keywords
        if self._json:
            inputdata.append('JSON')
            
        if self._overwrite:
            inputdata.append('CLOBBER')
        
        if self._useEAF:
            inputdata.append('LIBVERSION 0')
        
        if self._group != 0:
            option = -1 if self._binaryXS and not self._useEAF else 1
            inputdata.append('GETXS {} {}'.format(option, self._group))
        else:
            inputdata.append('GETXS 0')
        
        option = 1 if self._condense else 0
        inputdata.append('GETDECAY {}'.format(option))
    
        if self._approxGamma:
            inputdata.append('SPEK')
        
        if self.ignoreUncertainties:
            inputdata.append('NOERROR')
    
        inputdata.append('PROJ {}'.format(self._projectile))
        
        # end control phase
        inputdata.append('FISPACT')
        inputdata.append('* {}'.format(self._name))
        
        # end file
        inputdata.append('END')
        inputdata.append('* end')
        
        for line in inputdata:
            f.write("{}\n".format(line))

    def _deserialize(self, f):
        """
            The deserialization method
            f: file object
        """
        pass



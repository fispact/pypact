import os

from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactDeserializeException
from pypact.util.file import file_exists, dir_exists

# represents a null entry string
NULL_ENTRY = "null"

XS_LIBS = {
            'TENDL2014':
            {
                'ind_nuc' : os.path.join('TENDL2014data', 'tendl14_decay12_index'),
                'xs_endf' : os.path.join('TENDL2014data', 'tal2014-n', 'gxs-709'),
                'prob_tab' : os.path.join('TENDL2014data', 'tal2014-n', 'tp-709-294')
            },
            'TENDL2015':
            {
                'ind_nuc' : os.path.join('TENDL2015data', 'tendl15_decay12_index'),
                'xs_endf' : os.path.join('TENDL2015data', 'tal2015-n', 'gxs-709'),
                'prob_tab' : os.path.join('TENDL2015data', 'tal2015-n', 'tp-709-294')
            },
            'TENDL2017':
            {
                'ind_nuc' : os.path.join('TENDL2017data', 'tendl17_decay12_index'),
                'xs_endf' : os.path.join('TENDL2017data', 'tal2017-n', 'gxs-709'),
                'prob_tab' : os.path.join('TENDL2017data', 'tal2017-n', 'tp-709-294')
            }
}

FISSION_LIBS = {
            'GEFY61':
            {
                'fy_endf' : os.path.join('GEFY61data', 'gefy61_nfy'),
                'sf_endf' : os.path.join('GEFY61data', 'gefy61_sfy')
            },
            'GEFY52':
            {
                'fy_endf' : os.path.join('GEFY52data', 'gefy52_nfy'),
                'sf_endf' : os.path.join('GEFY52data', 'gefy52_sfy')
            }
}

@freeze_it
class FilesFile(object):
    def __init__(self, base_dir=os.sep):
        self.nullify()
        
        self.base_dir = base_dir
        
        # defaults
        self.ind_nuc    = os.path.join(base_dir, "TENDL2015data", "tendl15_decay12_index")
        self.xs_endf    = os.path.join(base_dir, "TENDL2015data", "tal2015-n", "gxs-709")
        self.prob_tab   = os.path.join(base_dir, "TENDL2015data", "tal2015-n", "tp-709-294")
        self.fy_endf    = os.path.join(base_dir, "GEFY61data", "gefy61_nfy")
        self.sf_endf    = os.path.join(base_dir, "GEFY61data", "gefy61_sfy")
        self.dk_endf    = os.path.join(base_dir, "decay", "decay_2012")
        self.hazards    = os.path.join(base_dir, "decay", "hazards_2012")
        self.clear      = os.path.join(base_dir, "decay", "clear_2012")
        self.a2data     = os.path.join(base_dir, "decay", "a2_2012")
        self.absorp     = os.path.join(base_dir, "decay", "abs_2012")
        self.fluxes     = "fluxes"
        self.collapxi   = "COLLAPX"
        self.collapxo   = "COLLAPX"
        self.arrayx     = "ARRAYX"
    
    def nullify(self):
        self.ind_nuc    = NULL_ENTRY
        self.xs_endf    = NULL_ENTRY
        self.prob_tab   = NULL_ENTRY
        self.fy_endf    = NULL_ENTRY
        self.sf_endf    = NULL_ENTRY
        self.dk_endf    = NULL_ENTRY
        self.hazards    = NULL_ENTRY
        self.clear      = NULL_ENTRY
        self.a2data     = NULL_ENTRY
        self.absorp     = NULL_ENTRY
        self.fluxes     = NULL_ENTRY
        self.collapxi   = NULL_ENTRY
        self.collapxo   = NULL_ENTRY
        self.arrayx     = NULL_ENTRY
        
        # optionals
        self.ggbins     = NULL_ENTRY
        self.xs_extra   = NULL_ENTRY
    
    def setXS(self, type):
        if type not in XS_LIBS:
            raise PypactException(
                    "Cannot set cross section library to type {0}, does not exist.".format(type))
        
        self.ind_nuc = os.path.join(self.base_dir, XS_LIBS[type]['ind_nuc'])
        self.xs_endf = os.path.join(self.base_dir, XS_LIBS[type]['xs_endf'])
        self.prob_tab = os.path.join(self.base_dir, XS_LIBS[type]['prob_tab'])

    def setFission(self, type):
        if type not in FISSION_LIBS:
            raise PypactException(
                    "Cannot set fission library to type {0}, does not exist.".format(type))
        
        self.fy_endf = os.path.join(self.base_dir, FISSION_LIBS[type]['fy_endf'])
        self.sf_endf = os.path.join(self.base_dir, FISSION_LIBS[type]['sf_endf'])

    def validate(self):
        """
            Validate if paths in files file exist
            Return a list of tuples (key, value) that do not exist
        """
        invalid = []
        for k, v in self.__dict__.items():
            if k in ['collapxi', 'collapxo', 'arrayx', 'fluxes'] or '__' in k:
                continue
            
            if not v or (not file_exists(v) and not dir_exists(v)):
                invalid.append((k,v))

        return invalid

    def _serialize(self, f):
        """
            The serialization method
            f: file object
            
            Format is:
            
            key1          value1
            
            key2          value2
            
            ...
        """
        for k, v in self.__dict__.items():
            if '__' not in k and v != NULL_ENTRY:
                f.write("{:<20} {:<100}\n\n".format(k,v))

    def _deserialize(self, f):
        """
            The deserialization method
            f: file object
            
            Format is:
            
            key1          value1
            
            key2          value2
        """
        for line in f:
            data = line.split()
            if not data:
                continue
            
            k = data[0]
            if k not in self.__dict__:
                raise PypactDeserializeException(
                    "Cannot deserialize files file. Unknown key {0} specified.".format(k))

            if self.__dict__[k] != NULL_ENTRY:
                raise PypactDeserializeException(
                    "Cannot deserialize files file. Repeated key {0} specified.".format(k))
            
            self.__setattr__(k, data[1])


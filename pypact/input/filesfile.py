import os

from pypact.library.projectiles import *
from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactDeserializeException
from pypact.util.file import dir_exists, file_exists
from pypact.util.jsonserializable import JSONSerializable

# represents a null entry string
NULL_ENTRY = "null"

NUCLEAR_LIBS = {
    "TENDL2014": {
        "ind_nuc": os.path.join("TENDL2014data", "tendl14_decay12_index"),
        "xs_endf": os.path.join("TENDL2014data", "tal2014-n", "gxs-709"),
        "prob_tab": os.path.join("TENDL2014data", "tal2014-n", "tp-709-294"),
    },
    "TENDL2015": {
        "ind_nuc": os.path.join("TENDL2015data", "tendl15_decay12_index"),
        "xs_endf": os.path.join("TENDL2015data", "tal2015-n", "gxs-709"),
        "prob_tab": os.path.join("TENDL2015data", "tal2015-n", "tp-709-294"),
    },
    "TENDL2017": {
        "ind_nuc": os.path.join("TENDL2017data", "tendl17_decay12_index"),
        "xs_endf": os.path.join("TENDL2017data", "tal2017-n", "gxs-709"),
        "prob_tab": os.path.join("TENDL2017data", "tal2017-n", "tp-709-294"),
    },
    "EAF2010": {
        "ind_nuc": os.path.join("EAF2010data", "eaf_index_20100"),
        "crossec": os.path.join("EAF2010data", "eaf_n_gxs_066_fis_20100"),
        "crossunc": os.path.join("EAF2010data", "eaf_un_20100"),
        "decay": os.path.join("EAF2010data", "eaf_dec_20100.001"),
        "asscfy": os.path.join("EAF2010data", "eaf_n_asscfy_20100"),
        "fissyld": os.path.join("EAF2010data", "eaf_n_fis_20100"),
        "hazards": os.path.join("EAF2010data", "eaf_haz_20100"),
        "clear": os.path.join("EAF2010data", "eaf_clear_20100"),
        "a2data": os.path.join("EAF2010data", "eaf_a2_20100"),
        "absorp": os.path.join("EAF2010data", "eaf_abs_20100"),
    },
    "CENDL31": {
        "ind_nuc": os.path.join("CENDL31data", "cendl31_decay12_index"),
        "xs_endf": os.path.join("CENDL31data", "cendl31-n", "gxs-709"),
    },
    "ENDFB71": {
        "ind_nuc": os.path.join("ENDFB71data", "endfb71_index"),
        "xs_endf": os.path.join("ENDFB71data", "endfb71-n", "gxs-709"),
        "dk_endf": os.path.join("ENDFB71data", "decay"),
        "fy_endf": os.path.join("ENDFB71data", "endfb71nfy"),
        "sf_endf": os.path.join("ENDFB71data", "endfb71sfy"),
    },
    "ENDFB80": {
        "ind_nuc": os.path.join("ENDFB80data", "endfb80_index"),
        "xs_endf": os.path.join("ENDFB80data", "endfb80-n", "gxs-709"),
        "dk_endf": os.path.join("ENDFB80data", "decay"),
    },
    "GEFY42": {
        "fy_endf": os.path.join("GEFY42data", "gefy42_nfy"),
        "sf_endf": os.path.join("GEFY42data", "gefy42_sfy"),
    },
    "GEFY52": {
        "fy_endf": os.path.join("GEFY52data", "gef52_nfy"),
        "sf_endf": os.path.join("GEFY52data", "gef52_sfy"),
    },
    "GEFY61": {
        "fy_endf": os.path.join("GEFY61data", "gefy61_nfy"),
        "sf_endf": os.path.join("GEFY61data", "gefy61_sfy"),
    },
    "UKFY41": {
        "fy_endf": os.path.join("UKFY41data", "ukfy4_1p"),
    },
    "UKFY42": {
        "fy_endf": os.path.join("UKFY42data", "ukfy4_2n"),
    },
    "HEAD2009": {
        "ind_nuc": os.path.join("HEAD2009data", "head2009-n_decay12_index"),
        "xs_endf": os.path.join("ENDFB71data", "head2009-n", "gxs-sp-709"),
    },
    "HEIR01": {
        "ind_nuc": os.path.join("HEIR01data", "heir01_decay12_index"),
        "xs_endf": os.path.join("HEIR01data", "heir01-p", "gxs-162"),
    },
    "JEFF32": {
        "ind_nuc": os.path.join("JEFF32data", "jeff32_decay12_index"),
        "xs_endf": os.path.join("JEFF32data", "jeff32-n", "gxs-709"),
        "dk_endf": os.path.join("JEFF32data", "decay"),
        "fy_endf": os.path.join("JEFF32data", "jeff32-n", "jeff311nfy"),
        "sf_endf": os.path.join("JEFF32data", "jeff32-n", "jeff311sfy"),
    },
    "JEFF33": {
        "ind_nuc": os.path.join("JEFF33data", "jeff33_decay12_index"),
        "xs_endf": os.path.join("JEFF33data", "jeff33-n", "gxs-709"),
        "prob_tab": os.path.join("JEFF33data", "jeff33-n", "tp-709-294"),
        "dk_endf": os.path.join("JEFF33data", "decay"),
        "fy_endf": os.path.join("JEFF33data", "jeff33-n", "jeff33nfy"),
        "sf_endf": os.path.join("JEFF33data", "jeff33-n", "jeff33sfy"),
    },
    "JENDL4data": {
        "ind_nuc": os.path.join("JENDL4data", "jendl4_decay12_index"),
        "xs_endf": os.path.join("JENDL4data", "jendl4-n", "gxs-709"),
        "dk_endf": os.path.join("JENDL4data", "decay"),
        "fy_endf": os.path.join("JENDL4data", "jendl4-n", "jendl4nfy"),
        "sf_endf": os.path.join("JENDL4data", "jendl4-n", "jendl4sfy"),
    },
    "DECAY": {
        "dk_endf": os.path.join("decay", "decay_2012"),
        "hazards": os.path.join("decay", "hazards_2012"),
        "clear": os.path.join("decay", "clear_2012"),
        "a2data": os.path.join("decay", "a2_2012"),
        "absorp": os.path.join("decay", "abs_2012"),
    },
    "DECAY2020": {
        "ind_nuc": os.path.join("decay", "decay_2020_index.txt"),
        "dk_endf": os.path.join("decay", "decay_2020"),
        "hazards": os.path.join("decay", "hazards_2012"),
        "clear": os.path.join("decay", "clear_2012"),
        "a2data": os.path.join("decay", "a2_2012"),
        "absorp": os.path.join("decay", "abs_2012"),
    },
}


@freeze_it
class FilesFile(JSONSerializable):
    def __init__(self, base_dir=os.sep, group=709, projectile=PROJECTILE_NEUTRON):
        self.reset()

        self.__base_dir = base_dir
        self.__group = group
        self.__projectile = projectile

        # defaults
        self.fluxes = "fluxes"
        self.collapxi = "COLLAPX"
        self.collapxo = "COLLAPX"
        self.arrayx = "ARRAYX"

    def reset(self):
        # nuclear data libraries
        self.ind_nuc = NULL_ENTRY
        self.xs_endf = NULL_ENTRY
        self.xs_endfb = NULL_ENTRY
        self.prob_tab = NULL_ENTRY
        self.fy_endf = NULL_ENTRY
        self.asscfy = NULL_ENTRY
        self.dk_endf = NULL_ENTRY
        self.hazards = NULL_ENTRY
        self.clear = NULL_ENTRY
        self.a2data = NULL_ENTRY
        self.absorp = NULL_ENTRY
        self.sf_endf = NULL_ENTRY
        self.sp_endf = NULL_ENTRY
        self.ggbins = NULL_ENTRY
        self.enbins = NULL_ENTRY
        self.xs_extra = NULL_ENTRY

        # eaf nuclear data
        self.crossec = NULL_ENTRY
        self.crossunc = NULL_ENTRY
        self.decay = NULL_ENTRY
        self.fissyld = NULL_ENTRY

        # additional files  - not nuclear data
        self.fluxes = NULL_ENTRY
        self.arb_flux = NULL_ENTRY
        self.collapxi = NULL_ENTRY
        self.collapxo = NULL_ENTRY
        self.arrayx = NULL_ENTRY
        self.files = NULL_ENTRY
        self.input = NULL_ENTRY
        self.graph = NULL_ENTRY
        self.gnuplot = NULL_ENTRY
        self.spec = NULL_ENTRY
        self.output = NULL_ENTRY
        self.tab1 = NULL_ENTRY
        self.tab2 = NULL_ENTRY
        self.tab3 = NULL_ENTRY
        self.tab4 = NULL_ENTRY
        self.runlog = NULL_ENTRY
        self.ind_nuco = NULL_ENTRY
        self.sens = NULL_ENTRY
        self.nucgraph = NULL_ENTRY
        self.nucgnu = NULL_ENTRY

    def to_dict(self):
        d = dict()
        for k, v in self.__dict__.items():
            if "__" not in k and v != NULL_ENTRY:
                d[k] = v

        return d

    def setXS(self, type):
        self._setVar(type, "ind_nuc")
        if type == "EAF2010":
            self._setVar(type, "crossec")
            self._setVar(type, "crossunc")
        else:
            self._setVar(type, "xs_endf")

    def setProbTab(self, type):
        self._setVar(type, "prob_tab")

    def setFissionYield(self, type):
        self._setVar(type, "fy_endf")

    def setDecay(self, type):
        key = "dk_endf"
        if type == "EAF2010":
            key = "decay"

        self._setVar(type, key)

    def setEAF(self):
        self.setXS("EAF2010")
        self.setDecay("EAF2010")
        self.setRegulatory("EAF2010")
        self.setGammaAbsorb("EAF2010")

    def setRegulatory(self, type):
        self._setVar(type, "hazards")
        self._setVar(type, "clear")
        self._setVar(type, "a2data")

    def setGammaAbsorb(self, type):
        self._setVar(type, "absorp")

    def _setVar(self, type, key):
        if type not in NUCLEAR_LIBS and not key in NUCLEAR_LIBS[type]:
            raise PypactException(
                "Cannot set {} library to type {}, does not exist.".format(key, type)
            )

        self.__setattr__(key, os.path.join(self.__base_dir, NUCLEAR_LIBS[type][key]))

    def invalidpaths(self):
        """
        Validate if paths in files file exist
        Return a list of tuples (key, value) that do not exist
        """
        ignore = [
            "collapxi",
            "collapxo",
            "arrayx",
            "tab1",
            "tab2",
            "tab3",
            "tab4",
            "output",
            "ind_nuco",
        ]
        invalid = []
        for k, v in self.to_dict().items():
            if k in ignore:
                continue

            if not v or (not file_exists(v) and not dir_exists(v)):
                invalid.append((k, v))

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
        for k, v in self.to_dict().items():
            f.write(f"{k:<20} {v:<100}\n\n")

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

            # ignore comments
            if k[0] == "#":
                continue

            if k not in self.__dict__:
                raise PypactDeserializeException(
                    "Cannot deserialize files file. Unknown key {0} specified.".format(
                        k
                    )
                )

            if self.__dict__[k] != NULL_ENTRY:
                raise PypactDeserializeException(
                    "Cannot deserialize files file. Repeated key {0} specified.".format(
                        k
                    )
                )

            self.__setattr__(k, data[1])

# control keywords
MAX_CONTROL_KEYWORDS = 32
CONTROL_KEYWORDS = [
    "ALLDISPEN",
    "ATDISPEN",
    "CLOBBER",
    "CNVTYPE",
    "COVARIANCE",
    "CUMFYLD",
    "FISPACT",
    "FULLXS",
    "GETDECAY",
    "GETXS",
    "GRPCONVERT",
    "JSON",
    "LIBVERSION",
    "LIMGRP",
    "LOGLEVEL",
    "MONITOR",
    "NOERROR",
    "NOFISS",
    "PROBTABLE",
    "PROJECTILE",
    "READGG",
    "READSF",
    "SAVELINES",
    "SPEK",
    "SSFCHOOSE",
    "SSFDILUTION",
    "SSFFUEL",
    "SSFGEOMETRY",
    "SSFMASS",
    "USESPALLATION",
    "USEXSEXTRA",
    "XSTHRESHOLD",
]
assert len(CONTROL_KEYWORDS) == MAX_CONTROL_KEYWORDS


# initialisation keywords
MAX_INIT_KEYWORDS = 64
INIT_KEYWORDS = [
    "ATOMS",
    "ATWO",
    "BREMSSTRAHLUNG",
    "CLEAR",
    "CULTAB",
    "DENSITY",
    "DEPLETION",
    "DOSE",
    "END",
    "ERROR",
    "FISCHOOSE",
    "FISYIELD",
    "FLUX",
    "FUEL",
    "FULLXS",
    "GENERIC",
    "GETXS",
    "GRAPH",
    "GROUP",
    "GRPCONVERT",
    "HALF",
    "HAZARDS",
    "INDEXPATH",
    "IRON",
    "LIBVERSION",
    "LOGLEVEL",
    "LOOKAHEAD",
    "MASS",
    "MCSAMPLE",
    "MCSEED",
    "MIND",
    "NOCOMP",
    "NOSORT",
    "NOT1",
    "NOT2",
    "NOT3",
    "NOT4",
    "NUCGRAPH",
    "OVER",
    "PATH",
    "PATHRESET",
    "POWER",
    "PRINTLIB",
    "PROBTABLE",
    "ROUTES",
    "SENSITIVITY",
    "SORTDOMINANT",
    "SPECTRUM",
    "SPLIT",
    "SSFCHOOSE",
    "SSFDILUTION",
    "SSFFUEL",
    "SSFGEOMETRY",
    "SSFMASS",
    "TAB1",
    "TAB2",
    "TAB3",
    "TAB4",
    "TIME",
    "TOLERANCE",
    "UNCERTAINTY",
    "UNCTYPE",
    "USEFISSION",
    "WALL",
]
assert len(INIT_KEYWORDS) == MAX_INIT_KEYWORDS

# inventory keywords
MAX_INVENTORY_KEYWORDS = 41
INVENTORY_KEYWORDS = [
    "ATOMS",
    "DEPLETION",
    "DAYS",
    "END",
    "ENDPULSE",
    "FLUX",
    "FULLXS",
    "GETXS",
    "GRPCONVERT",
    "HOURS",
    "LIBVERSION",
    "LOGLEVEL",
    "MINS",
    "NOSTABLE",
    "NOT1",
    "NOT2",
    "NOT3",
    "NOT4",
    "OVER",
    "PARTITION",
    "PATHRESET",
    "POWER",
    "PROBTABLE",
    "PULSE",
    "RESULT",
    "SECS",
    "SPECTRUM",
    "SSFCHOOSE",
    "SSFDILUTION",
    "SSFFUEL",
    "SSFGEOMETRY",
    "SSFMASS",
    "STEP",
    "TAB1",
    "TAB2",
    "TAB3",
    "TAB4",
    "TIME",
    "WALL",
    "YEARS",
    "ZERO",
]
assert len(INVENTORY_KEYWORDS) == MAX_INVENTORY_KEYWORDS

# over sub-keywords
MAX_OVER_SUBKEYWORDS = 4
OVER_SUBKEYWORDS = [
    "ACROSS",
    "ADCROSS",
    "ADLAM",
    "ALAM",
]
assert len(OVER_SUBKEYWORDS) == MAX_OVER_SUBKEYWORDS

# all FISPACT keywords
MAX_DEPRECATED_KEYWORDS = 15
DEPRECATED_KEYWORDS = [
    "AINPUT",  # deprecated - replaced by GETXS 0 GETDECAY 0
    "ARRAY",  # deprecated - replaced by GETDECAY 0
    "COLLAPSE",  # deprecated - replaced by GETXS 1
    "CONV",  # deprecated - use TOLERANCE instead
    "DOMINANT",  # deprecated - use UNCERTAINTY and SORTDOMINANT instead
    "EAFVERSION",  # deprecated - does nothing, use LIBVERSION instead
    "ENFA",  # deprecated - replaces GETDECAY
    "LEVEL",  # deprecated - does nothing
    "LINA",  # deprecated - replaces 0 for GETDECAY
    "LOOPS",  # deprecated - does nothing
    "NEWFILE",  # deprecated - does nothing
    "NOHEADER",  # deprecated - does nothing
    "SEQNUMBER",  # deprecated - does nothing, SCPR not yet implemented
    "SEQUENTIAL",  # deprecated - does nothing, SCPR not yet implemented
    "TAPA",  # deprecated - replaces 1 for GETDECAY
]
assert len(DEPRECATED_KEYWORDS) == MAX_DEPRECATED_KEYWORDS

# all keywords (no duplicates)
# expected number of keywords
MAX_KEYWORDS = 116
ALL_KEYWORDS = sorted(
    list(
        set(
            CONTROL_KEYWORDS
            + INIT_KEYWORDS
            + INVENTORY_KEYWORDS
            + OVER_SUBKEYWORDS
            + DEPRECATED_KEYWORDS
        )
    )
)
assert len(ALL_KEYWORDS) == MAX_KEYWORDS

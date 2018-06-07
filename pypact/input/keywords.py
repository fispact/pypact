# control keywords
MAX_CONTROL_KEYWORDS = 32
CONTROL_KEYWORDS = [
    'ALLDISPEN',
    'ATDISPEN',
    'CLOBBER',
    'CNVTYPE',
    'COVARIANCE',
    'CUMFYLD',
    'FISPACT',
    'FULLXS',
    'GETDECAY',
    'GETXS',
    'GRPCONVERT',
    'JSON',
    'LIBVERSION',
    'LIMGRP',
    'LOGLEVEL',
    'MONITOR',
    'NOERROR',
    'NOFISS',
    'PROBTABLE',
    'PROJECTILE',
    'READGG',
    'READSF',
    'SAVELINES',
    'SPEK',
    'SSFCHOOSE',
    'SSFDILUTION',
    'SSFFUEL',
    'SSFGEOMETRY',
    'SSFMASS',
    'USESPALLATION',
    'USEXSEXTRA',
    'XSTHRESHOLD'
]
assert len(CONTROL_KEYWORDS) == MAX_CONTROL_KEYWORDS


# initialisation keywords
MAX_INIT_KEYWORDS = 64
INIT_KEYWORDS = [
    'ATOMS',
    'ATWO',
    'BREMSSTRAHLUNG',
    'CLEAR',
    'CULTAB',
    'DENSITY',
    'DEPLETION',
    'DOSE',
    'END',
    'ERROR',
    'FISCHOOSE',
    'FISYIELD',
    'FLUX',
    'FUEL',
    'FULLXS',
    'GENERIC',
    'GETXS',
    'GRAPH',
    'GROUP',
    'GRPCONVERT',
    'HALF',
    'HAZARDS',
    'INDEXPATH',
    'IRON',
    'LIBVERSION',
    'LOGLEVEL',
    'LOOKAHEAD',
    'MASS',
    'MCSAMPLE',
    'MCSEED',
    'MIND',
    'NOCOMP',
    'NOSORT',
    'NOT1',
    'NOT2',
    'NOT3',
    'NOT4',
    'NUCGRAPH',
    'OVER',
    'PATH',
    'PATHRESET',
    'POWER',
    'PRINTLIB',
    'PROBTABLE',
    'ROUTES',
    'SENSITIVITY',
    'SORTDOMINANT',
    'SPECTRUM',
    'SPLIT',
    'SSFCHOOSE',
    'SSFDILUTION',
    'SSFFUEL',
    'SSFGEOMETRY',
    'SSFMASS',
    'TAB1',
    'TAB2',
    'TAB3',
    'TAB4',
    'TIME',
    'TOLERANCE',
    'UNCERTAINTY',
    'UNCTYPE',
    'USEFISSION',
    'WALL',
]
assert len(INIT_KEYWORDS) == MAX_INIT_KEYWORDS

# inventory keywords
MAX_INVENTORY_KEYWORDS = 41
INVENTORY_KEYWORDS = [
    'ATOMS',
    'DEPLETION',
    'DAYS',
    'END',
    'ENDPULSE',
    'FLUX',
    'FULLXS',
    'GETXS',
    'GRPCONVERT',
    'HOURS',
    'LIBVERSION',
    'LOGLEVEL',
    'MINS',
    'NOSTABLE',
    'NOT1',
    'NOT2',
    'NOT3',
    'NOT4',
    'OVER',
    'PARTITION',
    'PATHRESET',
    'POWER',
    'PROBTABLE',
    'PULSE',
    'RESULT',
    'SECS',
    'SPECTRUM',
    'SSFCHOOSE',
    'SSFDILUTION',
    'SSFFUEL',
    'SSFGEOMETRY',
    'SSFMASS',
    'STEP',
    'TAB1',
    'TAB2',
    'TAB3',
    'TAB4',
    'TIME',
    'WALL',
    'YEARS',
    'ZERO',
]
assert len(INVENTORY_KEYWORDS) == MAX_INVENTORY_KEYWORDS

# over sub-keywords
MAX_OVER_SUBKEYWORDS = 4
OVER_SUBKEYWORDS = [
    'ACROSS',
    'ADCROSS',
    'ADLAM',
    'ALAM',
]
assert len(OVER_SUBKEYWORDS) == MAX_OVER_SUBKEYWORDS

# all FISPACT keywords
MAX_DEPRICATED_KEYWORDS = 15
DEPRECIATED_KEYWORDS = [
    'AINPUT',       # depreciated - replaced by GETXS 0 GETDECAY 0
    'ARRAY',        # depreciated - replaced by GETDECAY 0
    'COLLAPSE',     # depreciated - replaced by GETXS 1
    'CONV',         # depreciated - use TOLERANCE instead
    'DOMINANT',     # depreciated - use UNCERTAINTY and SORTDOMINANT instead
    'EAFVERSION',   # depreciated - does nothing, use LIBVERSION instead
    'ENFA',         # depreciated - replaces GETDECAY
    'LEVEL',        # depreciated - does nothing
    'LINA',         # depreciated - replaces 0 for GETDECAY
    'LOOPS',        # depreciated - does nothing
    'NEWFILE',      # depreciated - does nothing
    'NOHEADER',     # depreciated - does nothing
    'SEQNUMBER',    # depreciated - does nothing, SCPR not yet implemented
    'SEQUENTIAL',   # depreciated - does nothing, SCPR not yet implemented
    'TAPA',         # depreciated - replaces 1 for GETDECAY
]
assert len(DEPRECIATED_KEYWORDS) == MAX_DEPRICATED_KEYWORDS

# all keywords (no duplicates)
# expected number of keywords
MAX_KEYWORDS = 116
ALL_KEYWORDS = sorted(list(set(CONTROL_KEYWORDS +
                               INIT_KEYWORDS +
                               INVENTORY_KEYWORDS +
                               OVER_SUBKEYWORDS +
                               DEPRECIATED_KEYWORDS)))
assert len(ALL_KEYWORDS) == MAX_KEYWORDS


# fispact values for projectiles
# do not change this mapping
PROJECTILE_NEUTRON  = 1
PROJECTILE_DEUTERON = 2
PROJECTILE_PROTON  = 3
PROJECTILE_ALPHA    = 4
PROJECTILE_GAMMA    = 5

VALID_PROJECTILES = [
    PROJECTILE_NEUTRON,
    PROJECTILE_DEUTERON,
    PROJECTILE_PROTON,
    PROJECTILE_ALPHA,
    PROJECTILE_GAMMA
]

VALID_PROJECTILE_NAMES = [
    'neutron',
    'deuteron',
    'proton',
    'alpha',
    'gamma'
]

VALID_PROJECTILE_SYMBOLS = [
    'n',
    'd',
    'p',
    'a',
    'g'
]

def get_projectile_name(projectile_value):
    return VALID_PROJECTILE_NAMES[VALID_PROJECTILES.index(projectile_value)]

def get_projectile_symbol(projectile_value):
    return VALID_PROJECTILE_SYMBOLS[VALID_PROJECTILES.index(projectile_value)]

def get_projectile_value(projectile_name):
    return VALID_PROJECTILES[VALID_PROJECTILE_NAMES.index(projectile_name)]

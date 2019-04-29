#!/usr/bin/env python3

import math
import os
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'printlib5.out')

def getZ(zai):
    return math.floor(zai/10000)

with pp.PrintLib5Reader(filename) as output:
    for m in output.spectral_mean_data:
        if getZ(m.zai) == 1:
            print(m.json_serialize())

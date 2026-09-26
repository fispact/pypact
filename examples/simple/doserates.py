#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'reference', 'second_modif.out')

with pp.Reader(filename) as output:
    dr = output[-1].dose_rate
    print(dr.json_serialize())

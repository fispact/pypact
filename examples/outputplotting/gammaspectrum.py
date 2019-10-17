#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'reference', 'test31.out')

# print the gamma spectrum for each time step
with pp.Reader(filename) as output:
    for t in output:
        print(t.gamma_spectrum.json_serialize())


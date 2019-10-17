#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'reference', 'test31.out')

with pp.Reader(filename) as output:
    print(output.json_serialize())

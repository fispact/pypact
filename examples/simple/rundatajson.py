#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test91.out"
)

with pp.Reader(filename) as output:
    rd = output.run_data
    print(rd.json_serialize())

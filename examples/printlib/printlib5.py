#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "printlib5.out"
)

with pp.PrintLib5Reader(filename) as output:
    for m in output.spectral_data:
        if m.zai == 270600:
            print(m.json_serialize())

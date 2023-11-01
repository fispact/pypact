#!/usr/bin/env python3

import os
import pypact as pp

nuclide_name = "Ca41"
filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test127.out"
)

def matcher(nuclide) -> bool:
    return nuclide.name == nuclide_name

with pp.Reader(filename) as output:
    time_and_act = [
        (timestep.cooling_time, nuclide.activity) 
        for timestep in output
        for nuclide in timestep.nuclides
        if matcher(nuclide)
    ]
    print(time_and_act)

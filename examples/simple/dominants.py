#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test31.out"
)

# get last timestep
TIMESTEP = -1

# sort by this property
# atoms, heat, activity, grams, ingestion, etc...
PROPERTY = "atoms"

# take top 10 (dominants)
NDOMINANTS = 10


with pp.Reader(filename) as output:
    doms = pp.dominants(output[TIMESTEP].nuclides, ntop=NDOMINANTS, prop=PROPERTY, show_stable=False)

    print(f"==== TOP {NDOMINANTS} NUCLIDES BY {PROPERTY} ====")
    for nuclide in doms:
        print(f"{nuclide.name:<6} -> {getattr(nuclide, PROPERTY):>10.3e}")

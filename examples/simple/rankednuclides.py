#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test31.out"
)

# sort by this property
# atoms, heat, activity, grams, ingestion, etc...
PROPERTY = "atoms"

# take top 10 (dominants)
NDOMINANTS = 10

with pp.Reader(filename) as output:
    # over all times - not just dominants for one timestep!
    sorted_nuclides = pp.ranked_nuclides(output, ntop=NDOMINANTS, prop=PROPERTY)

    print(sorted_nuclides)

    # todo: need to finish
    print(f"==== TOP {NDOMINANTS} NUCLIDES BY {PROPERTY} ====")
    for n in sorted_nuclides:
        print(n.name, getattr(n, PROPERTY))

#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test31.out"
)

# get dominants at third (0-based) timestep
TIMESTEP = 2

# sort by this property
# atoms, heat, activity, grams, ingestion, etc...
PROPERTY = "atoms"

# take top 10 (dominants)
NDOMINANTS = 10


with pp.Reader(filename) as output:
    assert len(output) > TIMESTEP

    sorted_nuclides = sorted(
        output[TIMESTEP].nuclides,
        key=lambda x: getattr(x, PROPERTY),
        # descending for top ranked - use False for bottom ranked
        reverse=True,
    )

    print(f"==== TOP {NDOMINANTS} NUCLIDES BY {PROPERTY} ====")
    for n in sorted_nuclides[:NDOMINANTS]:
        print(n.name, getattr(n, PROPERTY))

#!/usr/bin/env python3

import os
import pypact as pp

# change the filename here
runname = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test121.out"
)

# if you change this you must also
# change the list at the bottom!
headers = [
    "nuclides",
    "activity (Bq)",
    "grams",
    "alpha heat (kW)",
    "beta heat (kW)",
    "gamma heat (kW)",
    "cumulative time (secs)",
    "is irradiation",
]


def fmt(items):
    str = f"{items[0]:>20}"
    for i in items:
        str += f", {i:>20}"
    return f"{str}\n"


with pp.Reader(runname) as output:
    with open("csvexample.csv", "wt") as f:
        f.write(fmt(headers))
        for t in output:
            for n in t.nuclides:
                # if you changed the headers you must change this too!!
                #
                f.write(
                    fmt(
                        [
                            n.name,
                            n.activity,
                            n.grams,
                            n.alpha_heat,
                            n.beta_heat,
                            n.gamma_heat,
                            t.currenttime,
                            t.isirradiation,
                        ]
                    )
                )

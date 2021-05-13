#!/usr/bin/env python3

import os
import pypact as pp

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "printlib4.out"
)

with pp.PrintLib4Reader(filename) as output:
    # sort by ascending MT (warning sort is a bit slow!)
    output.cross_sections.sort(key=lambda x: x.findmt)

    for m in output.cross_sections:
        # get all reactions for C10
        if m.nuclide == "C10":
            print(
                "{:4} {:9} = {:.4e} +- {:.4e}".format(
                    m.findmt, m.reaction, m.xs, m.delta_xs
                )
            )

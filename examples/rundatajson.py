#!/usr/bin/env python3

import os

import pypact.reader as pr

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test91.out')

output = pr.Reader()(filename)

print(output.run_data.json_serialize())

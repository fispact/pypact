#!/usr/bin/env python3

import os

import pypact.reader as pr

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test91.out')

with pr.Reader(filename) as output:
    rd = output.run_data
    print(rd.json_serialize())

#!/usr/bin/env python3

import pypact as pp


# read a files file
ff = pp.FilesFile()
pp.deserialize(ff, "files")

print("Decay data: ", ff.dk_endf)
print("Condense output file: ", ff.arrayx)

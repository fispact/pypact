#!/usr/bin/env python3

import os
import pypact as pp


# read a files file
ff = pp.FilesFile()
pp.from_file(ff, os.path.join('files', 'filesfileexample'))

print("Decay data: ", ff.dk_endf)
print("Condense output file: ", ff.arrayx)

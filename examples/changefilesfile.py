#!/usr/bin/env python3

import os
import pypact as pp


old_path = '/FISPACT-II'
new_path = '/new/path/to/FISPACT-II/nuclear_data'

ff = pp.FilesFile()
pp.from_file(ff, os.path.join('files', 'filesfileexample'))

# verbose output for old files file
print(ff.json_serialize())

# change paths here
for k, v in ff.to_dict().items():
    if old_path in v:
        new_v = v.replace(old_path, new_path)
        ff.__setattr__(k, new_v)

# verbose output for new files file
print(ff.json_serialize())

# validate new paths
print(" * Invalid paths are: ")
for k, p in ff.invalidpaths():
    print("Key: {}, Path: {}".format(k, p))

pp.to_file(ff, os.path.join('files', 'filesfileexamplenew'))

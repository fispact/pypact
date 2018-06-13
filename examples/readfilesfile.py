import pypact as pp

filename = "dummyfiles"

# read a files file
ff = pp.FilesFile()
pp.deserialize(ff, filename)

print("Decay data: ", ff.dk_endf)
print("Condense output file: ", ff.arrayx)

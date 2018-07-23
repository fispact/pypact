import os
import subprocess

from pypact.reader import Reader
from pypact.input.serialization import serialize
from pypact.util.file import file_remove
from pypact.util.decorators import timeit

FISPACT_EXE_PATH = os.getenv('FISPACT', os.path.join(os.sep, 'opt', 'fispact', 'bin', 'fispact'))


@timeit
def compute(input, files, fluxes,
            input_filename="fispacttemp.i",
            files_filename="fispacttemp.files",
            fluxes_filename="fispacttemp.fluxes",
            cleanup=True):

    files.fluxes = fluxes_filename
    runname = input_filename.strip('.i')
    
    # write all files
    serialize(input, input_filename)
    serialize(files, files_filename)
    serialize(fluxes, fluxes_filename)

    # run fispact
    proc = subprocess.check_call("{} {} {}".format(FISPACT_EXE_PATH, runname, files_filename), shell=True)

    # check for log file
    logfile = "{}.log".format(runname)
    if not os.path.isfile(logfile):
        raise RuntimeError("No log file produced.")
    
    # clean up input and log files - keep output file
    if cleanup:
        file_remove(input_filename)
        file_remove(files_filename)
        file_remove(fluxes_filename)
        file_remove(logfile)

    outfile = "{}.out".format(runname)
    with Reader(outfile) as output:
        return output


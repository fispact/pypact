import os
import subprocess

from pypact.reader import Reader
from pypact.input.serialization import to_file
from pypact.util.file import file_remove, file_exists
from pypact.util.exceptions import PypactFispactExecutableNotFoundException
from pypact.util.decorators import time_it

FISPACT_EXE_PATH = os.getenv('FISPACT', os.path.join(os.sep, 'opt', 'fispact', 'bin', 'fispact'))


@time_it
def compute(input, files, fluxes,
            input_filename="fispacttemp.i",
            files_filename="fispacttemp.files",
            fluxes_filename="fispacttemp.fluxes",
            cleanup=True):

    files.fluxes = fluxes_filename
    runname = input_filename.strip('.i')
    
    # write all files
    to_file(input, input_filename)
    to_file(files, files_filename)
    to_file(fluxes, fluxes_filename)

    # run fispact
    if not file_exists(FISPACT_EXE_PATH):
        raise PypactFispactExecutableNotFoundException("Cannot find FISPACT-II binary. Instead got {}".format(FISPACT_EXE_PATH))

    print("* Running FISPACT-II...")
    proc = subprocess.check_call("{} {} {}".format(FISPACT_EXE_PATH, runname, files_filename), shell=True)
    print("* Computation complete")

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


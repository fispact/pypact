#!/usr/bin/env python3
import sys
import argparse
import os

from pypact.util.exceptions import PypactException
from pypact.input.filesfile import FilesFile
from pypact.input.serialization import serialize, deserialize


def main():
    # Command line argument support
    parser = argparse.ArgumentParser(description='Files File Maker')
    parser.add_argument('filesfile', type=argparse.FileType('w'),
                        help='The fispact files file to create (files)')
    parser.add_argument("-d", "--basedir", type=str,
                        help='The base directory')
    args = parser.parse_args()

    if args.basedir is None:
        args.basedir = os.sep
    
    filename = args.filesfile.name

    try:
        ff = FilesFile(base_dir=args.basedir)

        # set paths here, example only now
        ff.setXS('TENDL2017')
        ff.setFissionYield('GEFY52')
        ff.setProbTab('TENDL2015')
        ff.setDecay('JEFF33')
        ff.setRegulatory('DECAY')
        ff.setGammaAbsorb('DECAY')
        
        invalids = ff.validate()
        if invalids:
            print("Warning: Invalid paths in files file!")
            for i in invalids:
                print(" *** Missing {}: {}".format(i[0], i[1]))

        # write to file
        serialize(ff, filename)
    except PypactException as err:
        print("Pypact error: {}".format(err))
    except OSError as err:
        print("OS error: {}".format(err))
    except ValueError as err:
        print(err)
    except:
        print("Unexpected error:", sys.exc_info()[1])


if __name__ == "__main__":
    main()

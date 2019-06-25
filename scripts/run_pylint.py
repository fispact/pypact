# -*- coding: utf-8 -*-
"""Script to run the pylinter on the source code

This script wraps pylint to check the score is above a threshold.
This is not currently available 'out of the box' for pylint, hence 
the need for this script.

Useage is the same as the pylint command line tool, but now accepts
an additional arg: --score-threshold. The default is 4 if not set.

Example:
    To run with this package using the lint config:

        $ python3 scripts/runpylint.py -j4 \
            --rcfile=.pylintrc \
            --output-format=text \
            --score-threshold=4 \
                pypact &> pylint.txt

"""
import argparse
import sys
from pylint import lint, testutils


parser = argparse.ArgumentParser(description="score checker for pylint", allow_abbrev=False)
parser.add_argument('--score-threshold', dest='threshold', type=float, default=5,
                    help='If the final score is less than the threshold then'
                    ' exit with pylint\'s exitcode, otherwise all is fine.')

args, otherargs = parser.parse_known_args()
threshold = args.threshold
run = lint.Run(otherargs, do_exit=False)
score = run.linter.stats['global_note']

# if less then return pylint error code
print("Pylint score: {:.2f}".format(score))
if score < threshold:
    print("Pylint score is too low, pass threshold is {:.2f}".format(threshold))
    sys.exit(run.linter.msg_status)

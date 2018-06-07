import unittest

from tests.util.filetest import FileUnitTest
from tests.util.linestest import LinesUnitTest
from tests.util.numericaltest import NumericalUnitTest
from tests.util.propertyfindertest import PropertyFinderUnitTest

from tests.output.doseratetest import DoseRateUnitTest
from tests.output.rundatatest import RunDataUnitTest
from tests.output.nuclidestest import NuclidesUnitTest
from tests.output.timesteptest import TimeStepUnitTest
from tests.output.outputtest import OutputUnitTest

from tests.input.keywordstest import KeywordsUnitTest

from tests.library.nuclidelibtest import NuclideLibUnitTest


def main():
    unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite())

if __name__ == '__main__':
    unittest.main()

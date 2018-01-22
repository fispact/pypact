import unittest
from pypact.tests.material.isotopetest import IsotopeUnitTest
from pypact.tests.material.elementtest import ElementUnitTest
from pypact.tests.util.filetest import FileUnitTest
from pypact.tests.util.linestest import LinesUnitTest
from pypact.tests.util.numericaltest import NumericalUnitTest
from pypact.tests.util.propertyfindertest import PropertyFinderUnitTest
from pypact.tests.output.doseratetest import DoseRateUnitTest
from pypact.tests.output.rundatatest import RunDataUnitTest
from pypact.tests.output.nuclidestest import NuclidesUnitTest
from pypact.tests.output.timesteptest import TimeStepUnitTest
from pypact.tests.output.outputtest import OutputUnitTest

def main():
    unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite())


if __name__ == '__main__':
    unittest.main()

import math
import pypact as pp

from tests.testerbase import Tester


class InputDataUnitTest(Tester):
    
    def test_default(self):
        id = pp.InputData(name="test_default")
        self.assertEqual("test_default", id.name, "Assert name")

    def test_default_tofile(self):
        id = pp.InputData(name="test_default")
        
        filename = '_PYPACT_TEST_writeinputfile_default'
        pp.to_file(id, filename)

    def test_alloptions_tofile(self):
        id = pp.InputData(name="test_default")
        
        id.overwriteExisting(True)
        id.enableJSON(True)
        id.enableInitialInventoryInOutput(True)
        id.enableHalflifeInOutput(True)
        id.enableHazardsInOutput(True)
        id.readXSData(709, binary=True)
        id.useEAFLibraries(False)
        id.useCumulativeFissionYieldData(True)
        id.includeClearanceData(True)
        id.readDecayData(True)
        id.approxGammaSpectrum(True)
        id.ignoreUncertainties()
        id.setXSThreshold(1e-14)
        id.setProjectile(pp.PROJECTILE_PROTON)
        id.readGammaGroup()
        id.enableSystemMonitor()
        id.setAtomsThreshold(3.4e-8)
        id.addIrradiation(5.4, 1.1e12)
        id.addIrradiation(10.4, 1.3e12)
        id.addCooling(6.22)
        id.addCooling(12.22)
        id.addCooling(4.5)
        id.setLogLevel(pp.LOG_SEVERITY_TRACE)
        id.setDensity(1.3)
        id.setMass(45.7)
        id.addElement("He", 0.9)
        id.addElement("Fe", 0.1)

        filename = '_PYPACT_TEST_writeinputfile_alloptions'
        pp.to_file(id, filename)
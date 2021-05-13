import math
import pypact as pp

from tests.testerbase import Tester


class FluxesFileUnitTest(Tester):
    
    def test_default(self):
        ff = pp.FluxesFile(name="test_default", norm=1.0)
        self.assertEqual("test_default", ff.name, "Assert name")
        self.assertEqual(1.0, ff.norm, "Assert norm")
        self.assertEqual(0, len(ff.boundaries), "Assert default boundaries")
        self.assertEqual(0, len(ff.values), "Assert default values")
        self.assertEqual(0, len(ff.midPointEnergies), "Assert default mid point boundaries")
    
    def test_set_1102group_only(self):
        ff = pp.FluxesFile(name="test_set_1102group_only", norm=0.56)
        
        group = 1102
        # negative sign means ascending energies (legacy reasons)
        g = pp.ALL_GROUPS[-group]
        
        ff.setGroup(group)
        self.assertEqual(group, len(ff), "Assert group")
        self.assertEqual(group+1, len(ff.boundaries), "Assert group boundaries")
        self.assertEqual(group, len(ff.values), "Assert group default values")
        self.assertEqual(group, len(ff.midPointEnergies), "Assert group mid point boundaries")
        
        for i in range(0, group):
            expectedMidPoint = (g[i+1] + g[i])/2.0
            self.assertEqual(0.0, ff.values[i], "Assert bin value {}".format(i))
            self.assertEqual(expectedMidPoint, ff.midPointEnergies[i], "Assert bin mid point {}".format(i))
    
    def test_set_709group_setValid(self):
        ff = pp.FluxesFile(name="test_set_709group_setValid", norm=1.0)

        group = 709
        # negative sign means ascending energies (legacy reasons)
        g = pp.ALL_GROUPS[-group]
        
        ff.setGroup(group)
        self.assertEqual(group, len(ff), "Assert group")
        self.assertEqual(group+1, len(ff.boundaries), "Assert group boundaries")
        self.assertEqual(group, len(ff.values), "Assert group default values")
        self.assertEqual(group, len(ff.midPointEnergies), "Assert group mid point boundaries")
        
        energy1 = 10e6
        value1 = 3.4
        energy2 = 2.3e6
        value2 = 89.4e3
        ff.setValue(energy1, value1)
        ff.setValue(energy2, value2)
        foundBin1 = False
        foundBin2 = False
        for i in range(0, group):
            if not foundBin1 and g[i+1] > energy1:
                self.assertEqual(value1, ff.values[i], "Assert bin value {}".format(i))
                foundBin1 = True
            elif not foundBin2 and g[i+1] > energy2:
                self.assertEqual(value2, ff.values[i], "Assert bin value {}".format(i))
                foundBin2 = True
            else:
                # assert defaults
                self.assertEqual(0.0, ff.values[i], "Assert bin value {}".format(i))

    def test_reset(self):
        ff = pp.FluxesFile(name="test_reset", norm=0.7)
        
        group = 709
        ff.setGroup(group)
        self.assertEqual(group, len(ff), "Assert group")
        self.assertEqual(group+1, len(ff.boundaries), "Assert group boundaries")
        self.assertEqual(group, len(ff.values), "Assert group default values")
        self.assertEqual(group, len(ff.midPointEnergies), "Assert group mid point boundaries")
        
        ff.setValue(3.5e5, 6.7)
        ff.setValue(5.5e5, 16.7)
        ff.setValue(8.9e5, 26.17)
    
        ff.reset()
        
        self.assertEqual("test_reset", ff.name, "Assert name")
        self.assertEqual(1.0, ff.norm, "Assert norm")
        self.assertEqual(0, len(ff.boundaries), "Assert default boundaries")
        self.assertEqual(0, len(ff.values), "Assert default values")
        self.assertEqual(0, len(ff.midPointEnergies), "Assert default mid point boundaries")

    def test_set_162_writeread(self):
        ff = pp.FluxesFile(name="test_set_162_writeread", norm=1.0)
        
        group = 162
        ff.setGroup(group)
        
        energy1 = 10e5
        value1 = 3.4
        energy2 = 2.3e6
        value2 = 89.4e3
        ff.setValue(energy1, value1)
        ff.setValue(energy2, value2)
        
        self.assertEqual(group, len(ff), "Assert group")

        # write to file
        filename = "_PYPACT_TEST_set_162_writeread_fluxes"
        pp.to_file(ff, filename)

        ff.reset()
        self.assertEqual(0, len(ff), "Assert group")
        self.assertEqual("test_set_162_writeread", ff.name, "Assert name")
        self.assertEqual(1.0, ff.norm, "Assert norm")
        self.assertEqual(0, len(ff.boundaries), "Assert default boundaries")
        self.assertEqual(0, len(ff.values), "Assert default values")
        self.assertEqual(0, len(ff.midPointEnergies), "Assert default mid point boundaries")
        
        # read from file
        pp.from_file(ff, filename)
        self.assertEqual(group, len(ff), "Assert group")
        self.assertEqual(group+1, len(ff.boundaries), "Assert boundaries length")
        self.assertEqual(group, len(ff.values), "Assert values length")
        self.assertEqual(group, len(ff.midPointEnergies), "Assert mid point boundaries length")

        # get index of value1
        v1 = [i for i, j in enumerate(ff.values) if j == value1]
        self.assertEqual(1, len(v1), "Assert value1 is unique")
        self.assertTrue(ff.boundaries[v1[0]+1] > energy1 and ff.boundaries[v1[0]] <= energy1, "Assert value1 energy")

        # get index of value2
        v2 = [i for i, j in enumerate(ff.values) if j == value2]
        self.assertEqual(1, len(v2), "Assert value2 is unique")
        self.assertTrue(ff.boundaries[v2[0]+1] > energy2 and ff.boundaries[v2[0]] <= energy2, "Assert value2 energy")

    def test_set_arb161_writeread(self):
        ff = pp.ArbFluxesFile(name="test_set_arb161_writeread", norm=1.0)
        
        # create some cutoms bounds in ascending order
        group = 161
        bounds = [g for g in range(0, group+1)]
        ff.setGroup(bounds)
        
        # set some values at desired energies
        energy1 = 14
        value1 = 23.34
        energy2 = 100.4
        value2 = 189.4e3
        ff.setValue(energy1, value1)
        ff.setValue(energy2, value2)
        
        # assert bins values set at energies
        self.assertEqual(group, len(ff), "Assert group")
        self.assertEqual(0.0, ff.values[0], "Assert first value is 0")
        self.assertEqual(0.0, ff.values[13], "Assert first value is 0")
        self.assertEqual(value1, ff.values[14], "Assert 15th value is {}".format(value1))
        self.assertEqual(0.0, ff.values[15], "Assert 16th value is 0")
        self.assertEqual(0.0, ff.values[99], "Assert 100th value is 0")
        self.assertEqual(value2, ff.values[100], "Assert 101st value is {}".format(value2))
        self.assertEqual(0.0, ff.values[101], "Assert 102nd value is 0")

        # write to file
        filename = "_PYPACT_TEST_set_arb161_writeread_fluxes"
        pp.to_file(ff, filename)

        ff.reset()
        self.assertEqual("test_set_arb161_writeread", ff.name, "Assert name")
        self.assertEqual(1.0, ff.norm, "Assert norm")
        self.assertEqual(0, len(ff.boundaries), "Assert default boundaries")
        self.assertEqual(0, len(ff.values), "Assert default values")
        self.assertEqual(0, len(ff.midPointEnergies), "Assert default mid point boundaries")
        
        pp.from_file(ff, filename)
        self.assertEqual(group+1, len(ff.boundaries), "Assert boundaries length")
        self.assertEqual(group, len(ff.values), "Assert values length")
        self.assertEqual(group, len(ff.midPointEnergies), "Assert mid point boundaries length")

        # get index of value1
        v1 = [i for i, j in enumerate(ff.values) if j == value1]
        self.assertEqual(1, len(v1), "Assert value1 is unique")
        self.assertTrue(ff.boundaries[v1[0]+1] > energy1 and ff.boundaries[v1[0]] <= energy1, "Assert value1 energy")

        # get index of value2
        v2 = [i for i, j in enumerate(ff.values) if j == value2]
        self.assertEqual(1, len(v2), "Assert value2 is unique")
        self.assertTrue(ff.boundaries[v2[0]+1] > energy2 and ff.boundaries[v2[0]] <= energy2, "Assert value2 energy")

        self.assertEqual(group, len(ff), "Assert group")
        self.assertEqual(0.0, ff.values[0], "Assert first value is 0")
        self.assertEqual(0.0, ff.values[13], "Assert first value is 0")
        self.assertEqual(value1, ff.values[14], "Assert 15th value is {}".format(value1))
        self.assertEqual(0.0, ff.values[15], "Assert 16th value is 0")
        self.assertEqual(0.0, ff.values[99], "Assert 100th value is 0")
        self.assertEqual(value2, ff.values[100], "Assert 101st value is {}".format(value2))
        self.assertEqual(0.0, ff.values[101], "Assert 102nd value is 0")



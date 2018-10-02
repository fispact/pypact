import os
import pypact as pp

from tests.output.baseoutputtest import BaseOutputUnitTest
from tests.output.doseratetest import DoseRateAssertor
from tests.output.nuclidestest import NuclidesAssertor

from tests.testerbase import Tester, REFERENCE_DIR
from pypact.output.timestep import TimeStep

filename_test121out = os.path.join(REFERENCE_DIR, "test91.out")
filerecord121 = pp.FileRecord(filename_test121out)

ds_assertor = DoseRateAssertor()
nuc_assertor = NuclidesAssertor()
tester = Tester()

def assert_inventory(inv, compareinv):
    tester.assertValueAndType(inv, TimeStep, 'total_displacement_rate', float, compareinv.total_displacement_rate)
    tester.assertValueAndType(inv, TimeStep, 'time', float, compareinv.total_displacement)


def assert_timestep(inv, timestep):
    ds_assertor.assert_timestep(inv.dose_rate, timestep)
    nuc_assertor.assert_timestep(inv.nuclides, timestep)

    # Let's test some key timesteps
    # much too time consuming to test all timesteps
    if timestep == 1:
        assert_inventory(inv, timestep_1_inv())

def timestep_1_inv():
    inv = TimeStep()
    inv.total_displacement_rate = 2.11414E-09
    inv.time = 0.0
    return inv


class TimeStepUnitTest(BaseOutputUnitTest):

    def test_fispact_deserialize(self):

        def func(ts, i):
            ts.fispact_deserialize(filerecord121, i)
            assert_timestep(ts, i)

        self._wrapper(func)

    def test_fispact_readwriteread(self):

        def func(ts, i):
            # deserialize from standard output
            ts.fispact_deserialize(self.filerecord91, i)
            assert_timestep(ts, i)

            # serialize to JSON
            j = ts.json_serialize()

            # deserialize JSON and compare to original
            newts = TimeStep()
            newts.json_deserialize(j)
            assert_timestep(newts, i)

        self._wrapper(func)

    def _wrapper(self, func):

        ts = TimeStep()
        self.assertor.assert_defaults(ts)

        for i in range(-100, 100):
            func(ts, i)

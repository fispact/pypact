from tests.output.baseoutputtest import BaseOutputUnitTest
from tests.output.doseratetest import DoseRateAssertor
from tests.output.nuclidestest import NuclidesAssertor

from pypact.output.timestep import TimeStep


class TimeStepAssertor(BaseOutputUnitTest):
    ds_assertor = DoseRateAssertor()
    nuc_assertor = NuclidesAssertor()

    def assert_defaults(self, timestep):
        ts = TimeStep()
        ts.irradiation_time = 0.0
        ts.cooling_time = 0.0
        ts.flux = 0.0
        ts.total_heat = 0.0
        ts.alpha_heat = 0.0
        ts.beta_heat = 0.0
        ts.gamma_heat = 0.0
        ts.ingestion_dose = 0.0
        ts.inhalation_dose = 0.0
        ts.initial_mass = 0.0
        ts.total_mass = 0.0
        ts.total_activity = 0.0
        ts.total_activity_exclude_trit = 0.0
        self.assert_inventory(timestep, ts)

        self.ds_assertor.assert_defaults(timestep.dose_rate)
        self.nuc_assertor.assert_defaults(timestep.nuclides)

    def assert_inventory(self, inv, compareinv):
        self.assertValueAndType(inv, TimeStep, 'irradiation_time', float, compareinv.irradiation_time)
        self.assertValueAndType(inv, TimeStep, 'cooling_time', float, compareinv.cooling_time)
        self.assertValueAndType(inv, TimeStep, 'flux', float, compareinv.flux)
        self.assertValueAndType(inv, TimeStep, 'total_heat', float, compareinv.total_heat)
        self.assertValueAndType(inv, TimeStep, 'alpha_heat', float, compareinv.alpha_heat)
        self.assertValueAndType(inv, TimeStep, 'beta_heat', float, compareinv.beta_heat)
        self.assertValueAndType(inv, TimeStep, 'gamma_heat', float, compareinv.gamma_heat)
        self.assertValueAndType(inv, TimeStep, 'initial_mass', float, compareinv.initial_mass)
        self.assertValueAndType(inv, TimeStep, 'ingestion_dose', float, compareinv.ingestion_dose)
        self.assertValueAndType(inv, TimeStep, 'total_mass', float, compareinv.total_mass)
        self.assertValueAndType(inv, TimeStep, 'inhalation_dose', float, compareinv.inhalation_dose)
        self.assertValueAndType(inv, TimeStep, 'total_activity', float, compareinv.total_activity)
        self.assertValueAndType(inv, TimeStep, 'total_activity_exclude_trit', float, compareinv.total_activity_exclude_trit)

    def assert_timestep(self, inv, timestep):
        self.ds_assertor.assert_timestep(inv.dose_rate, timestep)
        self.nuc_assertor.assert_timestep(inv.nuclides, timestep)

        # Let's test some key timesteps
        # much too time consuming to test all timesteps
        if timestep == 1:
            self.assert_inventory(inv, timestep_1_inv())
        elif timestep == 2:
            self.assert_inventory(inv, timestep_2_inv())
        elif timestep == 14:
            self.assert_inventory(inv, timestep_14_inv())
        elif 16 > timestep > 2:
            return
        else:
            self.assert_defaults(inv)


def timestep_1_inv():
    inv = TimeStep()
    inv.irradiation_time = 0.0
    inv.cooling_time = 0.0
    inv.flux = 3.3400E+10
    inv.alpha_heat = 1.00026E-08
    inv.beta_heat = 3.98609E-11
    inv.gamma_heat = 6.71486E-11
    inv.total_heat = inv.alpha_heat + inv.beta_heat + inv.gamma_heat
    inv.ingestion_dose = 6.59242E-01
    inv.inhalation_dose = 1.17557E+02
    inv.initial_mass = 1.00067E+00
    inv.total_mass = 1.00067E+00
    inv.total_activity = 1.45396E+07
    inv.total_activity_exclude_trit = 1.45396E+07
    return inv


def timestep_2_inv():
    inv = TimeStep()
    inv.irradiation_time = 2.6298E+06
    inv.cooling_time = 0.0
    inv.flux = 3.3400E+10
    inv.alpha_heat = 1.00026E-08
    inv.beta_heat = 1.09700E-09
    inv.gamma_heat = 1.12065E-10
    inv.total_heat = inv.alpha_heat + inv.beta_heat + inv.gamma_heat
    inv.ingestion_dose = 6.84076E-01
    inv.inhalation_dose = 1.17614E+02
    inv.initial_mass = 1.00067E+00
    inv.total_mass = 1.00067E+00
    inv.total_activity = 3.11345E+07
    inv.total_activity_exclude_trit = 3.11345E+07
    return inv


def timestep_14_inv():
    inv = TimeStep()
    inv.irradiation_time = 2.6298E+06 + 5.2596E+06 + 7.8894E+06 + 1.5779E+07 \
                     + 1.5779E+07 + 1.5779E+07
    inv.cooling_time = 6.0000E+01 + 8.6400E+04 + 2.5434E+06 + 1.3149E+07 \
                       + 1.5779E+07 + 6.3115E+07 + 6.3115E+07
    inv.flux = 0.0000E+00
    inv.alpha_heat = 1.00031E-08
    inv.beta_heat = 1.80108E-09
    inv.gamma_heat = 1.36712E-10
    inv.total_heat = inv.alpha_heat + inv.beta_heat + inv.gamma_heat
    inv.ingestion_dose = 7.01423E-01
    inv.inhalation_dose = 1.17728E+02
    inv.initial_mass = 1.00067E+00
    inv.total_mass = 1.00067E+00
    inv.total_activity = 4.11571E+07
    inv.total_activity_exclude_trit = 4.11571E+07
    return inv


class TimeStepUnitTest(BaseOutputUnitTest):

    assertor = TimeStepAssertor()

    def test_fispact_deserialize(self):

        def func(ts, i):
            ts.fispact_deserialize(self.filerecord91, i)
            self.assertor.assert_timestep(ts, i)

        self._wrapper(func)

    def test_fispact_readwriteread(self):

        def func(ts, i):
            # deserialize from standard output
            ts.fispact_deserialize(self.filerecord91, i)
            self.assertor.assert_timestep(ts, i)

            # serialize to JSON
            j = ts.json_serialize()

            # reset object
            newts = TimeStep()
            self.assertor.assert_defaults(newts)

            # deserialize JSON and compare to original
            newts.json_deserialize(j)
            self.assertor.assert_timestep(newts, i)

        self._wrapper(func)

    def _wrapper(self, func):

        ts = TimeStep()
        self.assertor.assert_defaults(ts)

        for i in range(-100, 100):
            func(ts, i)

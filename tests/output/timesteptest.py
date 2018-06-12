from tests.output.baseoutputtest import BaseOutputUnitTest
from tests.output.doseratetest import DoseRateAssertor
from tests.output.nuclidestest import NuclidesAssertor

import pypact as pp


class TimeStepAssertor(BaseOutputUnitTest):
    ds_assertor = DoseRateAssertor()
    nuc_assertor = NuclidesAssertor()

    def assert_defaults(self, timestep):
        ts = pp.TimeStep()
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
        ts.number_of_fissions = 0.0
        ts.burnup = 0.0
        ts.total_activity = 0.0
        ts.total_activity_exclude_trit = 0.0
        self.assert_inventory(timestep, ts)

        self.ds_assertor.assert_defaults(timestep.dose_rate)
        self.nuc_assertor.assert_defaults(timestep.nuclides)

    def assert_inventory(self, inv, compareinv):
        self.assertValueAndType(inv, pp.TimeStep, 'irradiation_time', float, compareinv.irradiation_time)
        self.assertValueAndType(inv, pp.TimeStep, 'cooling_time', float, compareinv.cooling_time)
        self.assertValueAndType(inv, pp.TimeStep, 'flux', float, compareinv.flux)
        self.assertValueAndType(inv, pp.TimeStep, 'total_heat', float, compareinv.total_heat)
        self.assertValueAndType(inv, pp.TimeStep, 'alpha_heat', float, compareinv.alpha_heat)
        self.assertValueAndType(inv, pp.TimeStep, 'beta_heat', float, compareinv.beta_heat)
        self.assertValueAndType(inv, pp.TimeStep, 'gamma_heat', float, compareinv.gamma_heat)
        self.assertValueAndType(inv, pp.TimeStep, 'initial_mass', float, compareinv.initial_mass)
        self.assertValueAndType(inv, pp.TimeStep, 'ingestion_dose', float, compareinv.ingestion_dose)
        self.assertValueAndType(inv, pp.TimeStep, 'total_mass', float, compareinv.total_mass)
        self.assertValueAndType(inv, pp.TimeStep, 'number_of_fissions', float, compareinv.number_of_fissions)
        self.assertValueAndType(inv, pp.TimeStep, 'burnup', float, compareinv.burnup)
        self.assertValueAndType(inv, pp.TimeStep, 'inhalation_dose', float, compareinv.inhalation_dose)
        self.assertValueAndType(inv, pp.TimeStep, 'total_activity', float, compareinv.total_activity)
        self.assertValueAndType(inv, pp.TimeStep, 'total_activity_exclude_trit', float, compareinv.total_activity_exclude_trit)

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
    inv = pp.TimeStep()
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
    inv.number_of_fissions = 0.0E+00
    inv.burnup = 0.0E+00
    inv.total_activity = 1.45396E+07
    inv.total_activity_exclude_trit = 1.45396E+07
    return inv


def timestep_2_inv():
    inv = pp.TimeStep()
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
    inv.number_of_fissions = 0.0E+00
    inv.burnup = 0.0E+00
    inv.total_activity = 3.11345E+07
    inv.total_activity_exclude_trit = 3.11345E+07
    return inv


def timestep_14_inv():
    inv = pp.TimeStep()
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
    inv.number_of_fissions = 0.0E+00
    inv.burnup = 0.0E+00
    inv.total_activity = 4.11571E+07
    inv.total_activity_exclude_trit = 4.11571E+07
    return inv


class TimeStepUnitTest(BaseOutputUnitTest):

    assertor = TimeStepAssertor()

    def test_fission_example(self):

        ts = pp.TimeStep()

        ts.fispact_deserialize(self.filerecord_fission, 1)
        self.assertEquals(ts.alpha_heat, 7.22533E-10, "Assert alpha heat")
        self.assertEquals(ts.number_of_fissions, 0.0, "Assert number of fissions is zero")
        self.assertEquals(ts.burnup, 0.0, "Assert burnup is zero")

        ts.fispact_deserialize(self.filerecord_fission, 2)
        self.assertEquals(ts.alpha_heat, 7.38131E-10, "Assert alpha heat")
        self.assertEquals(ts.number_of_fissions, 6.73186E+09, "Assert number of fissions is non zero")
        self.assertEquals(ts.burnup, 2.93608E-11, "Assert burnup is non zero")

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
            newts = pp.TimeStep()
            self.assertor.assert_defaults(newts)

            # deserialize JSON and compare to original
            newts.json_deserialize(j)
            self.assertor.assert_timestep(newts, i)

        self._wrapper(func)

    def _wrapper(self, func):

        ts = pp.TimeStep()
        self.assertor.assert_defaults(ts)

        for i in range(-100, 100):
            func(ts, i)

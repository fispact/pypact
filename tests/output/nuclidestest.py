from tests.output.baseoutputtest import BaseOutputUnitTest

from pypact.output.nuclides import Nuclides
from pypact.output.nuclide import Nuclide


class NuclidesAssertor(BaseOutputUnitTest):

    def assert_defaults(self, nuclides):
        self.assertEqual(len(nuclides), 0)

    def assert_nuclides(self, nuclides, list):
        self.assertEqual(len(nuclides), len(list))

        for i in range(0, len(list)):
            self.assert_nuclide(nuclides[i], list[i])

    def assert_nuclide(self, nuclide, comparenuclide):
        self.assertValueAndType(nuclide, Nuclide, 'element', str, comparenuclide.element)
        self.assertValueAndType(nuclide, Nuclide, 'isotope', int, comparenuclide.isotope)
        self.assertValueAndType(nuclide, Nuclide, 'state', str, comparenuclide.state)
        self.assertValueAndType(nuclide, Nuclide, 'half_life', float, comparenuclide.half_life)
        self.assertValueAndType(nuclide, Nuclide, 'grams', float, comparenuclide.grams)
        self.assertValueAndType(nuclide, Nuclide, 'activity', float, comparenuclide.activity)
        self.assertValueAndType(nuclide, Nuclide, 'heat', float, comparenuclide.heat)
        self.assertValueAndType(nuclide, Nuclide, 'alpha_heat', float, comparenuclide.alpha_heat)
        self.assertValueAndType(nuclide, Nuclide, 'beta_heat', float, comparenuclide.beta_heat)
        self.assertValueAndType(nuclide, Nuclide, 'gamma_heat', float, comparenuclide.gamma_heat)
        self.assertValueAndType(nuclide, Nuclide, 'dose', float, comparenuclide.dose)
        self.assertValueAndType(nuclide, Nuclide, 'ingestion', float, comparenuclide.ingestion)
        self.assertValueAndType(nuclide, Nuclide, 'inhalation', float, comparenuclide.inhalation)

    def assert_timestep(self, nuclides, timestep):
        if timestep == 1:
            self.assert_nuclides(nuclides, timestep_1_nuclides())
        elif timestep == 2:
            self.assert_nuclides(nuclides, timestep_2_nuclides())
        elif 16 > timestep > 2:
            return
        else:
            self.assert_defaults(nuclides)


class NuclidesAssertor31(NuclidesAssertor):

    def assert_nuclides(self, nuclides, list):
        """
        Just assert certain nuclides in the list since there
        are too many to test

        :param nuclides:
        :param list:
        :return:
        """

        self.assert_nuclide(nuclides[2],  list[0])
        self.assert_nuclide(nuclides[32], list[1])
        self.assert_nuclide(nuclides[33], list[2])

    def assert_timestep(self, nuclides, timestep):
        if timestep == 1:
            self.assertEqual(len(nuclides), 5)
        elif timestep == 2:
            self.assert_nuclides(nuclides, timestep_2_nuclides31())
        elif 8 > timestep > 2:
            return
        else:
            self.assert_defaults(nuclides)


def timestep_1_nuclides():
    nuclides = []

    n = Nuclide()
    n.element = "U"
    n.isotope = 235
    n.state = ""
    n.half_life = 2.221E+16
    n.grams = 3.102E+01
    n.activity = 2.480E+06
    n.alpha_heat = 1.77E-09
    n.beta_heat = 2.014E-11
    n.gamma_heat = 6.502E-11
    n.heat = 1.855E-9
    n.dose = 2.818E-06
    n.ingestion = 1.166E-01
    n.inhalation = 2.108E+01
    nuclides.append(n)

    n = Nuclide()
    n.element = "U"
    n.isotope = 238
    n.state = ""
    n.half_life = 1.410E+17
    n.grams = 9.697E+02
    n.activity = 1.206E+07
    n.alpha_heat = 8.23E-09
    n.beta_heat = 1.972E-11
    n.gamma_heat = 2.126E-12
    n.heat = 8.252E-09
    n.dose = 1.599E-07
    n.ingestion = 5.427E-01
    n.inhalation = 9.647E+01
    nuclides.append(n)

    return nuclides


def timestep_2_nuclides():
    nuclides = []

    n = Nuclide()
    n.element = "He"
    n.isotope = 4
    n.state = ""
    n.half_life = 0.0
    n.grams = 2.541E-10
    n.activity = 0.0
    n.alpha_heat = 0.0
    n.beta_heat = 0.0
    n.gamma_heat = 0.0
    n.heat = 0.0
    n.dose = 0.0
    n.ingestion = 0.0
    n.inhalation = 0.0
    nuclides.append(n)

    n = Nuclide()
    n.element = "Ac"
    n.isotope = 227
    n.state = ""
    n.half_life = 6.871E+08
    n.grams = 1.959E-15
    n.activity = 5.241E-03
    n.alpha_heat = 5.82E-20
    n.beta_heat = 1.244E-20
    n.gamma_heat = 4.723E-22
    n.heat = 7.111E-20
    n.dose = 3.694E-17
    n.ingestion = 5.766E-09
    n.inhalation = 2.883E-06
    nuclides.append(n)

    n = Nuclide()
    n.element = "Th"
    n.isotope = 230
    n.state = ""
    n.half_life = 2.379E+12
    n.grams = 3.434E-16
    n.activity = 2.619E-07
    n.alpha_heat = 1.99E-22
    n.beta_heat = 5.203E-25
    n.gamma_heat = 5.357E-26
    n.heat = 1.996E-22
    n.dose = 3.489E-21
    n.ingestion = 5.500E-14
    n.inhalation = 2.619E-11
    nuclides.append(n)

    n = Nuclide()
    n.element = "Th"
    n.isotope = 231
    n.state = ""
    n.half_life = 9.187E+04
    n.grams = 1.261E-10
    n.activity = 2.480E+06
    n.alpha_heat = 0.00E+00
    n.beta_heat = 6.555E-11
    n.gamma_heat = 1.026E-11
    n.heat = 7.581E-11
    n.dose = 5.007E-07
    n.ingestion = 8.433E-04
    n.inhalation = 8.185E-04
    nuclides.append(n)

    n = Nuclide()
    n.element = "Th"
    n.isotope = 234
    n.state = ""
    n.half_life = 2.081E+06
    n.grams = 8.230E-09
    n.activity = 7.052E+06
    n.alpha_heat = 0.00E+00
    n.beta_heat = 6.842E-11
    n.gamma_heat = 9.944E-12
    n.heat = 7.836E-11
    n.dose = 3.399E-07
    n.ingestion = 2.398E-02
    n.inhalation = 5.430E-02
    nuclides.append(n)

    n = Nuclide()
    n.element = "Pa"
    n.isotope = 231
    n.state = ""
    n.half_life = 1.034E+12
    n.grams = 2.376E-09
    n.activity = 4.153E+00
    n.alpha_heat = 3.37E-15
    n.beta_heat = 3.480E-17
    n.gamma_heat = 2.577E-17
    n.heat = 3.431E-15
    n.dose = 4.920E-12
    n.ingestion = 2.949E-06
    n.inhalation = 5.814E-04
    nuclides.append(n)

    n = Nuclide()
    n.element = "Pa"
    n.isotope = 234
    n.state = ""
    n.half_life = 2.441E+04
    n.grams = 1.435E-13
    n.activity = 1.049E+04
    n.alpha_heat = 0.00E+00
    n.beta_heat = 6.485E-13
    n.gamma_heat = 2.411E-12
    n.heat = 3.06E-12
    n.dose = 2.431E-06
    n.ingestion = 5.349E-06
    n.inhalation = 4.196E-06
    nuclides.append(n)

    n = Nuclide()
    n.element = "Pa"
    n.isotope = 234
    n.state = "m"
    n.half_life = 7.020E+01
    n.grams = 2.776E-13
    n.activity = 7.052E+06
    n.alpha_heat = 0.00E+00
    n.beta_heat = 9.225E-10
    n.gamma_heat = 2.230E-11
    n.heat = 9.448E-10
    n.dose = 2.321E-05
    n.ingestion = 5.077E-06
    n.inhalation = 1.128E-03
    nuclides.append(n)

    n = Nuclide()
    n.element = "U"
    n.isotope = 234
    n.state = ""
    n.half_life = 7.754E+12
    n.grams = 4.095E-09
    n.activity = 9.419E-01
    n.alpha_heat = 7.31E-16
    n.beta_heat = 2.134E-18
    n.gamma_heat = 2.188E-19
    n.heat = 7.334E-16
    n.dose = 1.632E-14
    n.ingestion = 4.615E-08
    n.inhalation = 8.854E-06
    nuclides.append(n)

    n = Nuclide()
    n.element = "U"
    n.isotope = 235
    n.state = ""
    n.half_life = 2.221E+16
    n.grams = 3.102E+01
    n.activity = 2.480E+06
    n.alpha_heat = 1.77E-09
    n.beta_heat = 2.014E-11
    n.gamma_heat = 6.502E-11
    n.heat = 1.855E-09
    n.dose = 2.818E-06
    n.ingestion = 1.166E-01
    n.inhalation = 2.108E+01
    nuclides.append(n)

    n = Nuclide()
    n.element = "U"
    n.isotope = 238
    n.state = ""
    n.half_life = 1.410E+17
    n.grams = 9.697E+02
    n.activity = 1.206E+07
    n.alpha_heat = 8.23E-09
    n.beta_heat = 1.972E-11
    n.gamma_heat = 2.126E-12
    n.heat = 8.252E-09
    n.dose = 1.599E-07
    n.ingestion = 5.427E-01
    n.inhalation = 9.647E+01
    nuclides.append(n)

    return nuclides


def timestep_2_nuclides31():
    nuclides = []

    n = Nuclide()
    n.element = "H"
    n.isotope = 3
    n.state = ""
    n.half_life = 3.891E+08
    n.grams = 1.943E-04
    n.activity = 6.911E+10
    n.alpha_heat = 0.0
    n.beta_heat = 6.320E-08
    n.gamma_heat = 0.0
    n.heat = 6.320E-08
    n.dose = 0.0
    n.ingestion = 2.903E+00
    n.inhalation = 1.797E+01
    nuclides.append(n)

    n = Nuclide()
    n.element = "Cl"
    n.isotope = 38
    n.state = "m"
    n.half_life = 7.150E-01
    n.grams = 9.053E-17
    n.activity = 1.392E+06
    n.alpha_heat = 0.0
    n.beta_heat = 9.579E-14
    n.gamma_heat = 1.497E-10
    n.heat = 1.498E-10
    n.dose = 2.241E-04
    n.ingestion = 8.074E-08
    n.inhalation = 4.037E-08
    nuclides.append(n)

    n = Nuclide()
    n.element = "Cl"
    n.isotope = 39
    n.state = ""
    n.half_life = 3.336E+03
    n.grams = 3.899E-13
    n.activity = 1.252E+06
    n.alpha_heat = 0.0
    n.beta_heat = 1.650E-10
    n.gamma_heat = 2.918E-10
    n.heat = 4.568E-10
    n.dose = 5.269E-04
    n.ingestion = 1.064E-04
    n.inhalation = 5.760E-05
    nuclides.append(n)

    return nuclides


class NuclidesUnitTest(BaseOutputUnitTest):

    assertor = NuclidesAssertor()
    assertor31 = NuclidesAssertor31()

    def test_fispact_deserialize(self):

        def func(nucs, i):
            nucs.fispact_deserialize(self.filerecord91, i)
            self.assertor.assert_timestep(nucs, i)

        self._wrapper(func)

    def test_fispact_deserialize31(self):

        def func(nucs, i):
            nucs.fispact_deserialize(self.filerecord31, i)
            self.assertor31.assert_timestep(nucs, i)

        self._wrapper(func)

    def test_fispact_readwriteread(self):

        def func(nucs, i):
            # deserialize from standard output
            nucs.fispact_deserialize(self.filerecord91, i)
            self.assertor.assert_timestep(nucs, i)

            # serialize to JSON
            j = nucs.json_serialize()

            # reset object
            newnucs = Nuclides()
            self.assertor.assert_defaults(newnucs)

            # deserialize JSON and compare to original
            newnucs.json_deserialize(j)
            self.assertor.assert_timestep(newnucs, i)

        self._wrapper(func)

    def test_fispact_readwriteread31(self):

        def func(nucs, i):
            # deserialize from standard output
            nucs.fispact_deserialize(self.filerecord31, i)
            self.assertor31.assert_timestep(nucs, i)

            # serialize to JSON
            j = nucs.json_serialize()

            # reset object
            newnucs = Nuclides()
            self.assertor31.assert_defaults(newnucs)

            # deserialize JSON and compare to original
            newnucs.json_deserialize(j)
            self.assertor31.assert_timestep(newnucs, i)

        self._wrapper(func)

    def _wrapper(self, func):
        nucs = Nuclides()
        self.assertor.assert_defaults(nucs)

        for i in range(-100, 100):
            func(nucs, i)

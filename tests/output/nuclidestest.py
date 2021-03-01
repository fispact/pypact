from tests.output.baseoutputtest import BaseOutputUnitTest

import pypact as pp


class NuclidesAssertor(BaseOutputUnitTest):
    def assert_defaults(self, nuclides):
        self.assertEqual(len(nuclides), 0)

    def assert_nuclides(self, nuclides, nlist):
        self.assertEqual(len(nuclides), len(nlist))

        for i, nuc in enumerate(nlist):
            self.assert_nuclide(nuclides[i], nuc)

    def assert_nuclide(self, nuclide, comparenuclide):
        self.assertValueAndType(
            nuclide, pp.Nuclide, "element", str, comparenuclide.element
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "isotope", int, comparenuclide.isotope
        )
        self.assertValueAndType(nuclide, pp.Nuclide, "state", str, comparenuclide.state)
        self.assertValueAndType(
            nuclide, pp.Nuclide, "half_life", float, comparenuclide.half_life
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "atoms", float, comparenuclide.atoms
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "grams", float, comparenuclide.grams
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "activity", float, comparenuclide.activity
        )
        self.assertValueAndType(nuclide, pp.Nuclide, "heat", float, comparenuclide.heat)
        self.assertValueAndType(
            nuclide, pp.Nuclide, "alpha_heat", float, comparenuclide.alpha_heat
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "beta_heat", float, comparenuclide.beta_heat
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "gamma_heat", float, comparenuclide.gamma_heat
        )
        self.assertValueAndType(nuclide, pp.Nuclide, "dose", float, comparenuclide.dose)
        self.assertValueAndType(
            nuclide, pp.Nuclide, "ingestion", float, comparenuclide.ingestion
        )
        self.assertValueAndType(
            nuclide, pp.Nuclide, "inhalation", float, comparenuclide.inhalation
        )
        self.assertValueAndType(nuclide, pp.Nuclide, "zai", int, comparenuclide.zai)
        self.assertValueAndType(nuclide, pp.Nuclide, "name", str, comparenuclide.name)

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

        self.assert_nuclide(nuclides[2], list[0])
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

    n = pp.Nuclide()
    n.element = "U"
    n.isotope = 235
    n.state = ""
    n.half_life = 2.221e16
    n.atoms = 7.94800e22
    n.grams = 3.102e01
    n.activity = 2.480e06
    n.alpha_heat = 1.77e-09
    n.beta_heat = 2.014e-11
    n.gamma_heat = 6.502e-11
    n.heat = 1.855e-9
    n.dose = 2.818e-06
    n.ingestion = 1.166e-01
    n.inhalation = 2.108e01
    assert n.name == "U235"
    assert n.zai == 922350
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "U"
    n.isotope = 238
    n.state = ""
    n.half_life = 1.410e17
    n.atoms = 2.45300e24
    n.grams = 9.697e02
    n.activity = 1.206e07
    n.alpha_heat = 8.23e-09
    n.beta_heat = 1.972e-11
    n.gamma_heat = 2.126e-12
    n.heat = 8.252e-09
    n.dose = 1.599e-07
    n.ingestion = 5.427e-01
    n.inhalation = 9.647e01
    assert n.name == "U238"
    assert n.zai == 922380
    nuclides.append(n)

    return nuclides


def timestep_2_nuclides():
    nuclides = []

    n = pp.Nuclide()
    n.element = "He"
    n.isotope = 4
    n.state = ""
    n.half_life = 0.0
    n.atoms = 3.82362e13
    n.grams = 2.541e-10
    n.activity = 0.0
    n.alpha_heat = 0.0
    n.beta_heat = 0.0
    n.gamma_heat = 0.0
    n.heat = 0.0
    n.dose = 0.0
    n.ingestion = 0.0
    n.inhalation = 0.0
    assert n.name == "He4"
    assert n.zai == 20040
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Ac"
    n.isotope = 227
    n.state = ""
    n.half_life = 6.871e08
    n.atoms = 5.19573e06
    n.grams = 1.959e-15
    n.activity = 5.241e-03
    n.alpha_heat = 5.82e-20
    n.beta_heat = 1.244e-20
    n.gamma_heat = 4.723e-22
    n.heat = 7.111e-20
    n.dose = 3.694e-17
    n.ingestion = 5.766e-09
    n.inhalation = 2.883e-06
    assert n.name == "Ac227"
    assert n.zai == 892270
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Th"
    n.isotope = 230
    n.state = ""
    n.half_life = 2.379e12
    n.atoms = 8.99093e05
    n.grams = 3.434e-16
    n.activity = 2.619e-07
    n.alpha_heat = 1.99e-22
    n.beta_heat = 5.203e-25
    n.gamma_heat = 5.357e-26
    n.heat = 1.996e-22
    n.dose = 3.489e-21
    n.ingestion = 5.500e-14
    n.inhalation = 2.619e-11
    assert n.name == "Th230"
    assert n.zai == 902300
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Th"
    n.isotope = 231
    n.state = ""
    n.half_life = 9.187e04
    n.atoms = 3.28759e11
    n.grams = 1.261e-10
    n.activity = 2.480e06
    n.alpha_heat = 0.00e00
    n.beta_heat = 6.555e-11
    n.gamma_heat = 1.026e-11
    n.heat = 7.581e-11
    n.dose = 5.007e-07
    n.ingestion = 8.433e-04
    n.inhalation = 8.185e-04
    assert n.name == "Th231"
    assert n.zai == 902310
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Th"
    n.isotope = 234
    n.state = ""
    n.half_life = 2.081e06
    n.atoms = 2.11761e13
    n.grams = 8.230e-09
    n.activity = 7.052e06
    n.alpha_heat = 0.00e00
    n.beta_heat = 6.842e-11
    n.gamma_heat = 9.944e-12
    n.heat = 7.836e-11
    n.dose = 3.399e-07
    n.ingestion = 2.398e-02
    n.inhalation = 5.430e-02
    assert n.name == "Th234"
    assert n.zai == 902340
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Pa"
    n.isotope = 231
    n.state = ""
    n.half_life = 1.034e12
    n.atoms = 6.19433e12
    n.grams = 2.376e-09
    n.activity = 4.153e00
    n.alpha_heat = 3.37e-15
    n.beta_heat = 3.480e-17
    n.gamma_heat = 2.577e-17
    n.heat = 3.431e-15
    n.dose = 4.920e-12
    n.ingestion = 2.949e-06
    n.inhalation = 5.814e-04
    assert n.name == "Pa231"
    assert n.zai == 912310
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Pa"
    n.isotope = 234
    n.state = ""
    n.half_life = 2.441e04
    n.atoms = 3.69346e08
    n.grams = 1.435e-13
    n.activity = 1.049e04
    n.alpha_heat = 0.00e00
    n.beta_heat = 6.485e-13
    n.gamma_heat = 2.411e-12
    n.heat = 3.06e-12
    n.dose = 2.431e-06
    n.ingestion = 5.349e-06
    n.inhalation = 4.196e-06
    assert n.name == "Pa234"
    assert n.zai == 912340
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Pa"
    n.isotope = 234
    n.state = "m"
    n.half_life = 7.020e01
    n.atoms = 7.14202e08
    n.grams = 2.776e-13
    n.activity = 7.052e06
    n.alpha_heat = 0.00e00
    n.beta_heat = 9.225e-10
    n.gamma_heat = 2.230e-11
    n.heat = 9.448e-10
    n.dose = 2.321e-05
    n.ingestion = 5.077e-06
    n.inhalation = 1.128e-03
    assert n.name == "Pa234m"
    assert n.zai == 912341
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "U"
    n.isotope = 234
    n.state = ""
    n.half_life = 7.754e12
    n.atoms = 1.05359e13
    n.grams = 4.095e-09
    n.activity = 9.419e-01
    n.alpha_heat = 7.31e-16
    n.beta_heat = 2.134e-18
    n.gamma_heat = 2.188e-19
    n.heat = 7.334e-16
    n.dose = 1.632e-14
    n.ingestion = 4.615e-08
    n.inhalation = 8.854e-06
    assert n.name == "U234"
    assert n.zai == 922340
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "U"
    n.isotope = 235
    n.state = ""
    n.half_life = 2.221e16
    n.atoms = 7.94800e22
    n.grams = 3.102e01
    n.activity = 2.480e06
    n.alpha_heat = 1.77e-09
    n.beta_heat = 2.014e-11
    n.gamma_heat = 6.502e-11
    n.heat = 1.855e-09
    n.dose = 2.818e-06
    n.ingestion = 1.166e-01
    n.inhalation = 2.108e01
    assert n.name == "U235"
    assert n.zai == 922350
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "U"
    n.isotope = 238
    n.state = ""
    n.half_life = 1.410e17
    n.atoms = 2.45300e24
    n.grams = 9.697e02
    n.activity = 1.206e07
    n.alpha_heat = 8.23e-09
    n.beta_heat = 1.972e-11
    n.gamma_heat = 2.126e-12
    n.heat = 8.252e-09
    n.dose = 1.599e-07
    n.ingestion = 5.427e-01
    n.inhalation = 9.647e01
    assert n.name == "U238"
    assert n.zai == 922380
    nuclides.append(n)

    return nuclides


def timestep_2_nuclides31():
    nuclides = []

    n = pp.Nuclide()
    n.element = "H"
    n.isotope = 3
    n.state = ""
    n.half_life = 3.891e08
    n.atoms = 3.87956e19
    n.grams = 1.943e-04
    n.activity = 6.911e10
    n.alpha_heat = 0.0
    n.beta_heat = 6.320e-08
    n.gamma_heat = 0.0
    n.heat = 6.320e-08
    n.dose = 0.0
    n.ingestion = 2.903e00
    n.inhalation = 1.797e01
    assert n.name == "H3"
    assert n.zai == 10030
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Cl"
    n.isotope = 38
    n.state = "m"
    n.half_life = 7.150e-01
    n.atoms = 1.43597e06
    n.grams = 9.053e-17
    n.activity = 1.392e06
    n.alpha_heat = 0.0
    n.beta_heat = 9.579e-14
    n.gamma_heat = 1.497e-10
    n.heat = 1.498e-10
    n.dose = 2.241e-04
    n.ingestion = 8.074e-08
    n.inhalation = 4.037e-08
    assert n.name == "Cl38m"
    assert n.zai == 170381
    nuclides.append(n)

    n = pp.Nuclide()
    n.element = "Cl"
    n.isotope = 39
    n.state = ""
    n.half_life = 3.336e03
    n.atoms = 6.02606e09
    n.grams = 3.899e-13
    n.activity = 1.252e06
    n.alpha_heat = 0.0
    n.beta_heat = 1.650e-10
    n.gamma_heat = 2.918e-10
    n.heat = 4.568e-10
    n.dose = 5.269e-04
    n.ingestion = 1.064e-04
    n.inhalation = 5.760e-05
    assert n.name == "Cl39"
    assert n.zai == 170390
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
            newnucs = pp.Nuclides()
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
            newnucs = pp.Nuclides()
            self.assertor31.assert_defaults(newnucs)

            # deserialize JSON and compare to original
            newnucs.json_deserialize(j)
            self.assertor31.assert_timestep(newnucs, i)

        self._wrapper(func)

    def _wrapper(self, func):
        nucs = pp.Nuclides()
        self.assertor.assert_defaults(nucs)

        for i in range(-100, 100):
            func(nucs, i)

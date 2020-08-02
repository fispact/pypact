import pypact as pp

from tests.output.baseoutputtest import BaseOutputUnitTest


class GammaSpectrumUnitTest(BaseOutputUnitTest):

    def test_file91_first_timestep(self):
        self._assertGS(1, self.filerecord91, [], [], [])

    def test_file91_second_timestep(self):
        expectedBoundaries = [
                                0.000,
                                0.010,
                                0.020,
                                0.050,
                                0.100,
                                0.200,
                                0.300,
                                0.400,
                                0.600,
                                0.800,
                                1.000,
                                1.220,
                                1.440,
                                1.660,
                                2.000,
                                2.500,
                                3.000,
                                4.000,
                                5.000,
                                6.500,
                                8.000,
                                10.000,
                                12.000,
                                14.000,
                                20.000
                            ]
        expectedValues = [
                            3.76965E+03,
                            5.50637E+04,
                            9.87715E+03,
                            1.00700E+05,
                            3.48210E+05,
                            3.57227E+04,
                            1.20760E+03,
                            1.84718E+03,
                            3.01858E+04,
                            1.24627E+04,
                            6.17275E+04,
                            2.82575E+03,
                            3.98541E+03,
                            1.19461E+04,
                            7.08490E-01,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00
        ]
        expectedRates = [
                            7.60957E+03,
                            3.70512E+04,
                            2.84834E+03,
                            1.35519E+04,
                            2.34304E+04,
                            1.44222E+03,
                            3.48245E+01,
                            3.72878E+01,
                            4.35245E+02,
                            1.39765E+02,
                            5.61286E+02,
                            2.14442E+01,
                            2.59519E+01,
                            6.58877E+01,
                            3.17819E-03,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00
        ]
        self._assertGS(2, self.filerecord91, expectedBoundaries, expectedValues, expectedRates)
    
    def test_file91_last_timestep(self):
        expectedBoundaries = [
                                0.000,
                                0.010,
                                0.020,
                                0.050,
                                0.100,
                                0.200,
                                0.300,
                                0.400,
                                0.600,
                                0.800,
                                1.000,
                                1.220,
                                1.440,
                                1.660,
                                2.000,
                                2.500,
                                3.000,
                                4.000,
                                5.000,
                                6.500,
                                8.000,
                                10.000,
                                12.000,
                                14.000,
                                20.000
                            ]
        expectedValues = [
                            4.16972E+03,
                            6.14701E+04,
                            9.89745E+03,
                            1.40219E+05,
                            3.51060E+05,
                            3.71176E+04,
                            1.46416E+03,
                            3.14453E+03,
                            5.16571E+04,
                            2.14196E+04,
                            1.05565E+05,
                            4.84248E+03,
                            6.82105E+03,
                            2.04390E+04,
                            1.22184E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00
        ]
        expectedRates = [
                            8.41715E+03,
                            4.13620E+04,
                            2.85420E+03,
                            1.88702E+04,
                            2.36221E+04,
                            1.49854E+03,
                            4.22229E+01,
                            6.34767E+01,
                            7.44836E+02,
                            2.40214E+02,
                            9.59896E+02,
                            3.67490E+01,
                            4.44169E+01,
                            1.12729E+02,
                            5.48101E-03,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00,
                            0.00000E+00
        ]
        self._assertGS(15, self.filerecord91, expectedBoundaries, expectedValues, expectedRates)

    def _assertGS(self, timestep, filerecord, boundaries, values, rates):
        gs = pp.GammaSpectrum()
        
        self.assertEqual([], gs.boundaries, "Assert gamma spectrum boundary defaults")
        self.assertEqual([], gs.values, "Assert gamma spectrum value defaults")
        self.assertEqual([], gs.volumetric_rates, "Assert gamma spectrum rate defaults")
        
        gs.fispact_deserialize(filerecord, timestep)
        self.assertEqual(boundaries, gs.boundaries, "Assert gamma spectrum boundary")
        self.assertEqual(values, gs.values, "Assert gamma spectrum value")
        self.assertEqual(rates, gs.volumetric_rates, "Assert gamma spectrum rate")


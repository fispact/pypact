import os
import pypact as pp
from pypact.printlib.printlib5 import SpectralData

from tests.testerbase import Tester, REFERENCE_DIR


class PrintLib5UnitTest(Tester):
    def setUp(self):
        self.filename = os.path.join(os.path.join(REFERENCE_DIR), "printlib5.out")        

    def tearDown(self):
        pass

    def test_default(self):
        pl = pp.PrintLib5()
        self.assertEqual(0, len(pl), "Assert no data")
        self.assertEqual(0, len(pl.spectral_data), "Assert no mean data")

    def test_fispact_deserialize(self):
        pl = pp.PrintLib5()
        self.assertEqual(0, len(pl), "Assert no data")
        self.assertEqual(0, len(pl.spectral_data), "Assert no mean data")

        # due to a bug in FISPACT-II and/or nuclear data
        # it sometimes prints out 0 for number of spectra
        # in mean section but then has no line entry - hence the mismatch
        # between filerecord nr_of_entries and len(pl.spectral_data)
        fr = pp.PrintLib5FileRecord(self.filename)
        self.assertEqual(8422, fr.nr_of_entries, "Assert number of mean entries")

        pl = pp.PrintLib5()
        pl.fispact_deserialize(fr)
        self.assertEqual(8257, len(pl), "Assert data")
        self.assertEqual(8257, len(pl.spectral_data), "Assert mean data")
        self.assertEqual(3875, pl.nr_of_zais, "Assert number of ZAIs")

    def test_reader(self):
        with pp.PrintLib5Reader(self.filename) as pl:
            self.assertEqual(8257, len(pl), "Assert data")
            self.assertEqual(8257, len(pl.spectral_data), "Assert mean data")
            self.assertEqual(3875, pl.nr_of_zais, "Assert number of ZAIs")

            s = pl.spectral_data[0]
            self.assertEqual("H   3", s.name, "Assert name")
            self.assertEqual(10030, s.zai, "Assert zai")
            self.assertEqual(3, s.number, "Assert number")
            self.assertEqual("beta", s.type, "Assert type")
            self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(5.70740E+03, s.mean_energy, "Assert mean_energy")
            self.assertEqual(1.84397E+00, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.0, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_data[130]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("gamma", s.type, "Assert type")
            self.assertEqual(15, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(5.47120E+05, s.mean_energy, "Assert mean_energy")
            self.assertEqual(3.77412E+03, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(8.95500E-01, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(6.00000E-04, s.mean_normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_data[131]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("beta", s.type, "Assert type")
            self.assertEqual(7, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(2.34181E+06, s.mean_energy, "Assert mean_energy")
            self.assertEqual(1.08633E+05, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_data[132]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("e-", s.type, "Assert type")
            self.assertEqual(4, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(2.07265E+01, s.mean_energy, "Assert mean_energy")
            self.assertEqual(2.07265E+00, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_data[133]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("x", s.type, "Assert type")
            self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(6.31343E-04, s.mean_energy, "Assert mean_energy")
            self.assertEqual(6.31343E-05, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")

            # last entry
            s = pl.spectral_data[-1]
            self.assertEqual("Rg272", s.name, "Assert name")
            self.assertEqual(1112720, s.zai, "Assert zai")
            self.assertEqual(3875, s.number, "Assert number")
            self.assertEqual("no spectral data", s.type, "Assert type")
            self.assertEqual(0, s.nr_of_lines, "Assert default")
            self.assertEqual(0.0, s.mean_energy, "Assert default")
            self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
            self.assertEqual(0.0, s.mean_normalisation, "Assert default")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert default")

    def test_reader_spectral_lines(self):
        with pp.PrintLib5Reader(self.filename) as pl:
            self.assertEqual(8257, len(pl), "Assert data")
            self.assertEqual(8257, len(pl.spectral_data), "Assert mean data")
            self.assertEqual(3875, pl.nr_of_zais, "Assert number of ZAIs")

            s = pl.spectral_data[0]
            self.assertEqual("H   3", s.name, "Assert name")
            self.assertEqual(10030, s.zai, "Assert zai")
            self.assertEqual(3, s.number, "Assert number")
            self.assertEqual("beta", s.type, "Assert type")
            self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(5.70740E+03, s.mean_energy, "Assert mean_energy")
            self.assertEqual(1.84397E+00, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.0, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")
            self.assertEqual([1.85710E+04], s.lines.energies, "Assert line energies")
            self.assertEqual([6.00000E+00], s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual([1.00000E+00], s.lines.intensities, "Assert line intensities")
            self.assertEqual([0.0], s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual([1.00000E+00], s.lines.norms, "Assert line norms")
            self.assertEqual([0.0], s.lines.norms_unc, "Assert line norms uncert")

            s = pl.spectral_data[130]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("gamma", s.type, "Assert type")
            self.assertEqual(15, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(5.47120E+05, s.mean_energy, "Assert mean_energy")
            self.assertEqual(3.77412E+03, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(8.95500E-01, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(6.00000E-04, s.mean_normalisation_unc, "Assert normalisation_unc")

            line_energies = [
                3.50730E+05,
                1.39518E+06,
                1.74591E+06,
                1.89040E+06,
                1.98970E+06,
                2.78000E+06,
                2.79416E+06,
                3.38490E+06,
                3.53330E+06,
                3.73560E+06,
                3.88400E+06,
                4.17510E+06,
                4.33390E+06,
                4.52590E+06,
                4.68460E+06
            ]
            line_energies_unc = [
                1.00000E+01,
                3.00000E+01,
                2.00000E+01,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02,
                4.00000E+01,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02,
                2.00000E+02
            ]
            line_intensities = [
                1.00000E+00,
                1.71300E-01,
                8.64000E-03,
                2.03000E-05,
                2.50000E-06,
                1.77000E-05,
                2.03000E-05,
                4.20000E-06,
                3.26000E-05,
                2.78000E-05,
                1.07000E-05,
                3.56500E-04,
                5.30600E-04,
                1.06000E-04,
                3.12700E-04
            ]
            line_intensities_unc = [
                0.00000E+00,
                3.00000E-03,
                1.50000E-04,
                3.00000E-06,
                3.00000E-07,
                1.70000E-06,
                3.00000E-06,
                4.00000E-07,
                1.70000E-06,
                2.60000E-06,
                1.40000E-06,
                6.50000E-06,
                1.35000E-05,
                3.30000E-06,
                1.09000E-05
            ]
            line_norms = [
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01,
                8.95500E-01
            ]
            line_norms_unc = [
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04,
                6.00000E-04
            ]
            self.assertEqual(line_energies, s.lines.energies, "Assert line energies")
            self.assertEqual(line_energies_unc, s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual(line_intensities, s.lines.intensities, "Assert line intensities")
            self.assertEqual(line_intensities_unc, s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual(line_norms, s.lines.norms, "Assert line norms")
            self.assertEqual(line_norms_unc, s.lines.norms_unc, "Assert line norms uncert")

            s = pl.spectral_data[131]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("beta", s.type, "Assert type")
            self.assertEqual(7, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(2.34181E+06, s.mean_energy, "Assert mean_energy")
            self.assertEqual(1.08633E+05, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")

            line_energies = [
                9.99600E+05,
                1.15830E+06,
                1.80020E+06,
                1.94860E+06,
                3.93830E+06,
                5.33350E+06,
                5.68420E+06
            ]
            line_energies_unc = [
                2.00000E+03,
                2.00000E+03,
                2.00000E+03,
                2.00000E+03,
                1.80000E+03,
                1.80000E+03,
                1.80000E+03
            ]
            line_intensities = [
                7.70000E-04,
                4.30000E-04,
                3.90000E-05,
                3.10000E-05,
                1.61000E-01,
                7.41000E-01,
                9.60000E-02
            ]
            line_intensities_unc = [
                2.00000E-05,
                1.00000E-05,
                3.00000E-06,
                3.00000E-06,
                1.00000E-02,
                3.00000E-02,
                3.00000E-02
            ]
            line_norms = [
                1.00000E+00,
                1.00000E+00,
                1.00000E+00,
                1.00000E+00,
                1.00000E+00,
                1.00000E+00,
                1.00000E+00
            ]
            line_norms_unc = [
                0.00000E+00,
                0.00000E+00,
                0.00000E+00,
                0.00000E+00,
                0.00000E+00,
                0.00000E+00,
                0.00000E+00
            ]
            self.assertEqual(line_energies, s.lines.energies, "Assert line energies")
            self.assertEqual(line_energies_unc, s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual(line_intensities, s.lines.intensities, "Assert line intensities")
            self.assertEqual(line_intensities_unc, s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual(line_norms, s.lines.norms, "Assert line norms")
            self.assertEqual(line_norms_unc, s.lines.norms_unc, "Assert line norms uncert")

            s = pl.spectral_data[132]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("e-", s.type, "Assert type")
            self.assertEqual(4, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(2.07265E+01, s.mean_energy, "Assert mean_energy")
            self.assertEqual(2.07265E+00, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")
            line_energies = [
                8.30000E+02,
                3.49863E+05,
                3.50712E+05,
                3.50730E+05
            ]
            line_energies_unc = [
                4.15000E+01,
                1.74932E+04,
                1.75356E+04,
                1.75365E+04
            ]
            line_intensities = [
                5.47770E-05,
                5.55210E-05,
                3.13425E-06,
                4.47750E-07
            ]
            line_intensities_unc = [
                5.47770E-06,
                5.55210E-06,
                3.13425E-07,
                4.47750E-08
            ]
            line_norms = [
                1.00000E+00,
                1.00000E+00,
                1.00000E+00,
                1.00000E+00
            ]
            line_norms_unc = [
                0.00000E+00,
                0.00000E+00,
                0.00000E+00,
                0.00000E+00
            ]
            self.assertEqual(line_energies, s.lines.energies, "Assert line energies")
            self.assertEqual(line_energies_unc, s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual(line_intensities, s.lines.intensities, "Assert line intensities")
            self.assertEqual(line_intensities_unc, s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual(line_norms, s.lines.norms, "Assert line norms")
            self.assertEqual(line_norms_unc, s.lines.norms_unc, "Assert line norms uncert")

            s = pl.spectral_data[133]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("x", s.type, "Assert type")
            self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(6.31343E-04, s.mean_energy, "Assert mean_energy")
            self.assertEqual(6.31343E-05, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.mean_normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")
            self.assertEqual([8.48600E+02], s.lines.energies, "Assert line energies")
            self.assertEqual([1.69720E+01], s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual([7.43981E-07], s.lines.intensities, "Assert line intensities")
            self.assertEqual([7.43981E-08], s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual([1.0], s.lines.norms, "Assert line norms")
            self.assertEqual([0.0], s.lines.norms_unc, "Assert line norms uncert")

            # last non zero entry
            s = pl.spectral_data[8168]
            self.assertEqual("Lr257", s.name, "Assert name")
            self.assertEqual(1032570, s.zai, "Assert zai")
            self.assertEqual(3787, s.number, "Assert number")
            self.assertEqual("alpha", s.type, "Assert type")
            self.assertEqual(2, s.nr_of_lines, "Assert default")
            self.assertEqual(8.84930E+06, s.mean_energy, "Assert default")
            self.assertEqual(1.01144E+04, s.mean_energy_unc, "Assert default")
            self.assertEqual(1.00000E-02, s.mean_normalisation, "Assert default")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert default")
            self.assertEqual([8.79600E+06, 8.86100E+06], s.lines.energies, "Assert line energies")
            self.assertEqual([1.30000E+04, 1.20000E+04], s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual([1.80000E+01, 8.20000E+01], s.lines.intensities, "Assert line intensities")
            self.assertEqual([2.00000E+00, 2.00000E+00], s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual([1.00000E-02, 1.00000E-02], s.lines.norms, "Assert line norms")
            self.assertEqual([0.0, 0.0], s.lines.norms_unc, "Assert line norms uncert")

            # last entry
            s = pl.spectral_data[-1]
            self.assertEqual("Rg272", s.name, "Assert name")
            self.assertEqual(1112720, s.zai, "Assert zai")
            self.assertEqual(3875, s.number, "Assert number")
            self.assertEqual("no spectral data", s.type, "Assert type")
            self.assertEqual(0, s.nr_of_lines, "Assert default")
            self.assertEqual(0.0, s.mean_energy, "Assert default")
            self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
            self.assertEqual(0.0, s.mean_normalisation, "Assert default")
            self.assertEqual(0.0, s.mean_normalisation_unc, "Assert default")
            self.assertEqual([], s.lines.energies, "Assert line energies")
            self.assertEqual([], s.lines.energies_unc, "Assert line energies uncert")
            self.assertEqual([], s.lines.intensities, "Assert line intensities")
            self.assertEqual([], s.lines.intensities_unc, "Assert line intensities uncert")
            self.assertEqual([], s.lines.norms, "Assert line norms")
            self.assertEqual([], s.lines.norms_unc, "Assert line norms uncert")

    def test_default_spectra_data(self):
        s = SpectralData()
        self.assertEqual("", s.name, "Assert default")
        self.assertEqual(0, s.zai, "Assert default")
        self.assertEqual(0, s.number, "Assert default")
        self.assertEqual("", s.type, "Assert default")
        self.assertEqual(0, s.nr_of_lines, "Assert default")
        self.assertEqual(0.0, s.mean_energy, "Assert default")
        self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
        self.assertEqual(0.0, s.mean_normalisation, "Assert default")
        self.assertEqual(0.0, s.mean_normalisation_unc, "Assert default")
        self.assertEqual(0, len(s.lines), "Assert no line data")

    def test_default_spectra_data_deserialize(self):
        s = SpectralData()
        linedump = ['  He  8    20080    13   gamma                 1    8.63104E+05 +- 9.80839E+03  8.80000E-01 +- 0.00000E+00\n']
        s.fispact_deserialize(linedump)
        self.assertEqual("He  8", s.name, "Assert name")
        self.assertEqual(20080, s.zai, "Assert zai")
        self.assertEqual(13, s.number, "Assert number")
        self.assertEqual("gamma", s.type, "Assert type")
        self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
        self.assertEqual(8.63104E+05, s.mean_energy, "Assert mean_energy")
        self.assertEqual(9.80839E+03, s.mean_energy_unc, "Assert mean_energy_unc")
        self.assertEqual(8.80000E-01, s.mean_normalisation, "Assert normalisation")
        self.assertEqual(0.0, s.mean_normalisation_unc, "Assert normalisation_unc")
        self.assertEqual(0, len(s.lines), "Assert no line data")

        linedump = ['  Be  5    40050    25   no spectral data\n']
        s.fispact_deserialize(linedump)
        self.assertEqual("Be  5", s.name, "Assert name")
        self.assertEqual(40050, s.zai, "Assert zai")
        self.assertEqual(25, s.number, "Assert number")
        self.assertEqual("no spectral data", s.type, "Assert type")
        self.assertEqual(0, s.nr_of_lines, "Assert default")
        self.assertEqual(0.0, s.mean_energy, "Assert default")
        self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
        self.assertEqual(0.0, s.mean_normalisation, "Assert default")
        self.assertEqual(0.0, s.mean_normalisation_unc, "Assert default")
        self.assertEqual(0, len(s.lines), "Assert no line data")
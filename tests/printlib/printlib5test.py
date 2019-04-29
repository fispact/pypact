import os
import pypact as pp
from pypact.printlib.printlib5 import SpectralMeanData

from tests.testerbase import Tester, REFERENCE_DIR


class PrintLib5UnitTest(Tester):
    def setUp(self):
        self.filename = os.path.join(os.path.join(REFERENCE_DIR), "printlib5.out")        

    def tearDown(self):
        pass

    def test_default(self):
        pl = pp.PrintLib5()
        self.assertEqual(0, len(pl), "Assert no data")
        self.assertEqual(0, len(pl.spectral_mean_data), "Assert no mean data")
        self.assertEqual(0, len(pl.spectral_line_data), "Assert no line data")

    def test_fispact_deserialize(self):
        pl = pp.PrintLib5()
        self.assertEqual(0, len(pl), "Assert no data")
        self.assertEqual(0, len(pl.spectral_mean_data), "Assert no mean data")
        self.assertEqual(0, len(pl.spectral_line_data), "Assert no line data")

        fr = pp.PrintLib5FileRecord(self.filename)
        self.assertEqual(8422, fr.nr_of_mean_entries, "Assert number of mean entries")

        pl = pp.PrintLib5()
        pl.fispact_deserialize(fr)
        self.assertEqual(8422, len(pl), "Assert data")
        self.assertEqual(8422, len(pl.spectral_mean_data), "Assert mean data")
        self.assertEqual(0, len(pl.spectral_line_data), "Assert no line data")
        self.assertEqual(3875, pl.nr_of_zais, "Assert number of ZAIs")

    def test_reader(self):
        with pp.PrintLib5Reader(self.filename) as pl:
            self.assertEqual(8422, len(pl), "Assert data")
            self.assertEqual(8422, len(pl.spectral_mean_data), "Assert mean data")
            self.assertEqual(0, len(pl.spectral_line_data), "Assert no line data")
            self.assertEqual(3875, pl.nr_of_zais, "Assert number of ZAIs")

            s = pl.spectral_mean_data[0]
            self.assertEqual("H   3", s.name, "Assert name")
            self.assertEqual(10030, s.zai, "Assert zai")
            self.assertEqual(3, s.number, "Assert number")
            self.assertEqual("beta", s.type, "Assert type")
            self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(5.70740E+03, s.mean_energy, "Assert mean_energy")
            self.assertEqual(1.84397E+00, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.0, s.normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_mean_data[130]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("gamma", s.type, "Assert type")
            self.assertEqual(15, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(5.47120E+05, s.mean_energy, "Assert mean_energy")
            self.assertEqual(3.77412E+03, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(8.95500E-01, s.normalisation, "Assert normalisation")
            self.assertEqual(6.00000E-04, s.normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_mean_data[131]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("beta", s.type, "Assert type")
            self.assertEqual(7, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(2.34181E+06, s.mean_energy, "Assert mean_energy")
            self.assertEqual(1.08633E+05, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_mean_data[132]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("e-", s.type, "Assert type")
            self.assertEqual(4, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(2.07265E+01, s.mean_energy, "Assert mean_energy")
            self.assertEqual(2.07265E+00, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.normalisation_unc, "Assert normalisation_unc")

            s = pl.spectral_mean_data[133]
            self.assertEqual("F  21", s.name, "Assert name")
            self.assertEqual(90210, s.zai, "Assert zai")
            self.assertEqual(106, s.number, "Assert number")
            self.assertEqual("x", s.type, "Assert type")
            self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
            self.assertEqual(6.31343E-04, s.mean_energy, "Assert mean_energy")
            self.assertEqual(6.31343E-05, s.mean_energy_unc, "Assert mean_energy_unc")
            self.assertEqual(1.00000E+00, s.normalisation, "Assert normalisation")
            self.assertEqual(0.0, s.normalisation_unc, "Assert normalisation_unc")

            # last entry
            s = pl.spectral_mean_data[-1]
            self.assertEqual("Rg272", s.name, "Assert name")
            self.assertEqual(1112720, s.zai, "Assert zai")
            self.assertEqual(3875, s.number, "Assert number")
            self.assertEqual("no spectral data", s.type, "Assert type")
            self.assertEqual(0, s.nr_of_lines, "Assert default")
            self.assertEqual(0.0, s.mean_energy, "Assert default")
            self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
            self.assertEqual(0.0, s.normalisation, "Assert default")
            self.assertEqual(0.0, s.normalisation_unc, "Assert default")

    def test_default_spectra_mean(self):
        s = SpectralMeanData()
        self.assertEqual("", s.name, "Assert default")
        self.assertEqual(0, s.zai, "Assert default")
        self.assertEqual(0, s.number, "Assert default")
        self.assertEqual("", s.type, "Assert default")
        self.assertEqual(0, s.nr_of_lines, "Assert default")
        self.assertEqual(0.0, s.mean_energy, "Assert default")
        self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
        self.assertEqual(0.0, s.normalisation, "Assert default")
        self.assertEqual(0.0, s.normalisation_unc, "Assert default")

    def test_default_spectra_mean_deserialize(self):
        s = SpectralMeanData()
        linedump = ['  He  8    20080    13   gamma                 1    8.63104E+05 +- 9.80839E+03  8.80000E-01 +- 0.00000E+00\n']
        s.fispact_deserialize(linedump)
        self.assertEqual("He  8", s.name, "Assert name")
        self.assertEqual(20080, s.zai, "Assert zai")
        self.assertEqual(13, s.number, "Assert number")
        self.assertEqual("gamma", s.type, "Assert type")
        self.assertEqual(1, s.nr_of_lines, "Assert nr_of_lines")
        self.assertEqual(8.63104E+05, s.mean_energy, "Assert mean_energy")
        self.assertEqual(9.80839E+03, s.mean_energy_unc, "Assert mean_energy_unc")
        self.assertEqual(8.80000E-01, s.normalisation, "Assert normalisation")
        self.assertEqual(0.0, s.normalisation_unc, "Assert normalisation_unc")

        linedump = ['  Be  5    40050    25   no spectral data\n']
        s.fispact_deserialize(linedump)
        self.assertEqual("Be  5", s.name, "Assert name")
        self.assertEqual(40050, s.zai, "Assert zai")
        self.assertEqual(25, s.number, "Assert number")
        self.assertEqual("no spectral data", s.type, "Assert type")
        self.assertEqual(0, s.nr_of_lines, "Assert default")
        self.assertEqual(0.0, s.mean_energy, "Assert default")
        self.assertEqual(0.0, s.mean_energy_unc, "Assert default")
        self.assertEqual(0.0, s.normalisation, "Assert default")
        self.assertEqual(0.0, s.normalisation_unc, "Assert default")
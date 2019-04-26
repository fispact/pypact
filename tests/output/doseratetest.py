import math

import pypact as pp
from pypact.util.numerical import nan

from tests.output.baseoutputtest import BaseOutputUnitTest


class DoseRateAssertor(BaseOutputUnitTest):

    def assert_defaults(self, doserate):
        self.assert_dose_rate(doserate, "", 0.0, 0.0, 0.0)

    def assert_dose_rate(self, doserate, type, distance, mass, dose):
        if not math.isnan(dose):
            self.assertValueAndType(doserate, pp.DoseRate, 'dose', float, dose)

        self.assertValueAndType(doserate, pp.DoseRate, 'type', str, type)
        self.assertValueAndType(doserate, pp.DoseRate, 'distance', float, distance)
        self.assertValueAndType(doserate, pp.DoseRate, 'mass', float, mass)

    def assert_timestep(self, doserate, timestep):
        if timestep == 2:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 2.94608E-05)
        elif timestep == 3:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.51367E-05)
        elif timestep == 4:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79269E-05)
        elif timestep == 5:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79579E-05)
        elif timestep == 6:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79444E-05)
        elif timestep == 7:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79447E-05)
        elif timestep == 8:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79447E-05)
        elif timestep == 9:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79447E-05)
        elif timestep == 10:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79444E-05)
        elif timestep == 11:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79442E-05)
        elif timestep == 12:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79443E-05)
        elif timestep == 13:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79445E-05)
        elif timestep == 14:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79451E-05)
        elif timestep == 15:
            self.assert_dose_rate(doserate, "PLANE SOURCE", 0.0, 0.0, 4.79464E-05)
        else:
            self.assert_dose_rate(doserate, "", 0.0, 0.0, nan)


class DoseRateUnitTest(BaseOutputUnitTest):

    assertor = DoseRateAssertor()

    def test_fispact_deserialize(self):
        def func(dr, i):
            dr.fispact_deserialize(self.filerecord91, i)
            self.assertor.assert_timestep(dr, i)

        self._wrapper(func)

    def test_fispact_readwriteread(self):

        def func(dr, i):
            # deserialize from standard output
            dr.fispact_deserialize(self.filerecord91, i)
            self.assertor.assert_timestep(dr, i)

            # serialize to JSON
            j = dr.json_serialize()

            # reset object
            newdr = pp.DoseRate()
            self.assertor.assert_defaults(newdr)

            # deserialize JSON and compare to original
            newdr.json_deserialize(j)
            self.assertor.assert_timestep(newdr, i)

        self._wrapper(func)

    def test_fispact_deserialize_point_source(self):
        output_string = """
                                                       COMPOSITION  OF  MATERIAL  BY  ELEMENT
                                                       --------------------------------------
        0                                                             BETA                     GAMMA                     ALPHA
                              ATOMS      GRAM-ATOMS     GRAMS      CURIES-MeV      kW        CURIES-MeV      kW        CURIES-MeV      kW

           26       Fe      1.0784E+22   1.7907E-02   1.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00
        1 * * * TIME INTERVAL   4 * * * * * * * TIME IS   3.0000E+02 SECS OR  5.0000E+00 MINS  * * * ELAPSED TIME IS   5.000 m   * * * FLUX AMP IS  1.1160E+10 /cm^2/s  * * *
          NUCLIDE        ATOMS         GRAMS        Bq       b-Energy    a-Energy   g-Energy    DOSE RATE   INGESTION  INHALATION   HALF LIFE
                                                                kW          kW         kW         Sv/hr      DOSE(Sv)    DOSE(Sv)    seconds

          H   1    #  7.02629E+09   1.176E-14   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          H   2    #  2.01346E+08   6.734E-16   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          H   3       2.88738E+05   1.446E-18   5.144E-04   4.703E-22   0.00E+00   0.000E+00   0.000E+00   2.160E-14   1.337E-13   3.891E+08
          He  3    #  3.61000E+03   1.808E-20   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          He  4    #  1.32403E+09   8.800E-15   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          V  50       1.18223E+04   9.805E-19   1.855E-21   4.660E-39   0.00E+00   4.230E-37   3.118E-34   1.187E-29   2.040E-29   4.418E+24
          V  51    #  7.55029E+03   6.387E-19   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Cr 50       2.44413E+06   2.027E-16   2.982E-19   5.577E-35   0.00E+00   0.000E+00   0.000E+00   3.877E-28   3.877E-28   5.680E+24
          Cr 51       1.71528E+08   1.451E-14   4.967E+01   2.917E-17   0.00E+00   2.603E-16   2.840E-13   1.888E-09   1.838E-09   2.394E+06
          Cr 52    #  2.86672E+07   2.473E-15   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Cr 53    #  1.10736E+09   9.735E-14   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Cr 54    #  2.41527E+07   2.163E-15   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Cr 55       1.18626E+06   1.082E-16   3.871E+03   6.801E-13   0.00E+00   2.632E-15   2.985E-13   5.420E-09   2.400E-09   2.124E+02
          Mn 53       1.34345E+09   1.181E-13   8.019E-06   5.141E-24   0.00E+00   1.827E-24   1.534E-20   2.406E-16   4.330E-16   1.161E+14
          Mn 54       5.73671E+08   5.138E-14   1.474E+01   9.513E-18   0.00E+00   1.975E-15   1.625E-12   1.047E-08   2.212E-08   2.697E+07
          Mn 55    #  2.10930E+09   1.924E-13   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Mn 56       3.10348E+09   2.883E-13   2.314E+05   3.044E-11   0.00E+00   6.340E-11   4.704E-08   5.785E-05   2.777E-05   9.297E+03
          Mn 57  ?    1.51924E+07   1.436E-15   1.233E+05   2.182E-11   0.00E+00   1.968E-12   2.730E-09   1.973E-07   8.262E-08   8.540E+01
          Mn 58       3.63231E+05   3.495E-17   3.862E+03   1.059E-12   0.00E+00   1.474E-12   1.120E-09   1.622E-08   6.565E-09   6.520E+01
          Mn 58m      1.48266E+04   1.426E-18   3.806E+03   1.725E-12   0.00E+00   7.322E-14   4.422E-11   4.568E-10   1.979E-10   2.700E+00
          Fe 53       1.65821E+07   1.458E-15   2.251E+04   3.992E-12   0.00E+00   4.271E-12   3.547E-09   2.071E-07   2.026E-07   5.106E+02
          Fe 54    #> 6.30304E+20   5.646E-02   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Fe 55       1.46072E+10   1.333E-12   1.173E+02   7.525E-17   0.00E+00   3.122E-17   2.724E-13   3.871E-08   9.033E-08   8.631E+07
          Fe 56    #> 9.89443E+21   9.190E-01   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Fe 57    #> 2.28506E+20   2.160E-02   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Fe 58    #> 3.04099E+19   2.925E-03   0.000E+00   0.000E+00   0.00E+00   0.000E+00   0.000E+00   0.000E+00   0.000E+00     Stable
          Fe 59       1.51931E+05   1.487E-17   2.739E-02   5.195E-19   0.00E+00   5.219E-18   3.996E-15   4.931E-11   1.096E-10   3.844E+06
        0  TOTAL NUMBER OF NUCLIDES PRINTED IN INVENTORY =   27
        0  TOTAL CURIES   TOTAL ALPHA   TOTAL BETA    TOTAL GAMMA
                          CURIE-MeV     CURIE-MeV     CURIE-MeV
           1.05117E-05   0.00000E+00   1.00736E-05   1.20098E-05
        0  ALPHA BECQUERELS = 0.000000E+00  BETA BECQUERELS = 3.889323E+05  GAMMA BECQUERELS = 0.000000E+00
        0  TOTAL ACTIVITY FOR ALL MATERIALS     3.88932E+05 Bq
                                                8.27795E-08 Ci/cc           DENSITY   7.88E+00 gm/cc
           TOTAL ACTIVITY EXCLUDING TRITIUM     3.88932E+05 Bq
                                                8.27795E-08 Ci/cc
        0  TOTAL ALPHA HEAT PRODUCTION          0.00000E+00 kW
           TOTAL BETA  HEAT PRODUCTION          5.97166E-11 kW
           TOTAL GAMMA HEAT PRODUCTION          7.11948E-11 kW              TOTAL HEAT PRODUCTION 1.30911E-10 kW
        0  INITIAL TOTAL MASS OF MATERIAL       1.00000E-03 kg              TOTAL HEAT EX TRITIUM 1.30911E-10 kW
        0  TOTAL MASS OF MATERIAL               1.00000E-03 kg
           NEUTRON  FLUX DURING INTERVAL        1.11600E+10 n/cm**2/s
        0  NUMBER OF FISSIONS                   0.00000E+00                 BURN-UP OF ACTINIDES  0.00000E+00 %
        0  INGESTION  HAZARD FOR ALL MATERIALS  5.83256E-05 Sv/kg
           INHALATION HAZARD FOR ALL MATERIALS  2.81758E-05 Sv/kg
        0  INGESTION  HAZARD EXCLUDING TRITIUM  5.83256E-05 Sv/kg
           INHALATION HAZARD EXCLUDING TRITIUM  2.81758E-05 Sv/kg
        0  Total Displacement Rate (n,Ddiss) =  3.31164E+10 Displacements/sec  =  3.07098E-12 Displacements Per Atom/sec  =  9.69127E-05 DPA/year
           Total Displacement Rate (n,Dinel) =  7.33324E+10 Displacements/sec  =  6.80033E-12 Displacements Per Atom/sec  =  2.14602E-04 DPA/year
           Total Displacement Rate (n,Del  ) =  5.72789E+10 Displacements/sec  =  5.31164E-12 Displacements Per Atom/sec  =  1.67623E-04 DPA/year
           Total Displacement Rate (n,Dtot ) =  2.54427E+11 Displacements/sec  =  2.35938E-11 Displacements Per Atom/sec  =  7.44563E-04 DPA/year
        0  KERMA RATE (n,Kktot) =  9.70045E+14 eV/sec = 1.55418E-04 kW/kg = 1.22392E-06 kW/cm^3
           KERMA RATE (n,Kphot) =  7.54258E+14 eV/sec = 1.20845E-04 kW/kg = 9.51658E-07 kW/cm^3
           KERMA RATE (n,Kfiss) =  0.00000E+00 eV/sec = 0.00000E+00 kW/kg = 0.00000E+00 kW/cm^3
           KERMA RATE (n,Kinel) =  6.77059E+14 eV/sec = 1.08477E-04 kW/kg = 8.54255E-07 kW/cm^3
           KERMA RATE (n,Knone) =  1.01548E+15 eV/sec = 1.62697E-04 kW/kg = 1.28124E-06 kW/cm^3
           KERMA RATE (n,Kel  ) =  1.11016E+13 eV/sec = 1.77867E-06 kW/kg = 1.40071E-08 kW/cm^3
           KERMA RATE (n,Ktot ) =  1.02658E+15 eV/sec = 1.64476E-04 kW/kg = 1.29525E-06 kW/cm^3
        0  GAS   RATE (n,Xa   ) =  4.41343E+06 atoms per sec =  4.09270E-10 appm/sec
           GAS   RATE (n,Xh   ) =  1.20331E+01 atoms per sec =  1.11586E-15 appm/sec
           GAS   RATE (n,Xt   ) =  9.62461E+02 atoms per sec =  8.92519E-14 appm/sec
           GAS   RATE (n,Xd   ) =  6.71155E+05 atoms per sec =  6.22382E-11 appm/sec
           GAS   RATE (n,Xp   ) =  2.34210E+07 atoms per sec =  2.17190E-09 appm/sec
        0  APPM OF He  4    =  1.2278E-07
           APPM OF He  3    =  3.3477E-13
           APPM OF H   3    =  2.6776E-11
           APPM OF H   2    =  1.8671E-08
           APPM OF H   1    =  6.5157E-07



                                                       COMPOSITION  OF  MATERIAL  BY  ELEMENT
                                                       --------------------------------------
        0                                                             BETA                     GAMMA                     ALPHA
                              ATOMS      GRAM-ATOMS     GRAMS      CURIES-MeV      kW        CURIES-MeV      kW        CURIES-MeV      kW

            1       H       7.2279E+09   1.2002E-14   1.2434E-14   7.9341E-17   4.7034E-22   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00
            2       He      1.3240E+09   2.1986E-15   8.8001E-15   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00   0.0000E+00
           23       V       1.9373E+04   3.2169E-20   1.6192E-18   7.8601E-34   4.6595E-39   7.1361E-32   4.2303E-37   0.0000E+00   0.0000E+00
           24       Cr      1.3353E+09   2.2174E-15   1.1680E-13   1.1473E-07   6.8013E-13   4.8783E-10   2.8919E-15   0.0000E+00   0.0000E+00
           25       Mn      7.1455E+09   1.1865E-14   6.5166E-13   9.2853E-06   5.5044E-11   1.1289E-05   6.6921E-11   0.0000E+00   0.0000E+00
           26       Fe      1.0784E+22   1.7907E-02   1.0000E+00   6.7349E-07   3.9925E-12   7.2049E-07   4.2711E-12   0.0000E+00   0.0000E+00



                                                       GAMMA SPECTRUM AND ENERGIES/SECOND
                                                       ----------------------------------

             NEUTRONS PER SECOND ARISING FROM SPONTANEOUS FISSION                    0.00000E+00    Entered density (g/cc)       7.88
             POWER FROM ALPHA PARTICLES (MeV per Second)                             0.00000E+00
             POWER FROM BETA  PARTICLES (MeV per Second)                             3.72722E+05
             TOTAL GAMMA POWER FROM ACTIVATION  (MeV per Second)                     4.44363E+05    Total gammas (per cc per second)      3.66428E+06
             GAMMA RAY POWER FROM ACTIVATION DECAY  MeV/s    (  0.000-  0.010 MeV)   2.18188E+02    Gammas per group (per cc per second)  3.43646E+05
                                                             (  0.010-  0.020 MeV)   1.87677E+02                                          9.85303E+04
                                                             (  0.020-  0.050 MeV)   0.00000E+00                                          0.00000E+00
                                                             (  0.050-  0.100 MeV)   0.00000E+00                                          0.00000E+00
                                                             (  0.100-  0.200 MeV)   2.41838E+03                                          1.26965E+05
                                                             (  0.200-  0.300 MeV)   6.24622E+01                                          1.96756E+03
                                                             (  0.300-  0.400 MeV)   4.73283E+03                                          1.06489E+05
                                                             (  0.400-  0.600 MeV)   2.32610E+04                                          3.66361E+05
                                                             (  0.600-  0.800 MeV)   4.91286E+03                                          5.52696E+04
                                                             (  0.800-  1.000 MeV)   1.97607E+05                                          1.72906E+06
                                                             (  1.000-  1.220 MeV)   2.02735E+02                                          1.43833E+03
                                                             (  1.220-  1.440 MeV)   4.35231E+03                                          2.57703E+04
                                                             (  1.440-  1.660 MeV)   1.71895E+03                                          8.73337E+03
                                                             (  1.660-  2.000 MeV)   1.17247E+05                                          5.04548E+05
                                                             (  2.000-  2.500 MeV)   7.30574E+04                                          2.55701E+05
                                                             (  2.500-  3.000 MeV)   1.27688E+04                                          3.65652E+04
                                                             (  3.000-  4.000 MeV)   1.40862E+03                                          3.16939E+03
                                                             (  4.000-  5.000 MeV)   4.06163E+01                                          7.10785E+01
                                                             (  5.000-  6.500 MeV)   0.00000E+00                                          0.00000E+00
                                                             (  6.500-  8.000 MeV)   0.00000E+00                                          0.00000E+00
                                                             (  8.000- 10.000 MeV)   0.00000E+00                                          0.00000E+00
                                                             ( 10.000- 12.000 MeV)   0.00000E+00                                          0.00000E+00
                                                             ( 12.000- 14.000 MeV)   0.00000E+00                                          0.00000E+00
                                                             ( 14.000- 20.000 MeV)   0.00000E+00                                          0.00000E+00

            DOSE RATE (13.2 g POINT SOURCE  12.63m) FROM GAMMAS WITH ENERGY 0-20MeV IS   5.44870E-08 Sieverts/hour   ( 5.44870E-06 Rems/hour)




                                                                                   DOMINANT NUCLIDES
                                                                                   -----------------

              NUCLIDE   ACTIVITY    PERCENT  NUCLIDE     HEAT      PERCENT  NUCLIDE  DOSE RATE    PERCENT  NUCLIDE  INGESTION    PERCENT  NUCLIDE  INHALATION   PERCENT
                          (Bq)      ACTIVITY             (kW)       HEAT              (Sv/hr)    DOSE RATE            (Sv)      INGESTION            (Sv)     INHALATION
               Total   3.8893E+05             Total   1.3091E-10             Total   5.4487E-08             Total   5.8326E-05             Total   2.8176E-05
            1  Mn 56   2.3139E+05  59.49E+00  Mn 56   9.3847E-11  71.69E+00  Mn 56   4.7043E-08  86.34E+00  Mn 56   5.7848E-05  99.18E+00  Mn 56   2.7767E-05  98.55E+00
        """.splitlines()

        dr = pp.DoseRate()
        fr = pp.InventoryFileRecord(filename=None,asstring=output_string)
        self.assertor.assert_defaults(dr)
        dr.fispact_deserialize(fr, 1)
        self.assertor.assert_defaults(dr)
        dr.fispact_deserialize(fr, 2)
        self.assertor.assert_defaults(dr)
        dr.fispact_deserialize(fr, 3)
        self.assertor.assert_defaults(dr)
        dr.fispact_deserialize(fr, 4)
        self.assertor.assert_dose_rate(dr, type='POINT SOURCE', distance=12.63, mass=13.2e-3, dose=5.44870E-08)
        dr.fispact_deserialize(fr, 5)
        self.assertor.assert_defaults(dr)

    def _wrapper(self, func):
        dr = pp.DoseRate()
        self.assertor.assert_defaults(dr)

        for i in range(-100, 100):
            func(dr, i)

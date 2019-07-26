import os
import pypact as pp

from tests.testerbase import Tester, REFERENCE_DIR


class PrintLib5UnitTest(Tester):
    def setUp(self):
        self.filename = os.path.join(os.path.join(REFERENCE_DIR), "printlib4.out")        

    def tearDown(self):
        pass

    def test_default(self):
        pl = pp.PrintLib4()
        self.assertEqual(0, len(pl), "Assert no data")

    def test_fispact_deserialize(self):
        pl = pp.PrintLib4()
        self.assertEqual(0, len(pl), "Assert no data")

        fr = pp.PrintLib4FileRecord(self.filename)
        self.assertEqual(63, fr.start_index, "Assert start index")
        self.assertEqual(53181, fr.end_index, "Assert end index")

        pl = pp.PrintLib4()
        pl.fispact_deserialize(fr)
        self.assertEqual(106236, len(pl), "Assert data")

    def test_reader(self):
        with pp.PrintLib4Reader(self.filename) as pl:
            self.assertEqual(106236, len(pl), "Assert data")

            # first entry: H   1  (n,Dtot )          6.20087E+02+- 0.00000E+00
            self.assertEqual("H1", pl[0].nuclide, "Assert first entry nuclide")
            self.assertEqual("(n,Dtot )", pl[0].reaction, "Assert first entry reaction")
            self.assertEqual("", pl[0].daughter, "Assert first entry daughter")
            self.assertEqual(6.20087E+02, pl[0].xs, "Assert first entry xs")
            self.assertEqual(0.0, pl[0].delta_xs, "Assert first entry delta xs")
            
            # second entry: H   1  (n,Del  )          6.20024E+02+- 0.00000E+00
            self.assertEqual("H1", pl[1].nuclide, "Assert 2nd entry nuclide")
            self.assertEqual("(n,Del  )", pl[1].reaction, "Assert 2nd entry reaction")
            self.assertEqual("", pl[1].daughter, "Assert 2nd entry daughter")
            self.assertEqual(6.20024E+02, pl[1].xs, "Assert 2nd entry xs")
            self.assertEqual(0.0, pl[1].delta_xs, "Assert 2nd entry delta xs")

            # 10th entry: H   1  (n,E    )  H   1   1.04108E+00+- 1.34070E+00
            self.assertEqual("H1", pl[10].nuclide, "Assert 10th entry nuclide")
            self.assertEqual("(n,E    )", pl[10].reaction, "Assert 10th entry reaction")
            self.assertEqual("H1", pl[10].daughter, "Assert 10th entry daughter")
            self.assertEqual(1.04108E+00, pl[10].xs, "Assert 10th entry xs")
            self.assertEqual(1.34070E+00, pl[10].delta_xs, "Assert 10th entry delta xs")

            # 11th entry: H   1  (n,g    )  H   2   6.38203E-05+- 8.60406E+00
            self.assertEqual("H1", pl[11].nuclide, "Assert 11th entry nuclide")
            self.assertEqual("(n,g    )", pl[11].reaction, "Assert 11th entry reaction")
            self.assertEqual("H2", pl[11].daughter, "Assert 11th entry daughter")
            self.assertEqual(6.38203E-05, pl[11].xs, "Assert 11th entry xs")
            self.assertEqual(8.60406E+00, pl[11].delta_xs, "Assert 11th entry delta xs")

            # last entries
            # 
            # Ds281  (n,np   )  Mt280   6.13655E-08+- 9.81500E+01          Ds281  (n,d    )  Mt280   2.54049E-05+- 9.54769E+01
            # Ds281  (n,p    )  Mt281   6.61453E-05+- 8.11175E+01          Ds281  (n,3n   )  Ds279   5.79544E-11+- 1.08533E+02
            # Ds281  (n,2n   )  Ds280   3.30990E-04+- 9.52456E+01          Ds281  (n,E    )  Ds281   3.38367E+00+- 1.04664E+00
            # Ds281  (n,n    )  Ds281   5.72114E-07+- 9.38494E+01          Ds281  (n,g    )  Ds282   9.58985E-02+- 1.34170E-02

            # 6th last entry: H   1  (n,g    )  H   2   6.38203E-05+- 8.60406E+00
            self.assertEqual("Ds281", pl[-6].nuclide, "Assert last entry nuclide")
            self.assertEqual("(n,p    )", pl[-6].reaction, "Assert last entry reaction")
            self.assertEqual("Mt281", pl[-6].daughter, "Assert last entry daughter")
            self.assertEqual(6.61453E-05, pl[-6].xs, "Assert last entry xs")
            self.assertEqual(8.11175E+01, pl[-6].delta_xs, "Assert last entry delta xs")

            # 3rd last entry: H   1  (n,g    )  H   2   6.38203E-05+- 8.60406E+00
            self.assertEqual("Ds281", pl[-3].nuclide, "Assert last entry nuclide")
            self.assertEqual("(n,E    )", pl[-3].reaction, "Assert last entry reaction")
            self.assertEqual("Ds281", pl[-3].daughter, "Assert last entry daughter")
            self.assertEqual(3.38367E+00, pl[-3].xs, "Assert last entry xs")
            self.assertEqual(1.04664E+00, pl[-3].delta_xs, "Assert last entry delta xs")

            # last entry: H   1  (n,g    )  H   2   6.38203E-05+- 8.60406E+00
            self.assertEqual("Ds281", pl[-1].nuclide, "Assert last entry nuclide")
            self.assertEqual("(n,g    )", pl[-1].reaction, "Assert last entry reaction")
            self.assertEqual("Ds282", pl[-1].daughter, "Assert last entry daughter")
            self.assertEqual(9.58985E-02, pl[-1].xs, "Assert last entry xs")
            self.assertEqual(1.34170E-02, pl[-1].delta_xs, "Assert last entry delta xs")
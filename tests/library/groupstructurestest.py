import math
import pypact as pp

from tests.testerbase import Tester


DECIMAL_PLACE_ACC = 6

class GroupStructuresUnitTest(Tester):

    def test_group66(self):
        g = pp.ALL_GROUPS[66]
        self.assertEqual(67, len(g), "Assert the length of group 66 is 67")
        
        self.assertEqual(2.50e7, g[0], "Assert the first entry for group 66")
        self.assertEqual(1.49e7, g[3], "Assert the forth entry for group 66")
        self.assertEqual(1.00e-5, g[-1], "Assert the last entry for group 66")
    
        # for regression check the sum of all entries
        self.assertAlmostEqual(113960160.65750997, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 66")
                               
        self._check_list_is_decreasing(g)

    def test_group66r(self):
        g = pp.ALL_GROUPS[-66]
        self.assertEqual(67, len(g), "Assert the length of group 66 is 67")
        
        self.assertEqual(1.00e-5, g[0], "Assert the first entry for group 66")
        self.assertEqual(1.49e7, g[-4], "Assert the forth from last entry for group 66")
        self.assertEqual(2.50e7, g[-1], "Assert the last entry for group 66")
    
        # for regression check the sum of all entries
        self.assertAlmostEqual(113960160.65750997, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 66")
                               
        self._check_list_is_increasing(g)
    
    def test_group69(self):
        g = pp.ALL_GROUPS[69]
        self.assertEqual(70, len(g), "Assert the length of group 69 is 70")
        
        self.assertEqual(1.00000E7, g[0], "Assert the first entry for group 69")
        self.assertEqual(2.23100E6, g[3], "Assert the forth entry for group 69")
        self.assertEqual(1.00e-5, g[-1], "Assert the last entry for group 69")
    
        # for regression check the sum of all entries
        self.assertAlmostEqual(25417961.86301, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 69")
                               
        self._check_list_is_decreasing(g)
    
    def test_group69r(self):
        g = pp.ALL_GROUPS[-69]
        self.assertEqual(70, len(g), "Assert the length of group 69 is 70")
        
        self.assertEqual(1.00000E7, g[-1], "Assert the last entry for group 69")
        self.assertEqual(2.23100E6, g[-4], "Assert the forth last entry for group 69")
        self.assertEqual(1.00e-5, g[0], "Assert the first entry for group 69")
    
        # for regression check the sum of all entries
        self.assertAlmostEqual(25417961.86301, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 69")
                               
        self._check_list_is_increasing(g)

    def test_group100(self):
        g = pp.ALL_GROUPS[100]
        self.assertEqual(101, len(g), "Assert the length of group 100 is 101")
        
        self.assertEqual(1.49180E7, g[0], "Assert the first entry for group 100")
        self.assertEqual(1.10515E7, g[3], "Assert the forth entry for group 100")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 100")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(156097943.581636, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 100")
                               
        self._check_list_is_decreasing(g)

    def test_group100r(self):
        g = pp.ALL_GROUPS[-100]
        self.assertEqual(101, len(g), "Assert the length of group 100 is 101")
        
        self.assertEqual(1.49180E7, g[-1], "Assert the last entry for group 100")
        self.assertEqual(1.10515E7, g[-4], "Assert the forth last entry for group 100")
        self.assertEqual(1.0E-5, g[0], "Assert the first entry for group 100")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(156097943.581636, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 100")
                               
        self._check_list_is_increasing(g)

    def test_group162(self):
        g = pp.ALL_GROUPS[162]
        self.assertEqual(163, len(g), "Assert the length of group 162 is 163")
        
        self.assertEqual(1.000000E+09, g[0], "Assert the first entry for group 162")
        self.assertEqual(8.800000E+08, g[3], "Assert the forth entry for group 162")
        self.assertEqual(5.00000E3, g[-1], "Assert the last entry for group 162")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(14460200000.0, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 162")
                               
        self._check_list_is_decreasing(g)

    def test_group162r(self):
        g = pp.ALL_GROUPS[-162]
        self.assertEqual(163, len(g), "Assert the length of group 162 is 163")
        
        self.assertEqual(1.000000E+09, g[-1], "Assert the last entry for group 162")
        self.assertEqual(8.800000E+08, g[-4], "Assert the forth entry for group 162")
        self.assertEqual(5.00000E3, g[0], "Assert the first entry for group 162")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(14460200000.0, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 162")
                               
        self._check_list_is_increasing(g)

    def test_group172(self):
        g = pp.ALL_GROUPS[172]
        self.assertEqual(173, len(g), "Assert the length of group 172 is 173")
        
        self.assertEqual(1.96403E7, g[0], "Assert the first entry for group 172")
        self.assertEqual(1.38403E7, g[3], "Assert the forth entry for group 172")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 172")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(143972448.3481201, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 172")
                               
        self._check_list_is_decreasing(g)

    def test_group172r(self):
        g = pp.ALL_GROUPS[-172]
        self.assertEqual(173, len(g), "Assert the length of group 172 is 173")
        
        self.assertEqual(1.96403E7, g[-1], "Assert the last entry for group 172")
        self.assertEqual(1.38403E7, g[-4], "Assert the forth last entry for group 172")
        self.assertEqual(1.0E-5, g[0], "Assert the first entry for group 172")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(143972448.3481201, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 172")
                               
        self._check_list_is_increasing(g)

    def test_group175(self):
        g = pp.ALL_GROUPS[175]
        self.assertEqual(176, len(g), "Assert the length of group 175 is 176")
        
        self.assertEqual(1.96403E7, g[0], "Assert the first entry for group 175")
        self.assertEqual(1.45499E7, g[6], "Assert the seventh entry for group 175")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 175")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(431739677.108859, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 175")
                               
        self._check_list_is_decreasing(g)

    def test_group175r(self):
        g = pp.ALL_GROUPS[-175]
        self.assertEqual(176, len(g), "Assert the length of group 175 is 176")
        
        self.assertEqual(1.96403E7, g[-1], "Assert the last entry for group 175")
        self.assertEqual(1.45499E7, g[-7], "Assert the seventh last entry for group 175")
        self.assertEqual(1.0E-5, g[0], "Assert the first entry for group 175")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(431739677.108859, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 175")
                               
        self._check_list_is_increasing(g)

    def test_group211(self):
        g = pp.ALL_GROUPS[211]
        self.assertEqual(212, len(g), "Assert the length of group 211 is 212")
        
        self.assertEqual(5.5000E7, g[0], "Assert the first entry for group 211")
        self.assertEqual(5.2000E7, g[3], "Assert the forth entry for group 211")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 211")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(1781739677.1088598, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 211")
                               
        self._check_list_is_decreasing(g)

    def test_group211r(self):
        g = pp.ALL_GROUPS[-211]
        self.assertEqual(212, len(g), "Assert the length of group 211 is 212")
        
        self.assertEqual(5.5000E7, g[-1], "Assert the last entry for group 211")
        self.assertEqual(5.2000E7, g[-4], "Assert the forth last entry for group 211")
        self.assertEqual(1.0E-5, g[0], "Assert the first entry for group 211")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(1781739677.108859, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 211")
                               
        self._check_list_is_increasing(g)

    def test_group351(self):
        g = pp.ALL_GROUPS[351]
        self.assertEqual(352, len(g), "Assert the length of group 351 is 352")
        
        self.assertEqual(5.5000E7, g[0], "Assert the first entry for group 351")
        self.assertEqual(5.2000E7, g[3], "Assert the forth entry for group 351")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 351")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(1769655563.5445998, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 351")
                               
        self._check_list_is_decreasing(g)

    def test_group351r(self):
        g = pp.ALL_GROUPS[-351]
        self.assertEqual(352, len(g), "Assert the length of group 351 is 352")
        
        self.assertEqual(5.5000E7, g[-1], "Assert the last entry for group 351")
        self.assertEqual(5.2000E7, g[-4], "Assert the forth last entry for group 351")
        self.assertEqual(1.0E-5, g[0], "Assert the first entry for group 351")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(1769655563.5445998, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 351")
                               
        self._check_list_is_increasing(g)

    def test_group586(self):
        g = pp.ALL_GROUPS[586]
        self.assertEqual(587, len(g), "Assert the length of group 586 is 587")
        
        self.assertEqual(2.00000E7, g[0], "Assert the first entry for group 586")
        self.assertEqual(1.6487E+07, g[3], "Assert the forth entry for group 586")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 586")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(432119907.0250101, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 586")
                               
        self._check_list_is_decreasing(g)

    def test_group586r(self):
        g = pp.ALL_GROUPS[-586]
        self.assertEqual(587, len(g), "Assert the length of group 586 is 587")
        
        self.assertEqual(2.00000E7, g[-1], "Assert the last entry for group 586")
        self.assertEqual(1.6487E+07, g[-4], "Assert the forth last entry for group 586")
        self.assertEqual(1.0E-5, g[-0], "Assert the first entry for group 586")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(432119907.0250101, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 586")
                               
        self._check_list_is_increasing(g)
    
    def test_group616(self):
        g = pp.ALL_GROUPS[616]
        self.assertEqual(617, len(g), "Assert the length of group 616 is 617")
        
        self.assertEqual(2.00000E7, g[0], "Assert the first entry for group 616")
        self.assertEqual(1.81970E7, g[3], "Assert the forth entry for group 616")
        self.assertEqual(1.0E-5, g[-1], "Assert the last entry for group 616")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(463318411.1208999, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 616")
                               
        self._check_list_is_decreasing(g)
    
    def test_group616r(self):
        g = pp.ALL_GROUPS[-616]
        self.assertEqual(617, len(g), "Assert the length of group 616 is 617")
        
        self.assertEqual(2.00000E7, g[-1], "Assert the last entry for group 616")
        self.assertEqual(1.81970E7, g[-4], "Assert the forth last entry for group 616")
        self.assertEqual(1.0E-5, g[0], "Assert the first entry for group 616")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(463318411.1208999, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 616")
                               
        self._check_list_is_increasing(g)
    
    def test_group709(self):
        g = pp.ALL_GROUPS[709]
        self.assertEqual(710, len(g), "Assert the length of group 709 is 710")
        
        self.assertEqual(1.0e+09, g[0], "Assert the first entry for group 709")
        self.assertEqual(8.8e+08, g[3], "Assert the forth entry for group 709")
        self.assertEqual(1.0e-5, g[-1], "Assert the last entry for group 709")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(15992185618.888683, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 709")
                               
        self._check_list_is_decreasing(g)
    
    def test_group709r(self):
        g = pp.ALL_GROUPS[-709]
        self.assertEqual(710, len(g), "Assert the length of group 709 is 710")
        
        self.assertEqual(1.0e+09, g[-1], "Assert the last  entry for group 709")
        self.assertEqual(8.8e+08, g[-4], "Assert the forth last entry for group 709")
        self.assertEqual(1.0e-5, g[0], "Assert the first entry for group 709")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(15992185618.888676, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 709")
                               
        self._check_list_is_increasing(g)
    
    def test_group1102(self):
        g = pp.ALL_GROUPS[1102]
        self.assertEqual(1103, len(g), "Assert the length of group 1102 is 1103")
        
        self.assertEqual(1.0000e+09, g[0], "Assert the first entry for group 1102")
        self.assertEqual(8.7096e+08, g[3], "Assert the forth entry for group 1102")
        self.assertEqual(1.0000e-5, g[-1], "Assert the last entry for group 1102")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(23889164999.810318, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 1102")

        self._check_list_is_decreasing(g)
    
    def test_group1102r(self):
        g = pp.ALL_GROUPS[-1102]
        self.assertEqual(1103, len(g), "Assert the length of group 1102 is 1103")
        
        self.assertEqual(1.0000e+09, g[-1], "Assert the last entry for group 1102")
        self.assertEqual(8.7096e+08, g[-4], "Assert the forth last entry for group 1102")
        self.assertEqual(1.0000e-5, g[0], "Assert the first entry for group 1102")
        
        # for regression check the sum of all entries
        self.assertAlmostEqual(23889164999.81031, sum(g),
                               places=DECIMAL_PLACE_ACC,
                               msg="Assert the sum of all entries of 1102")

        self._check_list_is_increasing(g)

    def _check_list_is_decreasing(self, l):
        self.assertTrue(all(earlier >= later for earlier, later in zip(l, l[1:])),
                        "Assert list is in descending order")

    def _check_list_is_increasing(self, l):
        self.assertTrue(all(earlier < later for earlier, later in zip(l, l[1:])),
                        "Assert list is in ascending order")

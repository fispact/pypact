import math
import pypact as pp

from tests.testerbase import Tester


class GroupStructuresUnitTest(Tester):
    def test_group66(self):
        g = pp.ALL_GROUPS[66]
        self.assertEqual(67, len(g), "Assert the length of group 66 is 67")
        
        self.assertEqual(2.50e7, g[0], "Assert the first entry for group 66")
        self.assertEqual(1.49e7, g[3], "Assert the forth entry for group 66")
        self.assertEqual(1.00e-5, g[-1], "Assert the last entry for group 66")

    def test_group709(self):
        g = pp.ALL_GROUPS[709]
        self.assertEqual(710, len(g), "Assert the length of group 709 is 710")
        
        self.assertEqual(1.0e+09, g[0], "Assert the first entry for group 709")
        self.assertEqual(8.8e+08, g[3], "Assert the forth entry for group 709")
        self.assertEqual(1.0e-5, g[-1], "Assert the last entry for group 709")

import math
import numpy as np
import pypact as pp

from tests.testerbase import Tester


DECIMAL_PLACE_ACC = 6


class GroupConvertUnitTest(Tester):

    def _test_imp(self, in_group, in_values, out_group, expected_values, almost=False):
        if almost:
            np.testing.assert_almost_equal(expected_values, pp.groupconvert.by_energy(
                in_group, in_values, out_group), err_msg="Assert group convert")
        else:
            self.assertEqual(expected_values, pp.groupconvert.by_energy(
                in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_overlap(self):
        in_group = [0.0, 1.0]
        in_values = [1.0]
        out_group = [0.5, 1.0]
        expected_values = [0.5]
        self._test_imp(in_group, in_values, out_group, expected_values)

    def test_byenergy_simple_overlap2(self):
        in_group = [0.0, 1.0]
        in_values = [1.0]
        out_group = [0.0, 0.5]
        expected_values = [0.5]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_adjacent(self):
        in_group = [0.0, 1.0]
        in_values = [1.0]
        out_group = [1.0, 1.5]
        expected_values = [0.0]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_adjacent2(self):
        in_group = [0.0, 1.0]
        in_values = [1.0]
        out_group = [-1.0, 0.0]
        expected_values = [0.0]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_same(self):
        in_group = [0.0, 1.0]
        in_values = [1.0]
        out_group = [0.0, 1.0]
        expected_values = [1.0]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_same2(self):
        in_group = [0.0, 1.0, 2.0]
        in_values = [1.0, 0.7]
        out_group = [0.0, 1.0, 2.0]
        expected_values = [1.0, 0.7]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_negative1(self):
        in_group = [-1.0, 0.0, 1.0]
        in_values = [5.0, 8.0]
        out_group = [0.0, 0.5, 0.75, 1.0]
        expected_values = [4.0, 2.0, 2.0]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_simple_negative2(self):
        in_group = [-1.0, 0.0, 1.0]
        in_values = [5.0, 8.0]
        out_group = [-10.0, 0.5, 0.75, 1.0]
        expected_values = [9.0, 2.0, 2.0]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

    def test_byenergy_case1(self):
        self._test_imp([0.2, 0.5], [8], [0., 0.4, 0.5],
                       [16./3., 8./3.], almost=True)

    def test_byenergy_case2(self):
        self._test_imp([0, 0.1, 2], [2, 3], [0.1, 0.25, 0.5, 0.75, 0.9],
                       [0.23684210526315788, 0.39473684210526316, 0.39473684210526305, 0.23684210526315788], almost=True)

    def test_byenergy_case3(self):
        self._test_imp([0, 0.2, 2], [2, 3], [0.1, 0.25, 0.5, 0.75, 0.9],
                       [1.0833333333333333, 0.41666666666666663, 0.41666666666666663, 0.25], almost=True)

    def test_byenergy_case4(self):
        self._test_imp([0, 0.2, 0.3, 0.4, 0.55], [2, 3, 1, 8], [0.1, 0.25, 0.5, 0.75, 0.9],
                       [2.5, 7.833333333333331, 2.6666666666666687, 0.0], almost=True)

    def test_byenergy_709_to_single(self):
        g_709 = list(reversed(pp.ALL_GROUPS[709]))
        self._test_imp(g_709, [1.0]*709, [1e6, 2e6],
                       [15.050386030584683], almost=True)

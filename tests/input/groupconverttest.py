import math
import pypact as pp

from tests.testerbase import Tester


DECIMAL_PLACE_ACC = 6


class GroupConvertUnitTest(Tester):

    def test_byenergy_simple_overlap(self):
        in_group = [0.0, 1.0]
        in_values = [1.0]
        out_group = [0.5, 1.0]
        expected_values = [0.5]
        self.assertEqual(expected_values, pp.groupconvert.by_energy(
            in_group, in_values, out_group), "Assert group convert")

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

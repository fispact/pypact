import os
import re
import pytest

import numpy as np
from numpy.testing import assert_array_equal

from tests.testerbase import REFERENCE_DIR
from pypact.filerecord import InventoryFileRecord as FileRecord
from pypact.output.timestep import TimeStep
from pypact.output.gammaspectrum import GammaSpectrum, GAMMA_SPECTRUM_LINE_MATCHER, FLOAT_NUMBER

data_file_name = os.path.join(REFERENCE_DIR, "gamma_spectra_read_bug.out")
file_record = FileRecord(data_file_name)

EXPECTED_BOUNDARIES = np.array([
    1e-3,
    0.01,
    0.02,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.60,
    0.80,
    1.00,
    1.22,
    1.44,
    1.66,
    2.00,
    2.50,
    3.00,
    4.00,
    5.00,
    6.50,
    8.00,
    10.00,
    12.00,
    14.00,
    20.00,
])


def assert_is_valid_gs(gs: GammaSpectrum):
    assert gs is not None, "Time step has no gamma spectrum"
    actual_boundaries = np.array(gs.boundaries)
    assert_array_equal(EXPECTED_BOUNDARIES, actual_boundaries), "Boundaries are invalid"
    actual_values = np.array(gs.values)
    assert actual_values.size == actual_boundaries.size - 1
    assert np.all(actual_values == 0.0), \
        "All the gamma spectra values in the given out file are expected to be zero"


def test_every_time_step_has_valid_gamma_spectra():
    size = len(file_record.timesteps)
    assert size == 63, "Unexpected number of time-steps in the test file gamma_spectra_read_bug.out"
    for i in range(1, size + 1):
        ts = TimeStep()
        ts.fispact_deserialize(file_record, i)
        gs = ts.gamma_spectrum
        assert_is_valid_gs(gs)


FLOAT_NUMBER_MATCHER = re.compile(FLOAT_NUMBER, re.IGNORECASE)


@pytest.mark.parametrize("input, expected", [
    ("1.0", 1.0),
    ("0.01", 0.01),
    ("1e-3", 0.001),
    ("1.0e-3", 0.001),
])
def test_float_number_pattern(input, expected):
    match = FLOAT_NUMBER_MATCHER.match(input)
    actual = float(match.group(0))
    assert expected == actual, f"Cannot match value {input}"


@pytest.mark.parametrize("input, lower_boundary, upper_boundary, value", [
    ("     GAMMA RAY POWER FROM ACTIVATION DECAY  MeV/s        ( 1e-3- 0.01 MeV)   0.00000E+00    Gammas per group (per cc per second)  0.00000E+00",
       1.0e-3, 0.01, 0.0
    ),
    (
    "                                                         ( 0.01- 0.02 MeV)   0.00000E+00                                          0.00000E+00",
      0.01, 0.02, 0.0
    ),
    (
    "                                                         ( 8.00-10.00 MeV)   0.00000E+00                                          0.00000E+00",
      8.0, 10.0, 0.0
    ),
])
def test_gamma_spectrum_line_pattern(input, lower_boundary, upper_boundary, value):
    match = GAMMA_SPECTRUM_LINE_MATCHER.match(input)
    assert match
    actual_lower_boundary = float(match.group("lb"))
    actual_upper_boundary = float(match.group("ub"))
    actual_value = float(match.group("value"))
    assert lower_boundary == actual_lower_boundary
    assert upper_boundary == actual_upper_boundary
    assert value == actual_value


if __name__ == '__main__':
    pytest.main()

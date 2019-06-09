import os
import pytest

import numpy as np
from numpy.testing import assert_array_equal

from tests.testerbase import REFERENCE_DIR
from pypact.filerecord import InventoryFileRecord as FileRecord
from pypact.output.timestep import TimeStep, GammaSpectrum

data_file_name = os.path.join(REFERENCE_DIR, "gamma_spectra_read_bug.out")
file_record = FileRecord(data_file_name)

EXPECTED_BOUNDARIES = np.array([
    0.00,
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


if __name__ == '__main__':
    pytest.main()

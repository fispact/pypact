import os
import pytest

import numpy as np
from numpy.testing import assert_array_equal

import typing as tp


from tests.testerbase import REFERENCE_DIR
from pypact.filerecord import InventoryFileRecord as FileRecord
from pypact.output.timestep import TimeStep, GammaSpectrum

data_file_name = os.path.join(REFERENCE_DIR, "gamma_spectra_read_bug.out")
file_record = FileRecord(data_file_name)

EXPECTED_BOUNDARIES = np.array([
    0.000,
    0.010,
    0.020,
    0.050,
    0.100,
    0.200,
    0.300,
    0.400,
    0.600,
    0.800,
    1.000,
    1.220,
    1.440,
    1.660,
    2.000,
    2.500,
    3.000,
    4.000,
    5.000,
    6.500,
    8.000,
    10.000,
    12.000,
    14.000,
    20.000
])


def assert_is_valid_gs(gs:GammaSpectrum):
    assert gs is not None, "Time step has no gamma spectrum"
    actual_boundaries = np.array(gs.boundaries)
    assert_array_equal(EXPECTED_BOUNDARIES, actual_boundaries), "Boundaries are invalid"
    assert np.all(actual_boundaries == 0.0), \
        "All the gamma spectra values in the given file expected to be zero"



def test_every_time_step_has_valid_gamma_spectra():
    size = len(file_record.timesteps)
    assert size == 63, "Unexpected number of time-steps in the test file gamma_spectra_read_bug.out"
    for i in range(1, size + 1):
        ts: TimeStep = TimeStep()
        ts.fispact_deserialize(file_record, i)
        gs: GammaSpectrum = ts.gamma_spectrum
        assert_is_valid_gs(gs)


if __name__ == '__main__':
    pytest.main()

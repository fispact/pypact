import os
import pypact as pp
import pytest

from tests.testerbase import REFERENCE_DIR
from pypact.output.timestep import TimeStep

data_file_name = os.path.join(REFERENCE_DIR, "test_dpa.out")
filerecord = pp.FileRecord(data_file_name)


@pytest.mark.parametrize("interval, time, total_displacement_rate", [
    (1, 3.1558E+07, 8.62332E-12),
    (2, 3.1558E+07, 3.45006E-11),
    (3, 3.1558E+07, 3.45080E-11),
    (4, 3.1558E+07, 3.45155E-11),
])
def test_timestep_reads_dpa_and_time(interval, time, total_displacement_rate):
    ts = TimeStep()
    ts.fispact_deserialize(filerecord, interval)
    assert total_displacement_rate == ts.total_displacement_rate
    assert time == ts.time

import pypact as pp

from tests.output.baseoutputtest import BaseOutputUnitTest
from tests.output.rundatatest import RunDataAssertor
from tests.output.timesteptest import TimeStepAssertor


class ReaderUnitTest(BaseOutputUnitTest):

    def setUp(self):
        super(ReaderUnitTest, self).setUp()
        self.rdassertor = RunDataAssertor()
        self.ivassertor = TimeStepAssertor()

    def _assert_test91(self, output):
        rd = output.run_data
        expectedrd = pp.RunData()
        expectedrd.timestamp = "12:35:22 13 January 2018"
        expectedrd.run_name = "*PWR FUEL 3.1% U235 FBR-Na End of Cycle"
        expectedrd.flux_name = "FBR-Na End of Cycle heavy fuel s"
        self.rdassertor.assert_run_data(expectedrd, rd)

        iv = output.inventory_data
        self.assertEqual(15, len(iv), "Assert length of inventory steps")

    def test_reader_output(self):
        with pp.Reader(self.filename_test91out) as o:
            self._assert_test91(o)

    def test_reader_json(self):
        with pp.Reader(self.filename_test91json) as o:
            self._assert_test91(o)


from tests.output.baseoutputtest import BaseOutputUnitTest

import pypact as pp


class RunDataAssertor(BaseOutputUnitTest):

    def assert_defaults(self, rundata):
        self.assert_run_data(rundata, run_data_default())

    def assert_run_data(self, rundata, compared):
        self.assertValueAndType(rundata, pp.RunData, 'timestamp', str, compared.timestamp)
        self.assertValueAndType(rundata, pp.RunData, 'run_name', str, compared.run_name)
        self.assertValueAndType(rundata, pp.RunData, 'flux_name', str, compared.flux_name)

    def assert_run(self, rundata):
        self.assert_run_data(rundata, run_data_output())


def run_data_default():
    rd = pp.RunData()
    rd.timestamp = ""
    rd.run_name = ""
    rd.flux_name = ""
    return rd


def run_data_output():
    rd = pp.RunData()
    rd.timestamp = "12:35:22 13 January 2018"
    rd.run_name = "*PWR FUEL 3.1% U235 FBR-Na End of Cycle"
    rd.flux_name = "FBR-Na End of Cycle heavy fuel s"
    return rd


class RunDataUnitTest(BaseOutputUnitTest):

    assertor = RunDataAssertor()

    def test_fispact_deserialize(self):

        def func(rd):
            rd.fispact_deserialize(self.filerecord91)
            self.assertor.assert_run(rd)

        self._wrapper(func)

    def test_fispact_readwriteread(self):

        def func(rd):
            rd.fispact_deserialize(self.filerecord91)
            self.assertor.assert_run(rd)

            # serialize to JSON
            j = rd.json_serialize()

            # reset object
            newrd = pp.RunData()
            self.assertor.assert_defaults(newrd)

            # deserialize JSON and compare to original
            newrd.json_deserialize(j)
            self.assertor.assert_run(newrd)

        self._wrapper(func)

    def _wrapper(self, func):

        rd = pp.RunData()
        self.assertor.assert_defaults(rd)

        func(rd)

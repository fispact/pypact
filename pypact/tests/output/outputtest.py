from pypact.tests.output.baseoutputtest import BaseOutputUnitTest
from pypact.tests.output.rundatatest import RunDataAssertor
from pypact.tests.output.timesteptest import TimeStepAssertor
from pypact.output.output import Output


class OutputAssertor(BaseOutputUnitTest):
    rd_assertor = RunDataAssertor()
    ts_assertor = TimeStepAssertor()

    def assert_defaults(self, output):
        self.assertEqual(len(output.inventory_data), 0)
        self.rd_assertor.assert_defaults(output.run_data)

    def assert_output(self, output):
        self.rd_assertor.assert_run(output.run_data)
        for i in range(0, len(output.inventory_data)):
            self.ts_assertor.assert_timestep(output.inventory_data[i], i+1)


class OutputUnitTest(BaseOutputUnitTest):

    assertor = OutputAssertor()

    def test_fispact_deserialize(self):

        def func(output):
            output.fispact_deserialize(self.filerecord91)
            self.assertor.assert_output(output)

        self._wrapper(func)

    def test_fispact_readwriteread(self):

        def func(output):
            # deserialize from standard output
            output.fispact_deserialize(self.filerecord91)
            self.assertor.assert_output(output)

            # serialize to JSON
            j = output.json_serialize()

            # reset object
            newout = Output()
            self.assertor.assert_defaults(newout)

            # deserialize JSON and compare to original
            newout.json_deserialize(j)
            self.assertor.assert_output(newout)

        self._wrapper(func)

    def _wrapper(self, func):
        output = Output()
        self.assertor.assert_defaults(output)

        func(output)

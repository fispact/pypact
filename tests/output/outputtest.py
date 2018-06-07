from tests.output.baseoutputtest import BaseOutputUnitTest
from tests.output.rundatatest import RunDataAssertor
from tests.output.timesteptest import TimeStepAssertor

from pypact.output.output import Output


class OutputAssertor(BaseOutputUnitTest):
    rd_assertor = RunDataAssertor()
    ts_assertor = TimeStepAssertor()

    def assert_defaults(self, output):
        self.assert_length(output, 0)
        self.rd_assertor.assert_defaults(output.run_data)

    def assert_output(self, output):
        self.rd_assertor.assert_run(output.run_data)
        for i in range(0, len(output.inventory_data)):
            self.ts_assertor.assert_timestep(output.inventory_data[i], i+1)

    def assert_length(self, output, length):
        self.assertEqual(len(output.inventory_data), length)


class OutputUnitTest(BaseOutputUnitTest):

    assertor = OutputAssertor()

    def test_fispact_deserialize(self):

        def func(output):
            output.fispact_deserialize(self.filerecord91)
            self.assertor.assert_output(output)

        self._wrapper(func)

    def test_fispact_deserialize_length(self):

        def func(output):
            output.fispact_deserialize(self.filerecord91)
            self.assertor.assert_length(output, len(self.jsonoutput91))

        self._wrapper(func)
    
    def test_fispact_deserialize_length2(self):

        def func(output):
            output.fispact_deserialize(self.filerecord31)
            self.assertor.assert_length(output, len(self.jsonoutput31))

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

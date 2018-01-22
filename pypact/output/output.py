from pypact.output.serializable import Serializable
from pypact.output.rundata import RunData
from pypact.output.timestep import TimeStep


class Output(Serializable):
    """
        An object to represent the output
    """
    def __init__(self):
        self.run_data = RunData()
        self.inventory_data = []

    def json_deserialize(self, j):
        super(Output, self).json_deserialize(j)
        self.json_deserialize_list(j, 'inventory_data', TimeStep)

    def fispact_deserialize(self, filerecord):

        self.__init__()

        self.run_data.fispact_deserialize(filerecord)

        for i, s in filerecord.timesteps:
            t = TimeStep()
            t.fispact_deserialize(filerecord, interval=i)
            self.inventory_data.append(t)

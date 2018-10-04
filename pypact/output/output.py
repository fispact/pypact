from pypact.util.decorators import freeze_it
from pypact.util.jsonserializable import JSONSerializable
from pypact.output.rundata import RunData
from pypact.output.timestep import TimeStep


@freeze_it
class Output(JSONSerializable):
    """
        An object to represent the output
    """
    def __init__(self, ignorenuclides=False):
        self.run_data = RunData()
        self.inventory_data = []

        self.__ignorenuclides = ignorenuclides

    def __len__(self):
        return len(self.inventory_data)

    def __getitem__(self, index):
        return self.inventory_data[index]

    def json_deserialize(self, j, objtype=object):
        super(Output, self).json_deserialize(j)
        self.json_deserialize_list(j, 'inventory_data', TimeStep)

    def fispact_deserialize(self, filerecord):

        self.__init__(ignorenuclides=self.__ignorenuclides)

        self.run_data.fispact_deserialize(filerecord)

        for i, s in filerecord.timesteps:
            t = TimeStep(ignorenuclides=self.__ignorenuclides)
            t.fispact_deserialize(filerecord, interval=i)
            self.inventory_data.append(t)

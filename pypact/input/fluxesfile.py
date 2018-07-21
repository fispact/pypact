import os
from typing import List

from pypact.input.groupstructures import ALL_GROUPS
from pypact.util.decorators import freeze_it
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.numerical import getfloat, isfloat
from pypact.util.exceptions import PypactOutOfRangeException, PypactDeserializeException


@freeze_it
class FluxesFile(JSONSerializable):
    def __init__(self, name="fluxes", norm=1.0):
        self.name: str = name
        self.norm: float = norm
    
        self.boundaries: List[float] = []
        self.values: List[float] = []
        self.midPointEnergies: List[float] = []

    def reset(self):
        self.__init__(name=self.name)

    def setGroup(self, group: int):
        if group not in ALL_GROUPS:
            raise PypactOutOfRangeException("Group {} is not a valid group".format(group))

        # group structures are in reverse order
        self._setBoundaries(group)
        self.values = [0.0]*group

    def setValue(self, energy: float, value: float):
        """
            Requires setGroup is set before
        """
        for i in range(0, len(self.boundaries)-1):
            if self.boundaries[i] > energy:
                self.values[i] = value
                return

    def validate(self):
        if len(self.boundaries) != len(self.values) + 1:
            raise PypactOutOfRangeException("Bin boundaries must be of size one greater than values size")
    
    def _setBoundaries(self, group: int):
        self.boundaries = list(reversed(ALL_GROUPS[group]))
        self.midPointEnergies = [(self.boundaries[i] + self.boundaries[i+1])/2.0 for i in range(0, group)]
    
    def _serialize(self, f):
        """
            The serialization method
            f: file object
            
            Format is:
            
            v1
            v2
            ...
            vn
            1.0
            name
        """
        for e in self.values:
            f.write("{}\n".format(e))
        f.write("{}\n".format(self.norm))
        f.write(self.name)

    def _deserialize(self, f):
        """
            The deserialization method
            f: file object
            
            Format is:
            
            v1
            v2
            ...
            vn
            1.0
            name
        """
        lines = f.readlines()
        # last two lines are the normalisation and the name
        self.name = str(lines[-1])
        self.norm =  getfloat(lines[-2])

        for l in lines[:-2]:
            for e in l.split():
                if isfloat(e):
                    self.values.append(getfloat(e))
                else:
                    raise PypactDeserializeException("Entry {} in line {} is not a float.".format(e, l))

        group = len(self.values)
        if group not in ALL_GROUPS:
            raise PypactDeserializeException("Group structure {} not known to pypact.".format(group))

        self._setBoundaries(group)



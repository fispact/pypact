import os

from pypact.input.groupstructures import ALL_GROUPS
from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactOutOfRangeException, PypactDeserializeException


@freeze_it
class FluxesFile(object):
    def __init__(self, name="fluxes", norm=1.0):
        self._name = name
        self._norm = norm
    
        self.boundaries = []
        self.values = []
        self._midPointEnergies = []

    def reset(self):
        self.__init__(name=self._name)

    def setGroup(self, group):
        if group not in ALL_GROUPS:
            raise PypactOutOfRangeException("Group {} is not a valid group".format(group))

        # group structures are in reverse order
        self.boundaries = list(reversed(ALL_GROUPS[group]))
        size = len(self.boundaries)-1
        self.values = [0.0]*size
        self._midPointEnergies = [(self.boundaries[i] + self.boundaries[i+1])/2.0 for i in range(0, size)]

    def setValue(self, energy, value):
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
        f.write("{}\n".format(self._norm))
        f.write(self._name)

    def _deserialize(self, f):
        #todo
        pass

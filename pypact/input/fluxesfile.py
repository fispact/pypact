import os

from pypact.library.groupstructures import ALL_GROUPS
from pypact.util.decorators import freeze_it
from pypact.util.exceptions import (PypactDeserializeException,
                                    PypactException, PypactOutOfRangeException)
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.numerical import get_float, is_float


@freeze_it
class FluxesFile(JSONSerializable):
    """
    FISPACT-II traditionally takes the fluxes file in descending order
    not ascending, hence the reason for the reversed.
    However the values and __boundaries arrays should be in ascending order.
    It is advised that the user should set the values using the setValue
    at a specific energy.
    """

    def __init__(self, name="fluxes", norm=1.0):
        self.name = name
        self.norm = norm

        self.__boundaries = []
        self.__midpointenergies = []
        self.values = []

    def __len__(self):
        return len(self.values)

    def reset(self):
        self.__init__(name=self.name)

    @property
    def boundaries(self):
        return self.__boundaries

    @property
    def midPointEnergies(self):
        return self.__midpointenergies

    def setGroup(self, group):
        if group not in ALL_GROUPS:
            raise PypactOutOfRangeException(
                "Group {} is not a valid group".format(group)
            )

        # group structures are in reverse order
        self._setBoundaries(group)
        self.values = [0.0] * group

    def setValue(self, energy, value):
        """
        Requires setGroup is set before
        """
        if not self.__boundaries:
            raise PypactException("No group set, cannot set value.")

        if value < 0.0:
            raise PypactOutOfRangeException("Flux value cannot be negative.")

        if energy < self.__boundaries[0]:
            raise PypactOutOfRangeException(
                f"Energy value below minimum for group, group min is {self.__boundaries[0]}."
            )

        if energy >= self.__boundaries[-1]:
            raise PypactOutOfRangeException(
                f"Energy value exceeds maximum for group, group max is {self.__boundaries[-1]}."
            )

        for i in range(0, len(self.__boundaries) - 1):
            if self.__boundaries[i + 1] > energy:
                self.values[i] = value
                return

    def validate(self):
        if len(self.__boundaries) != len(self.values) + 1:
            raise PypactOutOfRangeException(
                "Bin boundaries must be of size one greater than values size"
            )

    def _setFromReversedBoundaries(self, boundaries):
        self.__boundaries = list(reversed(boundaries))
        self.__midpointenergies = [
            (self.__boundaries[i] + self.__boundaries[i + 1]) / 2.0
            for i in range(0, len(boundaries) - 1)
        ]

    def _setBoundaries(self, group):
        self._setFromReversedBoundaries(ALL_GROUPS[group])

    def _serialize(self, f):
        """
        The serialization method
        f: file object

        NOTE: The values are in reverse order

        Format is:

        v1
        v2
        ...
        vn
        1.0
        name
        """
        for e in list(reversed(self.values)):
            f.write("{}\n".format(e))
        f.write("{}\n".format(self.norm))
        f.write(self.name)

    def _deserialize(self, f):
        """
        The deserialization method
        f: file object

        NOTE: The values are in reverse order

        Format is:

        v1
        v2
        ...
        vn
        1.0
        name
        """
        self.reset()

        lines = f.readlines()
        # last two lines are the normalisation and the name
        self.name = str(lines[-1])
        self.norm = get_float(lines[-2])

        reversed_values = []
        for l in lines[:-2]:
            for e in l.split():
                if is_float(e):
                    reversed_values.append(get_float(e))
                else:
                    raise PypactDeserializeException(
                        "Entry {} in line {} is not a float.".format(e, l)
                    )

        group = len(reversed_values)
        if group not in ALL_GROUPS:
            raise PypactDeserializeException(
                "Group structure {} not known to pypact.".format(group)
            )

        self.values = list(reversed(reversed_values))
        self._setFromReversedBoundaries(ALL_GROUPS[group])


@freeze_it
class ArbFluxesFile(FluxesFile):
    def __init__(self, *args, **kwargs):
        super(ArbFluxesFile, self).__init__(*args, **kwargs)

    # custom boundaries should be in normal order
    def setGroup(self, boundaries):
        self._setBoundaries(boundaries)
        self.values = [0.0] * (len(boundaries) - 1)

    # custom boundaries should be in normal order
    def _setBoundaries(self, boundaries):
        self._setFromReversedBoundaries(list(reversed(boundaries)))

    def _serialize(self, f):
        """
        The serialization method
        f: file object

        Format is:

        e1
        e2
        ...
        en+1

        v1
        v2
        ...
        vn
        1.0
        name
        """
        for e in list(reversed(self.boundaries)):
            f.write("{}\n".format(e))

        # write space between xs boundaries and values
        f.write("\n")

        for e in list(reversed(self.values)):
            f.write("{}\n".format(e))
        f.write("{}\n".format(self.norm))
        f.write(self.name)

    def _deserialize(self, f):
        """
        The deserialization method
        f: file object

        Format is:

        e1
        e2
        ...
        en+1

        v1
        v2
        ...
        vn
        1.0
        name
        """
        self.reset()

        lines = f.readlines()
        # last two lines are the normalisation and the name
        self.name = str(lines[-1])
        self.norm = get_float(lines[-2])

        found_values = False
        reversed_values = []
        reversed_bounds = []
        for l in lines[:-2]:
            # find the space seperator to indicate flux values not boundaries
            if not l.split():
                found_values = True
            for e in l.split():
                if is_float(e):
                    if found_values:
                        reversed_values.append(get_float(e))
                    else:
                        reversed_bounds.append(get_float(e))
                else:
                    raise PypactDeserializeException(
                        "Entry {} in line {} is not a float.".format(e, l)
                    )

        self.values = list(reversed(reversed_values))
        self._setFromReversedBoundaries(reversed_bounds)

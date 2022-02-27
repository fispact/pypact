from pypact.filerecord import FileRecord
from pypact.library.reactionlib import getmt
from pypact.printlib.tags import (PRINTLIB4_END_HEADER, PRINTLIB4_HEADER,
                                  PRINTLIB4_START_HEADER)
from pypact.reader import Reader
from pypact.util.decorators import freeze_it
from pypact.util.exceptions import PypactNotPrintLib4FileException
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.lines import line_indices
from pypact.util.numerical import get_float


@freeze_it
class PrintLib4FileRecord(FileRecord):
    def _setup(self):
        indices = line_indices(self.cachedlines, PRINTLIB4_HEADER)
        if len(indices) != 1:
            raise PypactNotPrintLib4FileException("Not a valid printlib4 file.")

        sindx = line_indices(self.cachedlines, PRINTLIB4_START_HEADER)
        if len(sindx) != 1:
            raise PypactNotPrintLib4FileException("Not a valid printlib4 file.")

        eindx = line_indices(self.cachedlines, PRINTLIB4_END_HEADER)
        if len(eindx) != 1:
            raise PypactNotPrintLib4FileException("Not a valid printlib4 file.")

        # remove title and next empty line
        self.start_index = sindx[0] + 1
        self.end_index = eindx[0]


@freeze_it
class CollapsedXSData(JSONSerializable):
    # cannot enable slots yet due to json_deserialize_list
    # does not work without __dict__
    # __slots__ = ['nuclide', 'reaction', 'daughter', 'xs', 'delta_xs']

    def __init__(self, nuclide="", reaction="", daughter="", xs=0.0, delta_xs=0.0):
        self.nuclide = nuclide
        self.reaction = reaction
        self.daughter = daughter
        self.xs = xs
        self.delta_xs = delta_xs

    @property
    def findmt(self):
        return getmt(self.reaction[3:-1].strip())

    def fispact_deserialize(self, line):
        self.nuclide = "".join(line[4:11].split()).strip()
        self.reaction = line[11:21].strip()
        self.daughter = "".join(line[22:30].split()).strip()
        self.xs = float(line[29:41])
        self.delta_xs = float(line[44:56])
        return self

    def __repr__(self):
        daughter = "None"
        if self.daughter:
            daughter = self.daughter
        return "{:5} -> {:5}, {:10} @ {:.5e} +- {:.5e}".format(
            self.nuclide, daughter, self.reaction, self.xs, self.delta_xs
        )


@freeze_it
class PrintLib4(JSONSerializable):
    """
    An object to represent the Printlib4 output
    """

    def __init__(self):
        self.cross_sections = []

    def __len__(self):
        return len(self.cross_sections)

    def __getitem__(self, index):
        return self.cross_sections[index]

    def json_deserialize(self, j, objtype=object):
        super().json_deserialize(j)
        self.json_deserialize_list(j, "cross_sections", CollapsedXSData)

    def fispact_deserialize(self, filerecord):
        self.__init__()

        for i in range(filerecord.start_index, filerecord.end_index):
            line = filerecord.cachedlines[i].strip("\n")
            self.cross_sections.append(CollapsedXSData().fispact_deserialize(line[:60]))
            self.cross_sections.append(CollapsedXSData().fispact_deserialize(line[61:]))


class PrintLib4Reader(Reader):
    """
    It can read fispact printlib 4 file formats
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.record = PrintLib4FileRecord(filename)
        self.output = PrintLib4()

    def __enter__(self):
        self.output.fispact_deserialize(self.record)
        return self.output

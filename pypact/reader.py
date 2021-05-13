import os

from pypact.filerecord import InventoryFileRecord
from pypact.output.output import Output


class Reader(object):
    """
    It can read fispact out file formats
    """

    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class InventoryReader(Reader):
    """
    It can read fispact out file formats
    """

    def __init__(self, filename, ignorenuclides=False):
        super().__init__(filename)
        self.record = InventoryFileRecord(filename)
        self.output = Output(ignorenuclides=ignorenuclides)

    def __enter__(self):
        self.output.fispact_deserialize(self.record)
        return self.output


class JSONReader(InventoryReader):
    """
    It can read JSON fispact file formats
    """

    def __enter__(self):
        with open(self.filename, "rt") as f:
            self.output.json_deserialize(f.read())

        return self.output

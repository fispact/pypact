import os

from pypact.filerecord import FileRecord
from pypact.output.output import Output


class Reader(object):
    """
        It can read fispact out file formats
    """
    def __init__(self, filename, ignorenuclides=False):
        self.record = FileRecord(filename)
        self.output = Output(ignorenuclides=ignorenuclides)
        self.filename = filename

    def __enter__(self):
        self.output.fispact_deserialize(self.record)
        return self.output

    def __exit__(self, *args):
        pass


class JSONReader(Reader):
    """
        It can read JSON fispact file formats
    """
    def __enter__(self):
        with open(self.filename, 'rt') as f:
            self.output.json_deserialize(f.read())

        return self.output

    def __exit__(self, *args):
        pass

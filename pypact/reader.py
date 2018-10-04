import os

from pypact.filerecord import FileRecord
from pypact.output.output import Output


class Reader:
    def __init__(self, filename, ignorenuclides=False):
        """
            It can read both JSON and out file formats
        """
        self.record = FileRecord(filename)
        self.output = Output(ignorenuclides=ignorenuclides)
        self.isjson = False
        if os.path.splitext(filename)[-1] == '.json':
            self.isjson = True
            with open(filename) as f:
                self.output.json_deserialize(f.read())

    def __enter__(self):
        if not self.isjson:
            self.output.fispact_deserialize(self.record)

        return self.output

    def __exit__(self, *args):
        pass

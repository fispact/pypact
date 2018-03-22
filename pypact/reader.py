from pypact.filerecord import FileRecord
from pypact.output.output import Output


class Reader:
    def __init__(self, filename):
        self.record = FileRecord(filename)
        self.output = Output()

    def __enter__(self):
        self.output.fispact_deserialize(self.record)
        return self.output

    def __exit__(self, *args):
        pass

from pypact.reader.filerecord import FileRecord
from pypact.util.file import content_as_str
from pypact.output.output import Output


class Reader:
    def __init__(self):
        self.output = Output()

    def __call__(self, filename):

        fr = FileRecord(filename)
        self.output.fispact_deserialize(fr)

        return self.output

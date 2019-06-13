from pypact.output.tags import GAMMA_SPECTRUM_SUB_HEADER
from pypact.util.decorators import freeze_it
from pypact.util.jsonserializable import JSONSerializable


@freeze_it
class GammaSpectrum(JSONSerializable):
    """
        The gamma spectrum type from the output
    """

    def __init__(self):
        self.boundaries = []   # TODO dvp: should be numpy arrays (or even better xarrays)
        self.values = []

    def fispact_deserialize(self, file_record, interval):
        self.__init__()

        lines = file_record[interval]

        def extract_boundaries_and_values(_lines):
            header_found = False
            for line in _lines:
                if not header_found:
                    if GAMMA_SPECTRUM_SUB_HEADER in line:
                        header_found = True
                if header_found:
                    if line.strip() == "":
                        return
                    _, line = line.split('-', maxsplit=1)    # drop the not interesting first part
                    tokens = line.split()
                    boundary = float(tokens[0])  # the first token is boundary
                    value = float(tokens[2])     # the third one is MeV/s/group
                    yield boundary, value

        boundaries = [0.0]
        values = []

        for b, v in extract_boundaries_and_values(lines):
            boundaries.append(b)
            values.append(v)

        if values:
            self.boundaries = boundaries
            self.values = values

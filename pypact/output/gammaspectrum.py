import re

from pypact.output.tags import GAMMA_SPECTRUM_SUB_HEADER
from pypact.util.decorators import freeze_it
from pypact.util.jsonserializable import JSONSerializable

FLOAT_NUMBER = r"[0-9]+(?:\.(?:[0-9]+))?(?:e?(?:[-+][0-9]+)?)?"
GAMMA_SPECTRUM_LINE = \
    r"[^(]*\(\s*(?P<lb>{FN})\s*-\s*(?P<ub>{FN})\s*MeV\)\s*(?P<value>{FN}).*".format(
       FN=FLOAT_NUMBER,
    )
GAMMA_SPECTRUM_LINE_MATCHER = re.compile(GAMMA_SPECTRUM_LINE, re.IGNORECASE)

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
                    match = GAMMA_SPECTRUM_LINE_MATCHER.match(line)
                    lower_boundary = float(match.group("lb"))
                    upper_boundary = float(match.group("ub"))
                    value = float(match.group("value"))
                    yield lower_boundary, upper_boundary, value

        boundaries = []
        values = []

        for lb, ub, v in extract_boundaries_and_values(lines):
            if not boundaries:
                boundaries.append(lb)
            boundaries.append(ub)
            values.append(v)

        if values:
            self.boundaries = boundaries
            self.values = values

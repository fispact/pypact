from pypact.util.decorators import freeze_it
from pypact.util.numerical import getfloat
from pypact.util.exceptions import PypactDeserializeException
from pypact.util.lines import first_value_from_line, strings_from_line
from pypact.output.serializable import Serializable
from pypact.output.tags import DOSE_RATE_HEADER
import pypact.util.propertyfinder as pf
from pypact.util.lines import first_occurrence, first_value_from_line

GAMMA_SPECTRUM_IGNORES = ['\n']


@freeze_it
class GammaSpectrum(Serializable):
    """
        The gamma spectrum type from the output
    """
    def __init__(self):
        self.boundaries = []
        self.values     = []

    def fispact_deserialize(self, filerecord, interval):
        self.__init__()

        substring = filerecord[interval]

        # get the
        startindex, startline = first_occurrence(lines=substring, tag='GAMMA RAY POWER FROM ACTIVATION DECAY  MeV/s    (')
        endindex, endline = first_occurrence(lines=substring, tag=DOSE_RATE_HEADER)
        if startindex < 0 or endindex < 0:
            return
        
        end = endindex-startindex-1
        for i in range(0, end):
            line = substring[startindex+i:startindex+i+1][0]
            # we need to do this since in the output file the lower bin has a - without a whitespace after the value
            boundaries_line = line.split('-')
            if len(boundaries_line) < 2:
                raise PypactDeserializeException("Error when reading gamma spectrum, expected format as ( lb- ub MeV).")
            
            lower_bin = first_value_from_line(boundaries_line[0], '(', ignoretags=[])
            self.boundaries.append(lower_bin)
            
            # since we should have n+1 boundaries for n bin values we must append the final upper bound at the end
            if i == end-1:
                upper_bin = first_value_from_line(boundaries_line[1], '', ignoretags=[])
                self.boundaries.append(upper_bin)
            
            # the bin value
            value = first_value_from_line(line, 'MeV)', ignoretags=[])
            self.values.append(value)

from pypact.util.decorators import freeze_it
from pypact.util.numerical import getfloat
from pypact.util.lines import first_value_from_line, strings_from_line
from pypact.output.serializable import Serializable
from pypact.output.tags import DOSE_RATE_HEADER
import pypact.util.propertyfinder as pf

DOSE_RATE_IGNORES = ['\n', '|']


@freeze_it
class DoseRate(Serializable):
    """
        The dose rate type from the output
    """
    def __init__(self):
        self.type = ""
        self.distance = 0.0
        self.mass = 0.0
        self.dose = 0.0

    def fispact_deserialize(self, filerecord, interval):

        self.__init__()

        substring = filerecord[interval]

        dose_string = pf.first(datadump=substring,
                               headertag=DOSE_RATE_HEADER,
                               starttag=DOSE_RATE_HEADER,
                               endtag=')',
                               ignores=DOSE_RATE_IGNORES,
                               asstring=True)

        if 'PLANE' in dose_string:
            self.type = 'PLANE SOURCE'
        elif 'POINT' in dose_string:
            self.type = 'POINT SOURCE'

            # Mass is always in grams and is actually always 1 g
            # but read it in to verify
            self.mass = first_value_from_line(dose_string, '')*1e-3

            # Distance is always in meters but is written without a space so
            # we must strip it off
            self.distance = getfloat(strings_from_line(dose_string, 'SOURCE')[-1].replace('m', ''))

        self.dose = pf.first(datadump=substring,
                             headertag=DOSE_RATE_HEADER,
                             starttag='IS',
                             endtag='Sieverts/hour',
                             ignores=DOSE_RATE_IGNORES,
                             asstring=False)

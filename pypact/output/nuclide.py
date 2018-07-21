from pypact.util.decorators import freeze_it
from pypact.util.numerical import isfloat
from pypact.util.jsonserializable import JSONSerializable

NUCLIDE_IGNORES = ['\n', '|', '>', '&', '?', '#']


@freeze_it
class Nuclide(JSONSerializable):
    """
        The nuclide type from the output
    """
    def __init__(self):
        self.element = ""
        self.isotope = 0
        self.state = ""
        self.half_life = 0.0
        self.grams = 0.0
        self.activity = 0.0
        self.heat = 0.0
        self.alpha_heat = 0.0
        self.beta_heat = 0.0
        self.gamma_heat = 0.0
        self.dose = 0.0
        self.ingestion = 0.0
        self.inhalation = 0.0

    def fispact_deserialize(self, linedump, column_headers):

        self.__init__()

        # takes the first line of the dump and
        # strip of the markers and ignores
        line = linedump[0]
        for i in NUCLIDE_IGNORES:
            line = line.replace(i, '')

        # turn the line into a list
        strings = line.split()

        # first 2 characters are the symbol
        # next 3 characters are the symbol
        # last character is the symbol
        symbollength = 2
        isotopelength = 3
        if len(strings[0]) > symbollength:
            isotope = strings[0][symbollength:]
            strings[0] = strings[0][:symbollength]
            strings.insert(1, isotope)

        if strings[1][-1].isalpha():
            self.state = strings[1][-1]
            strings[1] = strings[1][:-1]

        self.element = strings[0]
        self.isotope = int(strings[1][:isotopelength])

        # Remove the isotope entry so that the entries now match with the header
        strings.pop(1)

        assert(len(column_headers) == len(strings))

        def get_entry(header_name):
            column_index = index_containing_substring(column_headers, header_name)
            if column_index != -1:
                item = strings[column_index]
                if isfloat(item):
                    return float(item)

            return 0.0

        self.grams = get_entry('GRAMS')
        self.activity = get_entry('Bq')
        self.half_life = get_entry('HALF LIFE')
        self.alpha_heat = get_entry('a-Energy')
        self.beta_heat = get_entry('b-Energy')
        self.gamma_heat = get_entry('g-Energy')
        # since the precision in the output file is to 4 significant figures of beta and gamma heats
        # we must set the precision to 4 significant figures for the total heat,
        # otherwise it is misleading to the user if they get 13.45999999999999999e-5 instead of 1.346e-4
        self.heat = float("{0:.4g}".format(self.alpha_heat + self.beta_heat + self.gamma_heat))
        self.dose = get_entry('DOSE RATE')
        self.ingestion = get_entry('INGESTION')
        self.inhalation = get_entry('INHALATION')


def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1

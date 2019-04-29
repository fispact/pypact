from pypact.util.decorators import freeze_it
from pypact.util.jsonserializable import JSONSerializable
from pypact.util.lines import line_indices
from pypact.util.exceptions import PypactNotPrintLib5FileException
from pypact.util.numerical import get_float
from pypact.printlib.tags import PRINTLIB5_HEADER
from pypact.filerecord import FileRecord
from pypact.reader import Reader


@freeze_it
class PrintLib5FileRecord(FileRecord):

    def _setup(self):
        indx = line_indices(self.cachedlines, PRINTLIB5_HEADER)
        assert len(indx) == 2
        
        # remove title and next empty line
        self.mean_start_index = indx[0]+ 2
        self.line_start_index = indx[1]
        self.nr_of_entries = 0

    def _process(self):
        if not line_indices(self.cachedlines, "Nuclide Nuclide Nuclide"):
            raise PypactNotPrintLib5FileException(
                "Not a valid printlib5 file or SAVELINES was not used, as no spectral data exists.")

        # off set start index to remove header (column titles are 2 lines)
        self.mean_start_index = self.mean_start_index + 2
        self.nr_of_entries = self.line_start_index - self.mean_start_index

@freeze_it
class SpectralLineData(JSONSerializable):
    """
        Spectral line data
    """
    def __init__(self):    
        self.energies = []
        self.energies_unc = []
        self.intensities = []
        self.intensities_unc = []
        self.norms = []
        self.norms_unc = []

    def __len__(self):
        return len(self.energies)

    def __getitem__(self, index):
        return (self.energies[index],
                self.energies_unc[index],
                self.intensities[index],
                self.intensities_unc[index],
                self.norms[index],
                self.norms_unc[index])

    def addline(self, energy, energy_unc, intensity, intensity_unc, norm, norm_unc):
        self.energies.append(energy)
        self.energies_unc.append(energy_unc)
        self.intensities.append(intensity)
        self.intensities_unc.append(intensity_unc)
        self.norms.append(norm)
        self.norms_unc.append(norm_unc)

@freeze_it
class SpectralData(JSONSerializable):
    """
        Spectral data
    """
    def __init__(self):
        self.name = ""
        self.zai = 0
        self.number = 0
        self.type = ""
        self.nr_of_lines = 0
        self.mean_energy = 0.0
        self.mean_energy_unc = 0.0
        self.mean_normalisation = 0.0
        self.mean_normalisation_unc = 0.0
        self.lines = SpectralLineData()

    def fispact_deserialize(self, linedump):
        self.__init__()

        line = linedump[0].strip('\n')

        # fortran format is:
        # format(2x,a6,i8,i6,3x,a9,6x,i8,2x,es13.5,' +-',es12.5,es13.5,' +-',es12.5)
        self.name = line[2:8].strip()
        self.zai = int(line[8:16])
        self.number = int(line[16:22])

        # this is a really horrible hack, but the logic used to make the output file
        # is really bad - "no spectral data" is output if no data exists, but this has
        # length 16 but otherwise the length of type is 9 +6 whitespace = 15, so just 1 off
        # why did they do this???
        # Because of this stupid logic we have to hack here
        self.type = line[25:40].strip()

        # if no spectral data then skip
        if self.type == "no spectral dat":
            self.type = "no spectral data"
            return

        self.nr_of_lines = int(line[40:48])
        self.mean_energy = get_float(line[50:63])
        self.mean_energy_unc = get_float(line[66:78])
        self.mean_normalisation = get_float(line[78:91])
        self.mean_normalisation_unc = get_float(line[94:106])

@freeze_it
class PrintLib5(JSONSerializable):
    """
        An object to represent the Printlib5 output
    """
    def __init__(self):
        self.spectral_data = []
        self.nr_of_zais = 0

    def __len__(self):
        return len(self.spectral_data)

    def __getitem__(self, index):
        return self.spectral_data[index]

    def json_deserialize(self, j, objtype=object):
        super().json_deserialize(j)
        self.json_deserialize_list(j, 'spectral_data', SpectralData)

    def fispact_deserialize(self, filerecord):
        self.__init__()

        # ignore header and column headers
        current_line_index = filerecord.line_start_index + 4

        # printlib file loops over ZAIs then loops over decay types
        for i in range(filerecord.nr_of_entries):
            spectral_data = SpectralData()
            indx = filerecord.mean_start_index+i
            spectral_data.fispact_deserialize(filerecord.cachedlines[indx:indx+1])
            self.nr_of_zais = max(self.nr_of_zais, spectral_data.number)

            # due to a bug in FISPACT-II or nuclear data
            # the number of spectral_data.nr_of_lines can be 0 sometimes
            # with type not equal to "no spectral data"
            # need to account for this 
            if (spectral_data.nr_of_lines == 0) and (spectral_data.type != "no spectral data"):
                continue

            if spectral_data.nr_of_lines > 0:            
                # next find the line data for that ZAI
                # we know that FISPACT-II writes it in the same order as averages
                line_data = filerecord.cachedlines[current_line_index:current_line_index+spectral_data.nr_of_lines]
                current_line_index += spectral_data.nr_of_lines
                # loop over decay types
                for line in line_data:
                    # first 41 characters are redundant - information is same as in mean data section
                    # format after is then 
                    # (3(es13.5,' +-',es12.5))
                    d = line[41:]
                    spectral_data.lines.addline(energy=float(d[:13]),
                                                energy_unc=float(d[16:28]),
                                                intensity=float(d[28:41]),
                                                intensity_unc=float(d[44:56]),
                                                norm=float(d[56:69]),
                                                norm_unc=float(d[72:84]))
                assert spectral_data.nr_of_lines == len(spectral_data.lines)
            else:
                current_line_index += 1

            # append to data
            self.spectral_data.append(spectral_data)

class PrintLib5Reader(Reader):
    """
        It can read fispact printlib 5 file formats
    """
    def __init__(self, filename):
        super().__init__(filename)
        self.record = PrintLib5FileRecord(filename)
        self.output = PrintLib5()

    def __enter__(self):
        self.output.fispact_deserialize(self.record)
        return self.output
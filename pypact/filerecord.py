from itertools import accumulate
from pypact.util.file import content_as_str
from pypact.util.lines import line_indices
from pypact.output.tags import TIME_STEP_HEADER, IRRAD_TIME_TAG, COOLING_TIME_TAG
import pypact.util.propertyfinder as pf


class FileRecord:

    def __init__(self, filename, asstring=''):
        """
        Cache the file content as a list of strings and process the timesteps
        :param filename:
        """

        self.cachedlines = (asstring if asstring else content_as_str(filename))
        self.lineindices = line_indices(self.cachedlines, TIME_STEP_HEADER)
        self.timesteps = []
        self.irradiation_times = []
        self.cooling_times = []

        self._processtimesteps()

    def __len__(self):
        return len(self.lineindices)

    def __getitem__(self, interval):
        """
        Get the timestep lines for a given interval

        :param interval:
        :return:
        """
        l = [s for i, s in self.timesteps if i == interval]
        if len(l) == 1:
            return l[0]

        return ''

    def cumulirradiationtime(self, interval):
        """
        Get the cumulative irradiation time at a given interval

        :param interval:
        :return:
        """
        return self._getcumultime(interval, self.irradiation_times)

    def cumulcoolingtime(self, interval):
        """
        Get the cumulative irradiation time at a given interval

        :param interval:
        :return:
        """
        return self._getcumultime(interval, self.cooling_times)

    def _processtimesteps(self):

        for i in range(0, len(self)):
            t = self.lineindices[i]
            nt = -1
            if i < len(self.lineindices) - 1:
                nt = self.lineindices[i+1]

            interval = int(pf.first(datadump=self.cachedlines[t:nt],
                                    headertag=TIME_STEP_HEADER,
                                    starttag=TIME_STEP_HEADER,
                                    endtag='',
                                    ignores=[],
                                    asstring=False))

            irrad_time = pf.first(datadump=self.cachedlines[t:nt],
                                  headertag=TIME_STEP_HEADER,
                                  starttag=IRRAD_TIME_TAG,
                                  endtag='SECS',
                                  ignores=[],
                                  asstring=False)

            cool_time = pf.first(datadump=self.cachedlines[t:nt],
                                 headertag=TIME_STEP_HEADER,
                                 starttag=COOLING_TIME_TAG,
                                 endtag='SECS',
                                 ignores=[],
                                 asstring=False)

            self.timesteps.append((interval, self.cachedlines[t:nt]))
            self.irradiation_times.append(irrad_time)
            self.cooling_times.append(cool_time)

        # turn them into cumulative values
        self.irradiation_times = list(accumulate(self.irradiation_times))
        self.cooling_times = list(accumulate(self.cooling_times))

        assert len(self.irradiation_times) == len(self.cooling_times)

    def _getcumultime(self, interval, listoftuples):
        t = [x for x, y in enumerate(self.timesteps) if y[0] == interval]
        if len(t) == 1:
            return listoftuples[t[0]]

        return 0.0

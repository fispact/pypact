from pypact.output.serializable import Serializable
import pypact.util.propertyfinder as pf

RUN_DATA_IGNORES = ['\n', '|']


class RunData(Serializable):
    """
        The run data type from the output
    """
    def __init__(self):
        self.timestamp = ""
        self.run_name = ""
        self.flux_name = ""

    def fispact_deserialize(self, filerecord):
        self.__init__()

        self.timestamp = pf.first(datadump=filerecord.cachedlines,
                                  headertag='THIS RUN',
                                  starttag='timestamp:',
                                  endtag='',
                                  ignores=RUN_DATA_IGNORES,
                                  asstring=True)

        self.run_name = pf.first(datadump=filerecord.cachedlines,
                                 headertag='THIS RUN',
                                 starttag='FISPACT title:',
                                 endtag='',
                                 ignores=RUN_DATA_IGNORES,
                                 asstring=True)

        self.flux_name = pf.first(datadump=filerecord.cachedlines,
                                  headertag='INITIAL CROSS SECTION DATA',
                                  starttag='FLUX file label:',
                                  endtag='',
                                  ignores=RUN_DATA_IGNORES,
                                  asstring=True)

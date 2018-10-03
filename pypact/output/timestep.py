from pypact.output.serializable import Serializable
from pypact.output.doserate import DoseRate
from pypact.output.nuclides import Nuclides
from pypact.output.tags import TIME_STEP_HEADER
import pypact.util.propertyfinder as pf

TIME_STEP_IGNORES = []


class TimeStep(Serializable):
    """
        An object to represent a time step in the output
    """
    def __init__(self):
        self.irradiation_time = 0.0
        self.cooling_time = 0.0
        self.flux = 0.0
        self.total_heat = 0.0
        self.alpha_heat = 0.0
        self.beta_heat = 0.0
        self.gamma_heat = 0.0
        self.ingestion_dose = 0.0
        self.inhalation_dose = 0.0
        self.total_activity = 0.0
        self.total_activity_exclude_trit = 0.0
        self.total_displacement_rate = 0.0
        self.time = 0.0
        self.dose_rate = DoseRate()
        self.nuclides = Nuclides()

    def fispact_deserialize(self, filerecord, interval):

        # reset to defaults before reading
        self.__init__()

        self.irradiation_time = filerecord.cumulirradiationtime(interval)
        self.cooling_time = filerecord.cumulcoolingtime(interval)

        substring = filerecord[interval]

        def get_value(starttag, endtag):
            return pf.first(datadump=substring,
                            headertag=TIME_STEP_HEADER,
                            starttag=starttag,
                            endtag=endtag,
                            ignores=TIME_STEP_IGNORES,
                            asstring=False)

        self.flux = get_value(starttag='* * * FLUX AMP IS', endtag='/cm^2/s')

        self.alpha_heat = get_value(starttag='TOTAL ALPHA HEAT PRODUCTION', endtag='kW')
        self.beta_heat = get_value(starttag='TOTAL BETA  HEAT PRODUCTION', endtag='kW')
        self.gamma_heat = get_value(starttag='TOTAL GAMMA HEAT PRODUCTION', endtag='kW')
        self.total_heat = self.alpha_heat + self.beta_heat + self.gamma_heat

        self.ingestion_dose = get_value(starttag='INGESTION  HAZARD FOR ALL MATERIALS', endtag='Sv/kg')
        self.inhalation_dose = get_value(starttag='INHALATION HAZARD FOR ALL MATERIALS', endtag='Sv/kg')

        self.total_activity = get_value(starttag='TOTAL ACTIVITY FOR ALL MATERIALS', endtag='Bq')
        self.total_activity_exclude_trit = get_value(starttag='TOTAL ACTIVITY EXCLUDING TRITIUM', endtag='Bq')

        self.total_displacement_rate = pf.first(
            datadump=substring,
            headertag="Total Displacement Rate (n,Dtot ) =",
            starttag="Displacements/sec  =",
            endtag="Displacements Per Atom/sec  =",
            ignores=TIME_STEP_IGNORES,
            asstring=False
        )
        self.time = filerecord.times[interval - 1]

        self.dose_rate.fispact_deserialize(filerecord, interval)
        self.nuclides.fispact_deserialize(filerecord, interval)

import json

from pypact.util.decorators import freeze_it
from pypact.util.jsonserializable import JSONSerializable
from pypact.output.doserate import DoseRate
from pypact.output.nuclides import Nuclides
from pypact.output.nuclide import Nuclide
from pypact.output.gammaspectrum import GammaSpectrum
from pypact.output.tags import TIME_STEP_HEADER
import pypact.util.propertyfinder as pf

TIME_STEP_IGNORES = []


@freeze_it
class TimeStep(JSONSerializable):
    """
        An object to represent a time step in the output
    """

    def __init__(self, ignorenuclides=False):
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
        self.alpha_activity = 0.0
        self.beta_activity = 0.0
        self.gamma_activity = 0.0
        self.initial_mass = 0.0
        self.total_mass = 0.0
        self.number_of_fissions = 0.0
        self.burnup = 0.0
        self.gamma_spectrum = GammaSpectrum()
        self.total_displacement_rate = 0.0
        self.time = 0.0
        self.dose_rate = DoseRate()
        self.nuclides = []

        self.__ignorenuclides = ignorenuclides

    @property
    def isirradiation(self):
        return self.cooling_time == 0.0

    @property
    def currenttime(self):
        if self.isirradiation:
            return self.irradiation_time
        return self.cooling_time

    def fispact_deserialize(self, filerecord, interval):

        # reset to defaults before reading
        self.__init__(ignorenuclides=self.__ignorenuclides)

        substring = filerecord[interval]

        if substring:
            self.irradiation_time = filerecord.cumulirradiationtime(interval)
            self.cooling_time = filerecord.cumulcoolingtime(interval)

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

            self.initial_mass = get_value(starttag='INITIAL TOTAL MASS OF MATERIAL', endtag='kg')
            self.total_mass = get_value(starttag='TOTAL MASS OF MATERIAL', endtag='kg')

            self.number_of_fissions = get_value(starttag='NUMBER OF FISSIONS', endtag='BURN-UP')
            self.burnup = get_value(starttag='BURN-UP OF ACTINIDES', endtag='%')

            self.ingestion_dose = get_value(starttag='INGESTION  HAZARD FOR ALL MATERIALS', endtag='Sv/kg')
            self.inhalation_dose = get_value(starttag='INHALATION HAZARD FOR ALL MATERIALS', endtag='Sv/kg')

            self.total_activity = get_value(starttag='TOTAL ACTIVITY FOR ALL MATERIALS', endtag='Bq')
            self.total_activity_exclude_trit = get_value(starttag='TOTAL ACTIVITY EXCLUDING TRITIUM', endtag='Bq')

            self.dose_rate.fispact_deserialize(filerecord, interval)
            self.gamma_spectrum.fispact_deserialize(filerecord, interval)

            self.total_displacement_rate = pf.first(
                datadump=substring,
                headertag="Total Displacement Rate (n,Dtot ) =",
                starttag="Displacements/sec  =",
                endtag="Displacements Per Atom/sec  =",
                ignores=TIME_STEP_IGNORES,
                asstring=False
            )
            self.time = filerecord.times[interval - 1]

            self.flux = get_value(starttag='* * * FLUX AMP IS', endtag='/cm^2/s')

            self.alpha_heat = get_value(starttag='TOTAL ALPHA HEAT PRODUCTION', endtag='kW')
            self.beta_heat = get_value(starttag='TOTAL BETA  HEAT PRODUCTION', endtag='kW')
            self.gamma_heat = get_value(starttag='TOTAL GAMMA HEAT PRODUCTION', endtag='kW')
            self.total_heat = self.alpha_heat + self.beta_heat + self.gamma_heat

            self.initial_mass = get_value(starttag='0  INITIAL TOTAL MASS OF MATERIAL', endtag='kg')
            self.total_mass = get_value(starttag='0  TOTAL MASS OF MATERIAL', endtag='kg')

            self.number_of_fissions = get_value(starttag='NUMBER OF FISSIONS', endtag='BURN-UP')
            self.burnup = get_value(starttag='BURN-UP OF ACTINIDES', endtag='%')

            self.ingestion_dose = get_value(starttag='INGESTION  HAZARD FOR ALL MATERIALS', endtag='Sv/kg')
            self.inhalation_dose = get_value(starttag='INHALATION HAZARD FOR ALL MATERIALS', endtag='Sv/kg')

            self.alpha_activity = get_value(starttag='ALPHA BECQUERELS =', endtag='BETA')
            self.beta_activity = get_value(starttag='BETA BECQUERELS =', endtag='GAMMA')
            self.gamma_activity = get_value(starttag='GAMMA BECQUERELS =', endtag='')

            self.total_activity = get_value(starttag='TOTAL ACTIVITY FOR ALL MATERIALS', endtag='Bq')
            self.total_activity_exclude_trit = get_value(starttag='TOTAL ACTIVITY EXCLUDING TRITIUM', endtag='Bq')

            # for fission this can be very large and hence very slow
            # if you do not care about the nuclides then we can set
            # it to ignore nuclides
            if not self.__ignorenuclides:
                t = Nuclides()
                t.fispact_deserialize(filerecord, interval)
                self.nuclides = t.nuclides


    def json_deserialize(self, json_dump, objtype=object):

        self.__init__(ignorenuclides=self.__ignorenuclides)

        d = JSONSerializable.json_deserialize(self, json_dump, objtype)

        if not self.__ignorenuclides:
            key = 'nuclides'
            if key in d:
                self.json_deserialize_list(json.dumps(d[key]), key, objtype=Nuclide)
